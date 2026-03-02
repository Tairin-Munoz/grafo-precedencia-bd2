from collections import defaultdict

def parse_operation(op):
    try:
        tipo = op[0].upper()
        transaccion = "T" + op[1]
        dato = op[3]
        return tipo, transaccion, dato
    except:
        return None

def construir_grafo(operaciones):
    grafo = defaultdict(set)
    parsed = []
    transacciones = set()

    for op in operaciones:
        p = parse_operation(op)
        if p:
            parsed.append(p)
            transacciones.add(p[1])

    for i in range(len(parsed)):
        tipo1, t1, dato1 = parsed[i]
        for j in range(i + 1, len(parsed)):
            tipo2, t2, dato2 = parsed[j]
            if t1 != t2 and dato1 == dato2:
                if tipo1 == 'W' or tipo2 == 'W':
                    grafo[t1].add(t2)

    for t in transacciones:
        if t not in grafo:
            grafo[t] = set()

    return grafo

def tiene_ciclo(grafo):
    visitado = set()
    pila = set()

    def dfs(nodo):
        visitado.add(nodo)
        pila.add(nodo)
        for vecino in grafo[nodo]:
            if vecino not in visitado:
                if dfs(vecino):
                    return True
            elif vecino in pila:
                return True
        pila.remove(nodo)
        return False

    for nodo in grafo:
        if nodo not in visitado:
            if dfs(nodo):
                return True

    return False

def mostrar_grafo(grafo):
    print("\nGRAFO DE PRECEDENCIA")
    print("---------------------------------")
    for t in sorted(grafo):
        if grafo[t]:
            destinos = ", ".join(sorted(grafo[t]))
            print(f"{t}  →  {destinos}")
        else:
            print(f"{t}  →  (sin dependencias)")

def main():
    print("============================================")
    print("   VERIFICADOR DE SERIALIZABILIDAD")
    print("============================================\n")

    entrada = input("Ingrese las operaciones separadas por espacio:\n> ")
    operaciones = entrada.split()

    print("\nOPERACIONES INGRESADAS")
    print("---------------------------------")
    for i, op in enumerate(operaciones, 1):
        print(f"{i}. {op}")

    grafo = construir_grafo(operaciones)
    mostrar_grafo(grafo)

    print("\nRESULTADO")
    print("---------------------------------")
    if tiene_ciclo(grafo):
        print("NO es serializable")
    else:
        print("ES serializable")

if __name__ == "__main__":
    main()