"""Práctica 2: Planificación de hilos y orden de impresión.
Alumna: Alondra Goretti González Martínez (218534681)
Materia: Programación paralela y recurrente - Mtro. Zeus Cobián

Cada hilo imprime los números del 1 al 10 con una pequeña pausa (sleep) que
simula tiempo de ejecución. El programa compara:
  1) una ejecución secuencial (sin hilos), y
  2) una ejecución con 2 o 3 hilos, repetida varias veces para observar
     cómo cambia el orden de impresión según la planificación.

Uso:
    python hilos_impresion.py                    # 3 hilos, 1 repetición
    python hilos_impresion.py -n 2 -r 5          # 2 hilos, 5 repeticiones
    python hilos_impresion.py -n 3 -r 5 -a       # pausas aleatorias (más variación)
"""
import argparse
import random
import sys
import threading
import time

NOMBRES = ["A", "B", "C"]
LIMITE = 10


def tarea(nombre, pausa, aleatoria, registro):
    """Trabajo de cada hilo: imprime del 1 al 10 con una pausa entre números."""
    for numero in range(1, LIMITE + 1):
        time.sleep(random.uniform(0.5 * pausa, 1.5 * pausa) if aleatoria else pausa)
        # Se escribe la línea completa en una sola llamada para que no se
        # mezclen los caracteres de dos hilos en la misma línea.
        sys.stdout.write(f"  Hilo {nombre}: {numero}\n")
        registro.append(f"{nombre}{numero}")  # list.append es seguro entre hilos en CPython


def ejecutar_secuencial(n_hilos, pausa, aleatoria):
    """Las mismas tareas, una detrás de otra, sin hilos."""
    registro = []
    t0 = time.perf_counter()
    for nombre in NOMBRES[:n_hilos]:
        tarea(nombre, pausa, aleatoria, registro)
    return registro, time.perf_counter() - t0


def ejecutar_con_hilos(n_hilos, pausa, aleatoria):
    """Las mismas tareas, cada una en su propio hilo."""
    registro = []
    hilos = [threading.Thread(target=tarea, args=(nombre, pausa, aleatoria, registro))
             for nombre in NOMBRES[:n_hilos]]
    t0 = time.perf_counter()
    for hilo in hilos:
        hilo.start()
    for hilo in hilos:
        hilo.join()
    return registro, time.perf_counter() - t0


def leer_argumentos():
    p = argparse.ArgumentParser(description="Hilos que imprimen del 1 al 10")
    p.add_argument("-n", "--hilos", type=int, default=3, choices=[2, 3], help="número de hilos (2 o 3)")
    p.add_argument("-r", "--repeticiones", type=int, default=1, help="veces que se repite la versión con hilos")
    p.add_argument("-p", "--pausa", type=float, default=0.1, help="pausa en segundos entre números (default 0.1)")
    p.add_argument("-a", "--aleatoria", action="store_true", help="pausa aleatoria entre 0.5x y 1.5x de --pausa")
    return p.parse_args()


def main():
    args = leer_argumentos()
    n, pausa, alea = args.hilos, args.pausa, args.aleatoria

    print("=" * 56)
    print(f"EJECUCIÓN SECUENCIAL (sin hilos) · {n} tareas")
    print("=" * 56)
    seq, t_seq = ejecutar_secuencial(n, pausa, alea)
    print(f"Tiempo secuencial: {t_seq:.2f} s\n")

    ordenes, tiempos = [], []
    for rep in range(1, args.repeticiones + 1):
        print("=" * 56)
        print(f"EJECUCIÓN CON {n} HILOS · repetición {rep} de {args.repeticiones}")
        print("=" * 56)
        orden, t = ejecutar_con_hilos(n, pausa, alea)
        ordenes.append(" ".join(orden))
        tiempos.append(t)
        # Cada hilo siempre conserva su propio orden 1..10; lo que cambia es la mezcla entre hilos
        ok = all([x for x in orden if x[0] == nombre] == [f"{nombre}{i}" for i in range(1, LIMITE + 1)]
                 for nombre in NOMBRES[:n])
        print(f"Tiempo con hilos: {t:.2f} s · orden interno de cada hilo correcto: {'sí' if ok else 'NO'}\n")

    print("=" * 56)
    print("RESUMEN")
    print("=" * 56)
    print(f"Orden secuencial : {' '.join(seq)}")
    for i, o in enumerate(ordenes, 1):
        print(f"Con hilos (rep {i}): {o}")
    print(f"\nÓrdenes distintos entre repeticiones: {len(set(ordenes))} de {len(ordenes)}")
    print(f"Tiempo secuencial: {t_seq:.2f} s | tiempo medio con hilos: {sum(tiempos) / len(tiempos):.2f} s")


if __name__ == "__main__":
    main()
