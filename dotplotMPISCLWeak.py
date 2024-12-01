from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt
import time
from Bio import SeqIO

begin_data = time.time()

nucleotide_map = {'A': 0, 'C': 1, 'G': 2, 'T': 3, 'N' : 4}

batch = 20000 # se reduce el tamano de la informacion por limitacion computacional

# Función para leer las secuencias desde archivos FASTA
def cargar_secuencias(fasta_file):
    secuencias = []
    for record in SeqIO.parse(fasta_file, "fasta"):
        # mapear la secuencia
        mapped_seq = [nucleotide_map[nuc] for nuc in str(record.seq)]  # Mapear cada letra
        secuencias.append(mapped_seq)
    return secuencias[0]

# Ejemplo de cómo usar la función
fasta_file1 = "elemento1.fasta"  # Ruta al archivo FASTA de la primera secuencia
fasta_file2 = "elemento2.fasta"  # Ruta al archivo FASTA de la segunda secuencia

Secuencia1, Secuencia2 = cargar_secuencias(fasta_file1), cargar_secuencias(fasta_file2)

Secuencia1 = Secuencia1[:batch]
Secuencia2 = Secuencia2[:batch]

#Tomo el valor del vector
secuencia1_array = np.array(Secuencia1, dtype=np.uint8)
secuencia2_array = np.array(Secuencia2, dtype=np.uint8)
#Imprimir la longitud de las secuencias


end_data =  time.time()
 
print(f"\n La carga de información tardó: {end_data-begin_data} segundos")



begin = time.time()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#[TEST] Definimos unas secuencias
# Estas secuencias se deben reemplazar con las que ingresan por FASTA
# cant_muestras = 150
# Secuencia1 = "ACGTCGTCGAGCTAGCATCGATCAGNNNCATCATCNACTATACNNNNCATCATCATCTACTGCTACGACTACGAGAGAGCTACGACTACG"*cant_muestras
# Secuencia2 = "NGCNATCACGATGCATGCACTACGATCGACAGCATCGATCGATGCATCATGCATCGNATGCNTGASCSATCGACGTANGCACTGACNTGA"*cant_muestras
# Estas secuencias se deben reemplazar con las que ingresan por FASTA
Secuencia1 = secuencia1_array
Secuencia2 = secuencia2_array


#Escalamiento Débil
Secuencia2Aux = Secuencia2[:len(Secuencia2)*size]  # Incrementa el tamaño de la secuencia.

# Dividir la secuencia1 en chunks, uno por cada proceso.
chunks = np.array_split(range(len(Secuencia1)), size)
print(f"El proceso {rank} tiene {len(chunks[rank])} elementos")


dotplot = np.empty([len(chunks[rank]),len(Secuencia2Aux)],dtype=np.uint8)

for i in range(len(chunks[rank])):
    for j in range(len(Secuencia2Aux)):
        if Secuencia1[chunks[rank][i]] == Secuencia2Aux[j]:
            dotplot[i,j] = np.uint8(1)
        else:
            dotplot[i,j] = np.uint8(0)

# gather data from all processes onto the root process
dotplot = comm.gather(dotplot, root=0)

# The root process prints the results and generates the plot.
if rank == 0:
    #print("La matriz de resultado tiene tamaño: ", dotplot.shape)

    # merge the gathered data into a single array
    merged_data = np.vstack(dotplot)


    end = time.time()
