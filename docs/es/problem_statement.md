# Planteamiento del problema

Los sistemas embebidos modernos requieren cada vez más interfaces gráficas para mostrar el estado del sistema, datos de sensores e información operativa de forma clara e intuitiva. A estas interfaces se les conoce comúnmente como **interfaces humano–máquina (HMI)**.

Una HMI es la interfaz que permite a un operador humano interactuar con una máquina, un sistema o un proceso, presentando información de forma visual y habilitando acciones de control. En entornos industriales, las HMI suelen mostrar datos en tiempo real, alarmas y estados del sistema, lo que permite a los operadores supervisar y controlar las máquinas de manera eficiente.

## ¿Qué es una HMI?

<iframe width="720" height="405" src="https://www.youtube.com/embed/kujHQgK352o" 
title="¿Qué es una HMI?" frameborder="0" allowfullscreen></iframe>

Las interfaces humano–máquina se usan ampliamente en automatización industrial, instrumentación, robótica, electrodomésticos inteligentes y muchas otras aplicaciones embebidas. Sirven como la **capa de comunicación entre las personas y las máquinas**, y traducen datos complejos del sistema en elementos visuales fáciles de interpretar y con los que es fácil interactuar.

Ejemplos de componentes visuales típicos de una HMI:

- Indicadores de estado  
- Pantallas numéricas  
- Barras gráficas  
- Alarmas y notificaciones  
- Botones e interruptores de control  

Mediante estos elementos, los operadores pueden monitorear el comportamiento de la máquina, analizar datos de sensores y ajustar parámetros del sistema en tiempo real.

## Retos en el desarrollo de HMI embebidas

A pesar de su importancia, implementar interfaces gráficas en sistemas embebidos sigue siendo un reto. La mayoría de las HMI embebidas se implementan hoy con software que corre en microcontroladores de propósito general o procesadores embebidos. Este enfoque suele requerir recursos de cómputo considerables y un firmware complejo para manejar:

- la generación de las señales de temporización de la pantalla
- el renderizado gráfico
- la comunicación con sensores y controladores
- el procesamiento de datos en tiempo real

En sistemas con recursos limitados, estas tareas compiten con la funcionalidad principal de la aplicación embebida, lo que aumenta la complejidad del firmware y reduce la eficiencia del sistema.

Otra limitación común es la falta de **plataformas de hardware flexibles y reutilizables** para construir interfaces personalizadas. Muchas soluciones comerciales de HMI dependen de ecosistemas propietarios o de módulos de pantalla fijos que limitan la personalización. Como resultado, los desarrolladores suelen tener que diseñar una nueva lógica de interfaz para cada proyecto.


## Necesidad de una plataforma de interfaz de hardware abierto

Una solución de hardware abierto y reutilizable, capaz de generar interfaces gráficas directamente en hardware, podría simplificar de forma significativa el desarrollo de HMI embebidas.

Una plataforma así permitiría a los desarrolladores:

- diseñar visualmente una interfaz personalizada
- conectar señales del mundo real al sistema
- renderizar elementos gráficos directamente en hardware
- reducir la complejidad del firmware
- acelerar el desarrollo de sistemas de monitoreo y control

Ofrecer una arquitectura abierta y reproducible para HMI embebidas puede acelerar el desarrollo de **dispositivos industriales, comerciales y de IoT en el borde**, y además hacer accesibles capacidades avanzadas de visualización a una comunidad de ingeniería más amplia.

## Usuarios objetivo

Lacerta está pensada para desarrolladores y organizaciones que necesitan construir **interfaces gráficas embebidas** de forma eficiente y con la menor complejidad de firmware posible. Al implementar el motor de renderizado de la interfaz directamente en hardware, Lacerta permite a los sistemas visualizar datos en tiempo real sin depender de marcos de software de pantalla complejos.

### Desarrolladores de sistemas embebidos

Los ingenieros que desarrollan dispositivos embebidos pueden usar Lacerta para crear tableros gráficos que muestren lecturas de sensores, estados del sistema o parámetros operativos. El motor de renderizado por hardware descarga el procesamiento gráfico del procesador principal, lo que simplifica el desarrollo del firmware y mejora el desempeño del sistema.

### Ingenieros de automatización industrial

Los sistemas industriales suelen requerir paneles de monitoreo visual para mostrar el estado de las máquinas, variables de proceso, alarmas y métricas operativas. Lacerta ofrece una plataforma de bajo costo para implementar interfaces humano–máquina personalizadas en sistemas de monitoreo y control industrial.

### Diseñadores de dispositivos IoT y de borde

Los dispositivos de borde suelen recopilar datos de sensores distribuidos y necesitan capacidades sencillas de visualización local. Lacerta permite desarrollar tableros personalizables que presentan información de sensores en tiempo real en aplicaciones como monitoreo ambiental, infraestructura inteligente y dispositivos conectados.

### Desarrolladores de producto y startups de hardware

Los equipos de desarrollo de producto pueden usar Lacerta para acelerar la creación de interfaces gráficas embebidas para dispositivos electrónicos. Al reducir la necesidad de firmware de pantalla complejo, Lacerta acorta los ciclos de desarrollo y simplifica la integración del sistema.

### Investigadores y educadores

Lacerta también sirve como plataforma educativa para explorar el diseño digital, los sistemas embebidos y el desarrollo de interfaces humano–máquina con herramientas de hardware abierto y flujos de diseño de ASIC reproducibles.
