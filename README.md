# HPC-FINAL: Análisis de Rendimiento de Dotplot Secuencial vs. Paralelización

## Descripción del Proyecto

El objetivo de este proyecto es implementar y analizar el rendimiento de tres formas de realizar un dotplot, una técnica comúnmente utilizada en bioinformática para comparar secuencias de ADN o proteínas. Se desarrolló un proyecto en Jupyter Notebook llamado **`proyectoFinal_HPC_Entregable.ipynb`** que explora estas variantes de implementación:

1. **Implementación Secuencial**: Un único hilo de ejecución.
2. **Paralelización con `multiprocessing`**: Uso de múltiples procesos en el mismo nodo.
3. **Paralelización con `mpi4py`**: Distribución de la tarea entre múltiples nodos y procesos usando MPI.

Se compararon estas implementaciones en base a métricas de rendimiento y se visualizan los resultados en gráficos.

## Requisitos del Proyecto

### Implementación de la Aplicación

Se creó una aplicación de línea de comandos que permite generar un dotplot entre dos secuencias en formato FASTA y ejecutar el análisis de tres formas diferentes. La aplicación debe ser capaz de ejecutarse como se describe a continuación.

### Análisis de Rendimiento

El análisis de rendimiento incluye el cálculo de las siguientes métricas para cada implementación:

1. Tiempos de ejecución totales y parciales (porciones paralelizables).
2. Tiempo de carga de los datos y generación de la imagen.
3. Tiempo muerto (tiempo no empleado en la ejecución).
4. Aceleración y eficiencia.
5. Escalabilidad.

Se comparan el rendimiento, la aceleración, la eficiencia y la escalabilidad de las tres implementaciones.

## Requisitos Previos

Este proyecto fue desarrollado en un entorno de Python 3.8 y usa las bibliotecas necesarias para el procesamiento paralelo. Las dependencias incluyen:

- `numpy`
- `matplotlib`
- `biopython`
- `mpi4py`

Además, se utilizan las siguientes herramientas de soporte:

- **Jupyter Notebook** para la presentación y análisis interactivo de los datos.

### Instalación de Dependencias

Recomendamos utilizar un entorno de Anaconda para la instalación de las dependencias. Para crear y activar el entorno, ejecuta:

```bash
conda create -n HPC_FINAL python=3.8
conda activate HPC_FINAL
conda install -c conda-forge biopython
conda install -c anaconda numpy
conda install -c conda-forge matplotlib
conda install -c anaconda mpi4p
conda install -c bioconda mashmap
conda install -c bioconda ragtag
```


### Uso
El proyecto incluye un archivo Jupyter Notebook llamado proyectoFinal_HPC_Entregable.ipynb. Este archivo contiene el código para ejecutar las pruebas de rendimiento y generar los gráficos.
Para la ejecución del notebook se puede ejecutar el siguiente comando: 

```bash
jupyter notebook proyectoFinal_HPC_Entregable.ipynb
```
En el notebook se incluyen ejecuciones directas que trabajan con los archivos generados para la ejecución utilizando el método MPI. Si se desea ejecutar el proyecto desde la línea de comandos, se puede hacer de la siguiente manera:
```bash
mpirun --allow-run-as-root -n 6 python dotplotMPISCLWeak.py
```
Es importante destacar que, independientemente de la variante de implementación utilizada, se genera un Dotplot de dimensiones superiores a 136.000 x 136.000. Sin embargo, por razones de limitaciones computacionales, se optó por trabajar con una matriz de 20.000 x 20.000 para realizar los análisis de manera rápida y eficiente. La variable involucrada para modificar ese tamaño se llama `batch`


