# Apéndice

Este apéndice conserva, como referencia y con fines educativos, un enfoque de implementación anterior de Lacerta.

## Primer enfoque de Lacerta

En esta sección se encuentra el primer enfoque considerado para Lacerta:

- una estrategia de implementación con **hardening jerárquico**,
- y un **enfoque basado en VGA** para el subsistema de pantalla.

Estas alternativas formaron parte de la fase inicial de exploración del diseño y ayudaron a definir la dirección final del sistema.

## Por qué se descartó este enfoque

Aunque el enfoque de hardening jerárquico y VGA fue técnicamente valioso durante el desarrollo, se descartó finalmente por las **limitaciones de pines de E/S** del entorno de integración objetivo.

La implementación orientada a VGA requería más recursos de interfaz externa de los que resultaban prácticos dentro de las restricciones de pads e integración disponibles. Por ello, el proyecto avanzó hacia el enfoque actual, que se ajusta mejor a los límites del envoltorio de proyecto de usuario de Caravel.

## Por qué se conserva en el apéndice

Este material se mantiene en el apéndice porque aporta contexto útil sobre:

- las primeras decisiones de arquitectura de Lacerta,
- las compensaciones al elegir una estrategia de hardening,
- y el valor educativo de comprender un flujo de **hardening jerárquico**.

Aunque este camino no se eligió para la implementación final, sigue siendo una referencia útil para quienes quieran estudiar estrategias de integración alternativas y aprender de la evolución del proyecto.



## Layout de Lacerta

La implementación física de **Lacerta** se ha ejercitado activamente a lo largo del desarrollo. La mayoría de los módulos RTL ya se han sintetizado, colocado y enrutado con el flujo completo RTL a GDSII, lo que permitió identificar de forma temprana retos de integración, temporización y enrutamiento.

Las vistas de layout y las métricas de diseño resultantes se documentan en la subsección siguiente. Estos resultados han sido fundamentales para iterar aspectos clave del diseño físico, como:

- Estrategias de floorplanning  
- Inserción y optimización de buffers  
- Distribución de reloj y de reinicio  

Este enfoque iterativo ha mejorado de manera notable el cierre de temporización y la robustez general del diseño.

Para agilizar la integración y simplificar el cierre de temporización, Lacerta adopta una **estrategia de implementación física mixta**:

- **Bloques aplanados (hardened)** para la lógica de control e interfaz más pequeña  
- **Macros preverificadas** para los módulos de ruta de datos más grandes y críticos en temporización  


Estos módulos se fusionarán en el nivel superior durante la implementación física:

- `wb_slave_memory_mapped`  
- `wb_slave_to_mem_sys_ports`  
- `command_arbiter_decoder`  

Estos módulos permanecerán como bloques independientes ya implementados:

- `mask_generator`  
- **Subsistema de memoria** (`mem_sys`, buffers)  
  - Conserva los generadores de registros y de patrones ya validados  
- **Controlador VGA y UART**  
  - Reutilización de lógica de temporización y de E/S ya validada  

### WB Slave to Memory Mapped

:::{image} ../assets/img/layout_gds/wb_mem_map.png
:width: 49%
:class: lacerta-half
:::
:::{image} ../assets/img/layout_gds/wb_mem_map_wires.png
:width: 49%
:class: lacerta-half
:::

:::{container} lacerta-caption
*Layout del esclavo Wishbone (WB) mapeado en memoria. La imagen de la izquierda muestra la colocación de celdas sin capas de metal y resalta la estructura subyacente de celdas estándar; la de la derecha incluye el enrutamiento de metal e ilustra las interconexiones y el cableado de señales del diseño.*
:::

| Métrica                    | Valor               | Notas |
|---------------------------|---------------------:|-------|
| Tecnología                | SKY130A              | PDK abierto (config pdk::sky130*) |
| Área del núcleo           | 0.131454 mm²         | design__core__area = 131454 µm² |
| Área del die              | 0.144400 mm²         | design__die__area = 144400 µm² |
| Utilización               | 10.86%               | design__instance__utilization = 0.108612 |
| Cantidad de celdas estándar | 3,575              | design__instance__count__stdcell |
| Cantidad de celdas secuenciales | 137            | Elementos secuenciales         |
| Completitud del enrutamiento | 100%              | enrutamiento completo (sin redes sin enrutar) |
| Peor holgura negativa     | 0.00 ns              | timing__setup__wns = 0.0 |
| Holgura negativa total    | 0.00 ns              | timing__setup__tns = 0.0 |
| Frecuencia máxima         | 100 MHz (objetivo)   | CLOCK_PERIOD = 10 ns |
| Potencia total            | 1.531 mW             | power__total reportada = 0.00153094 W |
| Violaciones de DRC        | 0                    | sin errores de DRC reportados |
| LVS                       | Aprobado             | coincidencia entre layout y netlist |
| Violaciones de antena     | 2                    | antenna__violating__nets = 2 |
| GDS generado              | Sí                   | final |

### WB Slave to Read/Write Ports

:::{image} ../assets/img/layout_gds/mem_port.png
:width: 49%
:class: lacerta-half
:::
:::{image} ../assets/img/layout_gds/mem_port_wire.png
:width: 49%
:class: lacerta-half
:::

:::{container} lacerta-caption
*Layout del esclavo Wishbone (WB) a puertos de lectura/escritura. La imagen de la izquierda muestra la colocación de celdas sin capas de metal y resalta la estructura subyacente de celdas estándar; la de la derecha incluye el enrutamiento de metal e ilustra las interconexiones y el cableado de señales del diseño.*
:::

| Métrica                  | Valor            | Notas                          |
|--------------------------|------------------|--------------------------------|
| Tecnología               | SKY130A          | PDK abierto (config pdk::sky130*) |
| Área del núcleo          | 0.131 mm²        | De 131,454 µm²                 |
| Área del die             | 0.144 mm²        | De 144,400 µm²                 |
| Utilización              | 7.19%            | Densidad de celdas estándar    |
| Cantidad de celdas estándar | 2,898         | Cantidad de instancias         |
| Cantidad de celdas secuenciales | 71        | Elementos secuenciales         |
| Completitud del enrutamiento | 100%         | Sin redes sin enrutar          |
| Peor holgura negativa    | 0.00 ns          | Temporización cumplida (sin violaciones) |
| Holgura negativa total   | 0.00 ns          | Sin violaciones                |
| Frecuencia máxima        | 100 MHz (objetivo) | CLOCK_PERIOD = 10 ns |
| Potencia total           | 0.934 mW         | Dinámica + fuga                |
| Violaciones de DRC       | 0                | Magic + KLayout sin errores    |
| LVS                      | Aprobado         | Sin errores reportados         |
| Violaciones de antena    | 3                | Del reporte de enrutamiento    |
| GDS generado             | Sí               | Implícito por el flujo completado |


### Controlador VGA

:::{image} ../assets/img/layout_gds/VGA.png
:width: 49%
:class: lacerta-half
:::
:::{image} ../assets/img/layout_gds/vga_wire.png
:width: 49%
:class: lacerta-half
:::

:::{container} lacerta-caption
*Layout del controlador VGA. La imagen de la izquierda muestra la colocación de celdas sin capas de metal y resalta la estructura subyacente de celdas estándar; la de la derecha incluye el enrutamiento de metal e ilustra las interconexiones y el cableado de señales del diseño.*
:::


| Métrica                  | Valor            | Notas                          |
|--------------------------|------------------|--------------------------------|
| Tecnología               | SKY130A          | PDK abierto (config pdk::sky130*) |
| Área del núcleo          | 0.0333 mm²       | De 33,344.5 µm²                |
| Área del die             | 0.0400 mm²       | De 40,000 µm²                  |
| Utilización              | 16.77%           | Utilización de celdas estándar |
| Cantidad de celdas estándar | 1,179         | Instancias de celdas estándar  |
| Cantidad de celdas secuenciales | 24        | Elementos secuenciales         |
| Completitud del enrutamiento | 100%         | Sin errores de DRC de enrutamiento |
| Peor holgura negativa    | -0.95 ns         | Violación de temporización (peor caso) en la esquina max_ss_100C_1v60 |
| Holgura negativa total   | -2.61 ns         | Hay violaciones de setup en la esquina max_ss_100C_1v60 |
| Frecuencia máxima        | 100 MHz          | Estimada a partir de ~2.2 ns de holgura |
| Potencia total           | 0.486 mW         | Dinámica + fuga                |
| Violaciones de DRC       | 0                | Magic + KLayout sin errores    |
| LVS                      | Aprobado         | Sin errores de LVS             |
| Violaciones de antena    | 0                | Sin errores                    |
| GDS generado             | Sí               | Flujo completado correctamente |

### Decodificador de arbitraje de comandos

:::{image} ../assets/img/layout_gds/arbiter.png
:width: 49%
:class: lacerta-half
:::
:::{image} ../assets/img/layout_gds/arbiterwire.png
:width: 49%
:class: lacerta-half
:::

:::{container} lacerta-caption
*Layout del decodificador de arbitraje de comandos. La imagen de la izquierda muestra la colocación de celdas sin capas de metal y resalta la estructura subyacente de celdas estándar; la de la derecha incluye el enrutamiento de metal e ilustra las interconexiones y el cableado de señales del diseño.*
:::


| Métrica                  | Valor            | Notas                          |
|--------------------------|------------------|--------------------------------|
| Tecnología               | SKY130A          | PDK abierto (config pdk::sky130*) |
| Área del núcleo          | 0.1315 mm²       | De 131,454 µm²                 |
| Área del die             | 0.1444 mm²       | De 144,400 µm²                 |
| Utilización              | 7.19%            | Utilización de celdas estándar |
| Cantidad de celdas estándar | 2,898         | Instancias de celdas estándar  |
| Cantidad de celdas secuenciales | 64        | Elementos secuenciales         |
| Completitud del enrutamiento | 100%         | Sin redes sin enrutar          |
| Peor holgura negativa    | 0.00 ns          | Temporización cumplida         |
| Holgura negativa total   | 0.00 ns          | Sin violaciones                |
| Frecuencia máxima        | ~208 MHz         | Estimada a partir de ~4.8 ns de holgura |
| Potencia total           | 0.934 mW         | Dinámica + fuga                |
| Violaciones de DRC       | 0                | Magic + KLayout sin errores    |
| LVS                      | Aprobado         | Sin errores de LVS             |
| Violaciones de antena    | 3                | Hay violaciones menores        |
| GDS generado             | Sí               | Flujo completado correctamente |

### Generador de máscaras

:::{image} ../assets/img/layout_gds/mask.png
:width: 49%
:class: lacerta-half
:::
:::{image} ../assets/img/layout_gds/maskwire.png
:width: 49%
:class: lacerta-half
:::

:::{container} lacerta-caption
*Layout del generador de máscaras. La imagen de la izquierda muestra la colocación de celdas sin capas de metal y resalta la estructura subyacente de celdas estándar; la de la derecha incluye el enrutamiento de metal e ilustra las interconexiones y el cableado de señales del diseño.*
:::


| Métrica               | Valor             | Notas                            |
| --------------------- | ----------------- | -------------------------------- |
| Tecnología            | SKY130A           | PDK abierto (config pdk::sky130*)|
| Área del núcleo       | 0.131 mm²         | De 131,454 µm²                   |
| Área del die          | 0.144 mm²         | De 144,400 µm²                   |
| Utilización           | 39.20%            | De 0.392 (utilización de celdas estándar) |
| Cantidad de celdas estándar | 7,471       | Instancias de celdas estándar    |
| Cantidad de celdas secuenciales | 599     | Celdas secuenciales              |
| Completitud del enrutamiento | 100%       | route__drc_errors = 0            |
| Peor holgura negativa | -0.36 ns          | timing__setup__wns               |
| Holgura negativa total | -9.20 ns         | timing__setup__tns               |
| Frecuencia máxima     | ~100 MHz (objetivo) | CLOCK_PERIOD ≈ 10 ns (dado)    |
| Potencia total        | 9.70 mW           | power__total (0.0097 W)          |
| Violaciones de DRC    | 0                 | Magic + KLayout sin errores      |
| LVS                   | Aprobado          | Sin errores de LVS               |
| Violaciones de antena | 1                 | route__antenna_violation__count  |
| GDS generado          | Sí                | Flujo completado                 |

### Sistema de memoria
🚧 Contenido próximamente.

### UART

:::{image} ../assets/img/layout_gds/UART.png
:width: 49%
:class: lacerta-half
:::
:::{image} ../assets/img/layout_gds/UARTIRE.png
:width: 49%
:class: lacerta-half
:::

:::{container} lacerta-caption
*Layout de la UART. La imagen de la izquierda muestra la colocación de celdas sin capas de metal y resalta la estructura subyacente de celdas estándar; la de la derecha incluye el enrutamiento de metal e ilustra las interconexiones y el cableado de señales del diseño.*
:::


| Métrica               | Valor             | Notas                                     |
| --------------------- | ----------------- | ----------------------------------------- |
| Tecnología            | SKY130A           | PDK abierto (config pdk::sky130*)         |
| Área del núcleo       | 0.0801 mm²        | De 80,146.9 µm²                           |
| Área del die          | 0.0900 mm²        | De 90,000 µm²                             |
| Utilización           | 26.86%            | De 0.2686 (utilización de celdas estándar)|
| Cantidad de celdas estándar | 3,331       | design__instance__count                   |
| Cantidad de celdas secuenciales | 278     | design__instance__count__class:sequential |
| Completitud del enrutamiento | 100%       | route__drc_errors = 0                     |
| Peor holgura negativa | 0.00 ns           | timing__setup__wns                        |
| Holgura negativa total | 0.00 ns          | timing__setup__tns                        |
| Frecuencia máxima     | ~100 MHz (objetivo) | CLOCK_PERIOD ≈ 10 ns                    |
| Potencia total        | 2.66 mW           | power__total (0.00266 W)                  |
| Violaciones de DRC    | 0                 | Magic + KLayout sin errores               |
| LVS                   | Aprobado          | Sin errores de LVS (asumido por el flujo sin errores) |
| Violaciones de antena | 1                 | route__antenna_violation__count           |
| GDS generado          | Sí                | Flujo completado                          |
