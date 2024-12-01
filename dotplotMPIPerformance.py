from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt
import time
from Bio import SeqIO
import numpy as np
# Diccionario de mapeo
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

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


# Estas secuencias se deben reemplazar con las que ingresan por FASTA
Secuencia1 = secuencia1_array
Secuencia2 = secuencia2_array

# # Generar las secuencias mapeadas
# Secuencia1 = np.array([nucleotide_map[char] for char in "ACGTCGTCGAGCTAGCATCGATCAGNNNCATCATCNACTATACNNNNCATCATCATCTACTGCTACGACTACGAGAGAGCTACGACTACG" * cant_muestras], dtype=np.uint8)
# Secuencia2 = np.array([nucleotide_map[char] for char in "NGCNATCACGATGCATGCACTACGATCGACAGCATCGATCGATGCATCATGCATCGNATGCNTGASCSATCGACGTANGCACTGACNTGA" * cant_muestras], dtype=np.uint8)

# Dividir índices en chunks para cada proceso
chunks = np.array_split(range(len(Secuencia1)), size)
local_chunk = chunks[rank]

print(f"El proceso {rank} tiene {len(chunks[rank])} elementos")

# Crear matriz dotplot local
dotplot_local = np.zeros((len(local_chunk), len(Secuencia2)), dtype=np.uint8)

# Generar el dotplot local
for i, idx in enumerate(local_chunk):
    for j in range(len(Secuencia2)):
        dotplot_local[i, j] = 1 if Secuencia1[idx] == Secuencia2[j] else 0

# Reunir resultados en el proceso root
dotplot = comm.gather(dotplot_local, root=0)

if rank == 0:
    # Combinar los resultados en una sola matriz
    merged_data = np.vstack(dotplot)

    plt.figure(figsize=(5, 5))
    plt.imshow(merged_data, cmap='Greys', aspect='auto')
    plt.ylabel("Secuencia 1")
    plt.xlabel("Secuencia 2")
    plt.savefig("dotplot_mpi4py.svg")
