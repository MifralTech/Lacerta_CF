:::{image} ../assets/img/Logo_Black_background_white.svg
:alt: Logotipo de Mifral
:width: 220px
:align: center
:::

# Lacerta: motor de interfaz de hardware abierto para sistemas embebidos

![Logotipo de Lacerta](../assets/img/Lacerta2.png)

## Descripción del proyecto

**Lacerta** es una plataforma de hardware de código abierto que permite crear con rapidez interfaces gráficas para sistemas embebidos.

El sistema permite a los desarrolladores diseñar interfaces gráficas con una herramienta de configuración gráfica y desplegarlas directamente en hardware, implementado en un ASIC a medida integrado en la plataforma SoC Caravel. El hardware genera la interfaz en tiempo real y envía el resultado a las pantallas TFT/OLED con interfaz SPI que se usan comúnmente en dispositivos embebidos.

La interfaz generada puede incluir componentes visuales como:

- Botones
- Barras horizontales y verticales
- Indicadores numéricos
- Indicadores de estado

:::{figure} ../assets/img/sample_icons.jpg
:alt: Ejemplos de componentes gráficos que admite Lacerta
:align: center

**Figura 1.** Ejemplos de componentes gráficos que admite Lacerta, entre ellos botones, barras horizontales y verticales, indicadores numéricos, gráficas e indicadores de estado, usados para visualizar datos del sistema en tiempo real.
:::

El ASIC recibe información mediante flujos UART y admite dos modos principales de operación para actualizar la pantalla:

1. **Modo directo:** los datos recibidos por UART se envían directamente al área de proyecto de usuario. En este modo los valores se actualizan en la pantalla TFT/OLED SPI con latencia mínima, ideal para actualizaciones sencillas o críticas en tiempo.

2. **Modo de procesamiento:** los datos de la UART se enrutan primero al núcleo RISC-V integrado, donde se puede aplicar cualquier operación matemática, función o lógica personalizada. Tras el procesamiento, los resultados se envían al área de proyecto de usuario para actualizar la pantalla. Este modo es adecuado para aplicaciones que requieren manipular los datos o una lógica de interfaz más compleja.

Esta arquitectura flexible permite a Lacerta gestionar de forma eficiente múltiples entradas y objetos en pantalla con un único protocolo UART, y adaptarse tanto a casos de uso sencillos como avanzados. Cualquier otro tipo de señal debe convertirse a UART de antemano mediante circuitería de interfaz externa o dispositivos de preprocesamiento.

:::{figure} ../assets/img/flow_sensor_lacertav2.png
:alt: Concepto del sistema Lacerta
:align: center

**Figura 2.** Concepto del sistema Lacerta: el ASIC Lacerta procesa las señales para generar la HMI gráfica personalizada que se muestra en pantallas TFT/OLED con interfaz SPI, pensada para instalaciones embebidas compactas.
:::

El objetivo de Lacerta es ofrecer una arquitectura de referencia de bajo costo y totalmente de código abierto para interfaces humano–máquina (HMI) embebidas. Al combinar la generación de gráficos configurable por hardware con interfaces de entrada flexibles, Lacerta permite el desarrollo rápido de tableros y sistemas de monitoreo personalizables para aplicaciones industriales, comerciales y de IoT en el borde.


```{toctree}
:hidden:
:caption: Introducción
:maxdepth: 1

problem_statement
proposed_solution
```

```{toctree}
:hidden:
:caption: Sistema
:maxdepth: 1

system_architecture
system_development
```

```{toctree}
:hidden:
:caption: Recursos
:maxdepth: 1

lacerta_gui_fpga_demo
appendix
authors
```
