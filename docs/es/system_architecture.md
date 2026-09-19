# Visión general de la arquitectura del sistema

La plataforma Lacerta consta de cuatro componentes principales: la **implementación en silicio a medida**, el **hardware PCBA**, la **capa de firmware** y el **software de diseño de interfaces**. En conjunto, estos elementos forman un sistema completo de código abierto para crear, desplegar y operar interfaces gráficas embebidas personalizables.

## Silicio a medida (proyecto de usuario de Caravel)

El núcleo de la plataforma Lacerta es un ASIC a medida implementado en el **proceso SKY130** e integrado dentro del **área de proyecto de usuario de Caravel**. Este subsistema realiza el motor de gráficos por hardware que recibe los comandos de la interfaz, actualiza el estado interno de la pantalla y genera el flujo de salida que se presenta en la pantalla.

El ASIC de Lacerta sigue una arquitectura centrada en la memoria. Los datos de configuración y los valores en tiempo de ejecución entran al sistema por **UART**. Según el modo de operación seleccionado, los datos recibidos pueden reenviarse directamente al área de proyecto de usuario o procesarse primero en el procesador **RISC-V de Caravel** integrado. Las transacciones internas se enrutan por la **interconexión Wishbone** hacia la lógica de renderizado, que actualiza el contenido del cuadro almacenado en memoria. El bloque de salida de pantalla lee entonces esa memoria y la convierte continuamente en la señal que necesita la **pantalla TFT/OLED SPI** conectada.

El ASIC incluye los siguientes módulos principales:

- la interfaz con la SRAM externa,
- la interfaz SPI de la TFT,
- la interfaz de comandos UART,
- la interfaz Wishbone,
- la lógica de actualización de pantalla,
- la lógica de dibujo,
- y el subsistema de memoria compartida.


:::{figure} ../assets/img/lacerta_blockd_vfinal.png
:alt: Diagrama de bloques del ASIC Lacerta dentro del entorno Caravel
:align: center

**Figura 5.** Diagrama de bloques del ASIC Lacerta dentro del entorno Caravel. La figura muestra cómo interactúan los datos UART y el procesador RISC-V de Caravel integrado a través de la ruta de control conectada por Wishbone, la lógica de renderizado y el subsistema de memoria; el bloque de salida de pantalla lee después los datos actualizados del cuadro para manejar la pantalla.
:::

Su función principal es enrutar las solicitudes de distintos clientes hacia el mismo sistema de memoria. En este diseño, varios bloques pueden necesitar acceso a la memoria en momentos distintos:

- la ruta del anfitrión UART,
- la ruta de refresco de pantalla,
- la ruta de actualización de dibujo/máscara,
- y la ruta de Wishbone/procesador.

`dig_top` asigna cada uno de estos clientes a buffers de lectura/escritura dedicados y luego los conecta a `mem_sys`.

## Subsistema de memoria

### `memory_system/mem_sys.v`

`mem_sys` es el gestor del tráfico de memoria. Envuelve los bloques internos de almacenamiento en buffers y de arbitraje que se usan para acceder a la SRAM externa de forma segura y eficiente.

Su función es:

- aceptar múltiples solicitudes de lectura y escritura de clientes independientes,
- encolar los datos mediante FIFO,
- arbitrar los accesos a la memoria principal,
- y presentar al resto del sistema una interfaz con buffers más sencilla.

### `memory_system/buffers.v`

Este módulo instancia las FIFO que usa el subsistema de memoria.

Existen:

- buffers de lectura, llenados con datos que vienen de la SRAM,
- y buffers de escritura, cargados por los productores antes de que los datos se confirmen en la SRAM.

Este almacenamiento en buffers desacopla el acceso a memoria, lento o a ráfagas, de la lógica que produce o consume píxeles.

### `memory_system/buffers_filler.v`

Este bloque gestiona el arbitraje del lado de lectura de la SRAM.

Cuando un cliente solicita una lectura en ráfaga, `buffers_filler`:

- inicia la ráfaga de lectura,
- obtiene bytes de la SRAM,
- y los escribe en el buffer de lectura seleccionado.

Es especialmente importante para:

- los refrescos de pantalla,
- las operaciones de dibujo que necesitan leer los píxeles actuales,
- y las lecturas por Wishbone/UART.

### `memory_system/buffers_discharger.v`

Este bloque gestiona el arbitraje del lado de escritura de la SRAM.

Cuando un cliente tiene datos listos en un buffer de escritura, `buffers_discharger`:

- lee bytes de la FIFO de escritura seleccionada,
- los escribe en la SRAM,
- y confirma la ráfaga de escritura al terminar.

Es la ruta que se usa cuando hay que guardar de nuevo en memoria datos de imagen nuevos o píxeles modificados.

### `memory_system/sfifo.v`

Es la FIFO síncrona genérica que sirve de bloque constructivo de los buffers de lectura y escritura.

### `memory_system/sram_controller.v`

Este módulo convierte el protocolo interno de lectura/escritura de memoria en las señales de control reales de la SRAM externa.

Es el puente de bajo nivel entre el sistema de memoria interno con buffers y los pines físicos de la SRAM.

## Subsistema de salida de pantalla

### `screen/screen_system.v`

`screen_system` es el módulo superior de la ruta de salida a la pantalla.

Envuelve:

- `tft_control_fsm`,
- `spi_master`,
- y `color_mapping_table`.

Su trabajo es convertir los datos de píxeles almacenados en la SRAM en transacciones seriales para la pantalla TFT.

### `screen/tft_control_fsm.v`

Es el controlador principal de la pantalla.

Realiza tres funciones principales:

1. Inicialización de la TFT  
   Lee una pequeña memoria de inicialización y envía secuencias de comandos y datos para configurar el controlador de la TFT.

2. Refresco de cuadro o de región  
   Recibe una región rectangular por actualizar, lee de la memoria los bytes de píxeles correspondientes y los envía a la RAM de la TFT.

3. Carga de la barra lateral o del logotipo  
   También puede cargar un área de barra lateral con datos de píxel directos de 16 bits.

En el área activa de la HMI, la lógica de pantalla no siempre almacena píxeles RGB565 completos en memoria. En su lugar, puede almacenar códigos de píxel compactos que indexan una tabla de colores. Esto reduce el uso de memoria y permite asociar colores lógicos con valores RGB565 reales durante la visualización.

### `screen/color_mapping_table.v`

Este módulo es una pequeña tabla de consulta programable.

Convierte índices compactos de píxel/color en valores RGB565 de 16 bits antes de la transmisión a la TFT. Es útil para gráficos de HMI en los que muchos píxeles reutilizan un pequeño conjunto de colores.

### `screen/spi_master.v`

Este bloque serializa bytes hacia la interfaz SPI de la TFT.

Envía:

- comandos del controlador,
- parámetros de los comandos,
- y bytes de píxeles.

### Comportamiento relacionado con la TFT

La ruta de pantalla admite actualizaciones parciales. En lugar de redibujar toda la pantalla cada vez, el sistema puede actualizar solo la región rectangular afectada por el cambio de un objeto. Esto encaja bien con pantallas de HMI en las que indicadores, barras, gráficas o dígitos cambian de forma independiente.

## Subsistema de dibujo y actualización gráfica

### `drawing/mask_generator.v`

`mask_generator` es el motor de actualización de objetos.

Lee bytes de píxeles existentes de la memoria, modifica bits seleccionados según el tipo de objeto y escribe de nuevo los bytes actualizados en la SRAM.

Los estilos de objeto admitidos incluyen:

- objetos de tipo booleano,
- objetos incrementales horizontales,
- objetos incrementales verticales,
- objetos de tipo gráfica,
- y objetos basados en máscara, como las pantallas de 7 segmentos.

Al terminar la actualización de memoria, este bloque dispara un refresco de pantalla de la región afectada para que la TFT muestre el nuevo estado de la HMI.

En la práctica, este es uno de los bloques clave que hacen que el sistema se comporte como una HMI y no solo como un buffer de cuadro.

## Subsistema de comando y control

### `command_arbiter_decoder.v`

Este bloque es el decodificador central de comandos.

Recibe transacciones de control desde:

- la interfaz UART mapeada en memoria,
- y la interfaz de control Wishbone.

Las decodifica en acciones como:

- iniciar lecturas o escrituras de memoria,
- configurar los parámetros de los objetos de dibujo,
- disparar el redibujado de objetos,
- configurar las entradas de inicialización de la pantalla,
- configurar el mapa de colores,
- iniciar un refresco de la TFT,
- habilitar la ruta del microprocesador,
- o solicitar un reinicio por software.

Este módulo es, en la práctica, el centro del plano de control del sistema.

## Subsistema UART

### `uart/uart_ip_memory_mapped.v`

Es el extremo frontal UART que usa un anfitrión externo.

Convierte paquetes UART en operaciones sencillas de lectura/escritura mapeadas en memoria. Esto permite que una PC o un controlador externo cargue datos de imagen, programe la configuración de la pantalla y dispare operaciones de dibujo o refresco sin tocar directamente los detalles internos del RTL.

### Otros archivos UART

Los módulos UART restantes implementan el funcionamiento interno del enlace serial:

- ruta de recepción,
- ruta de transmisión,
- generación del reloj de baudios,
- registros de estado y de control,
- sincronización,
- y la FSM de paquetes y control.

En conjunto, proporcionan un puerto de comandos para la configuración, la depuración y la carga de datos de imagen y de control.

## Wishbone e interfaz con el procesador

### `wb_slave/wb_slave_memory_mapped.v`

Este módulo expone una interfaz esclava Wishbone para accesos orientados al control.

Se usa para registros de control mapeados en memoria, como los comandos de dibujo y los comandos de control de pantalla.

### `wb_slave/wb_slave_to_mem_sys_ports.v`

Este módulo adapta las transacciones Wishbone al sistema de memoria interno orientado a bytes.

Como Wishbone tiene un ancho de 32 bits y la ruta de memoria principal es de 8 bits, este bloque divide o ensambla los accesos en varias transferencias de bytes.

Esto permite que un procesador o un SoC acceda a la memoria de imagen almacenada en la SRAM a través del mismo subsistema de memoria compartida.

## Operación típica del sistema

En un caso de uso normal de HMI, el flujo es el siguiente:

1. El anfitrión carga en la SRAM los recursos de imagen, las máscaras o los datos de configuración.
2. La TFT se inicializa a través del subsistema de pantalla.
3. Un procesador o un comando UART actualiza el valor de un objeto.
4. `command_arbiter_decoder` configura e inicia `mask_generator`.
5. `mask_generator` lee el área de imagen relevante, la modifica y la escribe de vuelta.
6. Se solicita a `screen_system` el rectángulo actualizado.
7. `tft_control_fsm` obtiene los píxeles de la memoria y los transmite a la TFT mediante `spi_master`.

Esta organización hace que el diseño sea eficiente para HMI en las que solo cambian pequeñas regiones de la pantalla a la vez.



## Placa Lacerta

La placa Lacerta integra en una sola PCB varios subsistemas: regulación de potencia, generación de reloj, interfaces de comunicación y conectividad de periféricos. La placa permite una interacción fluida entre una computadora anfitriona y el sistema embebido mediante una interfaz USB a serial, y admite además la programación externa mediante memoria Flash SPI.

En su núcleo, la placa aloja el SoC principal y expone señales esenciales como los GPIO, los rieles de alimentación y los buses de comunicación. Componentes adicionales, como un oscilador MEMS, proporcionan una temporización estable, mientras que los reguladores de voltaje garantizan una alimentación confiable. Los encabezados de pines accesibles permiten una expansión y pruebas flexibles, lo que hace que la plataforma sea adecuada tanto para prototipado como para uso educativo.

El sistema también admite salida gráfica para pantallas TFT/OLED basadas en SPI, lo que permite desarrollar interfaces de usuario por hardware en pantallas embebidas compactas. La depuración y el control se facilitan con LED integrados y un botón de reinicio, que ofrecen retroalimentación inmediata y gestión del sistema. En conjunto, la placa ofrece un entorno integrado para experimentación y evaluación de conectar y usar.


:::{figure} ../assets/img/PCB_UART.jpeg
:alt: Render 3D de la placa Lacerta
:align: center

**Figura 7.** Render 3D de la placa Lacerta, que ilustra la ubicación de los componentes y el diseño, incluyendo la colocación del chip Caravel/Lacerta, los reguladores de voltaje, la circuitería de generación de reloj, la interfaz de memoria Flash SPI, los encabezados GPIO y los conectores de periféricos, y ofrece una vista realista de la plataforma de hardware ensamblada.
:::



## Firmware

La plataforma Lacerta incluye una capa de firmware que puede ejecutarse directamente en el **procesador RISC-V integrado que proporciona el SoC Caravel**. Este firmware actúa como la capa de control responsable de gestionar la interfaz gráfica y de coordinar la interacción entre las entradas del sistema y el motor de renderizado por hardware de Lacerta.

El firmware que se ejecuta en el procesador RISC-V de Caravel se encarga de:

- recibir datos UART desde un anfitrión externo o una etapa de preprocesamiento  
- actualizar los elementos gráficos en memoria  
- configurar los parámetros de la interfaz  
- controlar el circuito de generación de pantalla a través del bus Wishbone  

Durante la operación, el procesador RISC-V lee los datos UART entrantes, aplica la lógica o el procesamiento matemático que se requiera y traduce esta información en actualizaciones gráficas. El procesador envía comandos a través de la **interfaz maestra Wishbone** al motor de pantalla de Lacerta, que escribe los datos gráficos correspondientes en la memoria del sistema.

El **controlador de salida de pantalla SPI** lee los datos gráficos almacenados en memoria y genera la señal que produce la imagen final en la pantalla.

Además de ejecutarse en el procesador integrado, el sistema Lacerta también puede interactuar con **microcontroladores externos**. En esta configuración, un controlador externo puede recopilar datos de sensores o realizar procesamiento adicional y luego transmitir la información relevante al sistema Caravel mediante **UART**.

Esta arquitectura permite que Lacerta opere en dos modos:

- **Modo directo**, en el que los datos UART se reenvían con latencia mínima para actualizar la interfaz gráfica.
- **Modo de procesamiento**, en el que los datos UART son manejados primero por el procesador RISC-V de Caravel antes de que los valores resultantes se envíen al motor de pantalla.

Al aprovechar el procesador RISC-V integrado y la interconexión Wishbone, el firmware ofrece un mecanismo flexible para controlar la interfaz gráfica sin perder el modelo de comunicación centrado en UART descrito para la plataforma.

## Software de diseño de interfaces

El cuarto componente principal de la arquitectura de Lacerta es el **software de diseño de interfaces**, que ofrece el entorno de cara al usuario para definir interfaces gráficas personalizadas.

El software permite crear interfaces personalizadas mediante un editor visual y exportar los archivos de configuración que usa el motor de hardware.

Con este editor visual, los usuarios pueden colocar y configurar elementos gráficos como botones, barras, indicadores numéricos y pantallas de estado. La herramienta permite diseñar la interfaz a alto nivel sin necesidad de implementar manualmente lógica gráfica de bajo nivel.

:::{figure} ../assets/img/Lacerta_GUI.jpg
:alt: Editor gráfico del software de diseño de interfaces de Lacerta
:align: center

**Figura 6.** Editor gráfico del software de diseño de interfaces de Lacerta, donde los usuarios pueden diseñar interfaces embebidas personalizadas organizando componentes gráficos como pantallas de siete segmentos, barras e indicadores.
:::

Una vez terminado el diseño, el software genera un archivo de configuración que describe la estructura y los parámetros de la interfaz. Este archivo se carga luego en el motor de hardware de Lacerta, lo que permite que el ASIC renderice directamente en hardware la interfaz deseada.

Al combinar estos cuatro componentes, Lacerta ofrece una plataforma completa y reproducible para HMI embebidas configurables, que abarca la creación de la interfaz, la implementación en silicio, el control en tiempo de ejecución y la integración física del sistema.
