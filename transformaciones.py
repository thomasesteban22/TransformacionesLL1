# Función para leer la gramática desde un archivo .txt
def leer_gramatica(archivo):
    producciones = {}
    try:
        with open(archivo, 'r') as file:
            for linea in file:
                if '->' in linea:
                    # Separar el no terminal de las producciones
                    lado_izquierdo, lado_derecho = linea.split('->')
                    lado_izquierdo = lado_izquierdo.strip()
                    producciones[lado_izquierdo] = [prod.strip() for prod in lado_derecho.split('|')]
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo {archivo} no se encuentra. Verifica el nombre y la ruta.")
    except Exception as e:
        raise Exception(f"Ocurrió un error al leer el archivo: {e}")

    return producciones


# Función para calcular el conjunto de primeros (First) de un símbolo
def first(symbol, productions, firsts):
    try:
        if symbol in firsts:
            return firsts[symbol]

        first_set = set()

        if symbol.islower():  # Si es un terminal
            first_set.add(symbol)
        else:
            for production in productions[symbol]:
                for char in production:
                    if char == symbol:  # Evitar bucles de recursión directa
                        break
                    char_first = first(char, productions, firsts)
                    first_set.update(char_first - {'ε'})
                    if 'ε' not in char_first:
                        break
                else:
                    first_set.add('ε')

        firsts[symbol] = first_set
        return first_set
    except KeyError as e:
        raise KeyError(f"El símbolo {e} no está definido en las producciones.")
    except Exception as e:
        raise Exception(f"Ocurrió un error al calcular el conjunto First: {e}")


# Función para comprobar si hay recursividad por la izquierda
def has_left_recursion(productions):
    problematic = []
    try:
        for non_terminal in productions:
            for production in productions[non_terminal]:
                if production[0] == non_terminal:
                    problematic.append(non_terminal)
        return problematic if problematic else None
    except Exception as e:
        raise Exception(f"Error al comprobar la recursividad por la izquierda: {e}")


# Función para comprobar si hay factores comunes por la izquierda
def has_common_prefix(productions):
    problematic = []
    try:
        for non_terminal in productions:
            prefixes = set()
            for production in productions[non_terminal]:
                if production[0] in prefixes:
                    problematic.append(non_terminal)
                    break
                prefixes.add(production[0])
        return problematic if problematic else None
    except Exception as e:
        raise Exception(f"Error al comprobar factores comunes: {e}")


# Función principal que verifica si una gramática es LL(1)
def is_ll1_grammar(productions):
    try:
        firsts = {}

        # Comprobar recursividad por la izquierda
        left_recursion = has_left_recursion(productions)
        if left_recursion:
            return False, f"La gramática tiene recursividad por la izquierda en los no terminales: {', '.join(left_recursion)}."

        # Comprobar factores comunes por la izquierda
        common_prefix = has_common_prefix(productions)
        if common_prefix:
            return False, f"La gramática tiene factores comunes por la izquierda en los no terminales: {', '.join(common_prefix)}."

        return True, "La gramática es LL(1)."
    except Exception as e:
        raise Exception(f"Error al verificar si la gramática es LL(1): {e}")


# Ejemplo de uso leyendo la gramática desde un archivo .txt
def main():
    archivo = 'gramatica.txt'  # Nombre del archivo
    try:
        producciones = leer_gramatica(archivo)
        is_ll1, message = is_ll1_grammar(producciones)
        print(message)
    except Exception as e:
        print(f"Ocurrió un error: {e}")


if __name__ == "__main__":
    main()
