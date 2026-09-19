# Solución propuesta

Lacerta propone una plataforma de hardware abierto diseñada para simplificar la creación de interfaces gráficas para sistemas embebidos, trasladando el proceso de generación de la interfaz del software a hardware dedicado. La plataforma introduce un motor de renderizado de interfaz configurable, implementado como un ASIC a medida e integrado en el área de proyecto de usuario de Caravel SoC.

En lugar de exigir a los desarrolladores que programen manualmente interfaces gráficas complejas en el firmware, Lacerta permite **diseñar la interfaz de forma visual con una herramienta de configuración gráfica**. Esta herramienta permite colocar elementos gráficos como botones, barras, indicadores numéricos y pantallas de estado dentro de un diseño virtual que representa la interfaz final.

Una vez diseñada la interfaz, la configuración se exporta como un archivo de descripción. Esta configuración se transmite después al motor de hardware de Lacerta mediante la **interfaz UART**, lo que permite configurar y actualizar el ASIC fácilmente desde cualquier sistema anfitrión compatible. El ASIC interpreta la configuración y genera la salida gráfica en tiempo real.

## Renderizado de la interfaz en hardware

El ASIC de Lacerta incluye un motor de renderizado por hardware capaz de generar componentes de interfaz gráfica directamente en hardware. Este enfoque reduce de forma significativa la carga de cómputo que normalmente recae sobre los procesadores embebidos.

Al implementar la lógica de generación de la interfaz en hardware dedicado, Lacerta ofrece varias ventajas:

- renderizado gráfico determinista
- menor complejidad del firmware
- menor utilización del procesador
- mejor capacidad de respuesta del sistema
- integración simplificada con sistemas embebidos basados en UART

La interfaz generada se transmite a una pantalla mediante una **salida SPI TFT/OLED**, lo que permite al sistema manejar las pantallas embebidas compactas comunes en dispositivos modernos, sin requerir procesadores gráficos externos.

## Integración con sistemas embebidos

Lacerta está diseñada para recibir datos mediante una **interfaz UART**, lo que permite visualizar información real del sistema a través de la interfaz gráfica.

En su arquitectura actual, Lacerta no adquiere directamente señales analógicas ni señales digitales heterogéneas. En su lugar, los datos necesarios deben formatearse como mensajes UART mediante un microcontrolador externo, una etapa de preprocesamiento o un circuito de interfaz antes de enviarse al ASIC.

Una vez recibidos por UART, el motor de interfaz de Lacerta interpreta los datos y los asocia a elementos gráficos como barras o indicadores numéricos, lo que permite la visualización en tiempo real de los parámetros del sistema.

:::{figure} ../assets/img/flow_inputs.png
:alt: Ejemplo de datos del sistema adaptados a mensajes UART
:align: center

**Figura 3.** Ejemplo de datos del sistema adaptados a mensajes UART antes de llegar a la plataforma Lacerta, donde el motor de interfaz actualiza los elementos gráficos en tiempo real.
:::

## Flujo de trabajo de diseño de la interfaz

La plataforma Lacerta introduce un flujo de trabajo simplificado para crear interfaces gráficas embebidas:

1. **Diseño de la interfaz**  
   Una herramienta de diseño gráfico permite crear un diseño de interfaz personalizado con componentes visuales predefinidos.

2. **Generación de la configuración**  
   La herramienta exporta un archivo de configuración que describe la estructura de la interfaz y los parámetros de los elementos gráficos.

3. **Despliegue en hardware mediante UART**  
   La configuración se envía al motor de hardware de Lacerta a través de la interfaz UART, lo que permite configurar el ASIC de forma fácil y flexible.

4. **Visualización en tiempo de ejecución**  
   Los datos UART entrantes actualizan dinámicamente los elementos gráficos que renderiza el hardware. Si el origen no es UART, la circuitería externa o el firmware deben convertirlo antes.

Este flujo de trabajo permite a los desarrolladores diseñar interfaces complejas sin escribir un firmware extenso de control de pantalla.

:::{figure} ../assets/img/Flow_interfacev2.png
:alt: Flujo de creación de interfaces de Lacerta
:align: center

**Figura 4.** Flujo de creación de interfaces de Lacerta. Un editor gráfico se usa para diseñar diseños de interfaz personalizados, que se traducen a datos de configuración y se transmiten por UART al motor de hardware de Lacerta para generar la pantalla gráfica.
:::


## Arquitectura abierta y reproducible

Lacerta está concebida como una **arquitectura de referencia totalmente de código abierto**. El proyecto incluye todos los artefactos de diseño necesarios para reproducir el sistema, entre ellos:

- Documentación (este sitio)
- [Código fuente RTL de la implementación del ASIC](https://github.com/MifralTech/Lacerta_CF/tree/main/verilog/rtl)
- [Integración del flujo de diseño físico con Librelane](https://github.com/MifralTech/Lacerta_CF/tree/main/openlane)  
<!--- [Verification testbenches]()  -->
- [Archivos de diseño de la PCB](https://github.com/MifralTech/Lacerta_CF/tree/main/PCB)
- [Ejemplos de firmware](https://github.com/chipfoundry/caravel_board)  
- [Herramientas de diseño de interfaces](https://github.com/MifralTech/Lacerta_CF/tree/main/Interface_Design_Software)

Al ofrecer una plataforma abierta y reproducible, Lacerta permite a desarrolladores, investigadores y educadores construir interfaces humano–máquina embebidas personalizables para aplicaciones industriales, comerciales y de IoT en el borde.
