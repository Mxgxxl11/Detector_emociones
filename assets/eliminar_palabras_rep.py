"""
Este archivo contiene funciones para eliminar palabras repetidas de un archivo txt
"""

# Abre el archivo en modo lectura
with open('assets/palabras_eliminar.txt', 'r', encoding='utf-8') as file:
    # Lee todas las líneas del archivo
    palabras = file.readlines()

# Elimina los saltos de línea y espacios en blanco
palabras = [palabra.strip() for palabra in palabras]

# Usa un conjunto para eliminar duplicados
palabras_unicas = list(set(palabras))

# Abre el archivo en modo escritura para guardar las palabras únicas
with open('assets/palabras_eliminar.txt', 'w', encoding='utf-8') as file:
    for palabra in palabras_unicas:
        file.write(palabra + '\n')

print("Las palabras duplicadas han sido eliminadas.")
