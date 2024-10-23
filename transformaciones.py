# Función para leer la gramática desde un archivo .txt
def leer_gramatica(archivo):
    producciones = {}

    with open(archivo, 'r') as file:
        for linea in file:
            if '->' in linea:
                # Separar el no terminal de las producciones
                lado_izquierdo, lado_derecho = linea.split('->')
                lado_izquierdo = lado_izquierdo.strip()
                producciones[lado_izquierdo] = [prod.strip() for prod in lado_derecho.split('|')]

    return producciones


# Función para calcular el conjunto de primeros (First) de un símbolo
def first(symbol, productions, firsts):
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


# Función para comprobar si hay recursividad por la izquierda
def has_left_recursion(productions):
    for non_terminal in productions:
        for production in productions[non_terminal]:
            if production[0] == non_terminal:
                return True
    return False


# Función para comprobar si hay factores comunes por la izquierda
def has_common_prefix(productions):
    for non_terminal in productions:
        prefixes = set()
        for production in productions[non_terminal]:
            if production[0] in prefixes:
                return True
            prefixes.add(production[0])
    return False


# Función principal que verifica si una gramática es LL(1)
def is_ll1_grammar(productions):
    firsts = {}

    # Comprobar recursividad por la izquierda
    if has_left_recursion(productions):
        return False, "La gramática tiene recursividad por la izquierda."

    # Comprobar factores comunes por la izquierda
    if has_common_prefix(productions):
        return False, "La gramática tiene factores comunes por la izquierda."

    return True, "La gramática es LL(1)."


# Ejemplo de uso leyendo la gramática desde un archivo .txt
def main():
    archivo = 'gramatica.txt'  # Nombre del archivo
    producciones = leer_gramatica(archivo)

    is_ll1, message = is_ll1_grammar(producciones)
    print(message)


if __name__ == "__main__":
    main()
