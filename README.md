# Práctica 2 · Planificación de hilos y orden de impresión

Programación paralela y recurrente · Universidad de Guadalajara (CUCEI)
Alumna: Alondra Goretti González Martínez · Código 218534681

Programa en Python que crea 2 o 3 hilos que imprimen del 1 al 10 con una pausa (`sleep`),
lo ejecuta varias veces para observar cómo cambia el orden de impresión y lo compara con
una ejecución secuencial.

## Simulador interactivo

**https://TU-USUARIO.github.io/practica2-hilos/**

(Reemplaza `TU-USUARIO` por tu usuario de GitHub.) Es una simulación en el navegador: permite
ejecutar con hilos o en secuencial, repetir 10 veces y comparar los órdenes de impresión.

## Archivos

| Archivo | Descripción |
|---|---|
| `index.html` | Simulador visual (HTML + CSS + JavaScript, sin dependencias) |
| `hilos_impresion.py` | Programa de la práctica |
| `Practica2_Hilos_Gonzalez_Martinez.pdf` | Informe de la práctica |

## Cómo ejecutar el programa

```bash
python hilos_impresion.py                # 3 hilos, 1 repetición
python hilos_impresion.py -n 2 -r 5      # 2 hilos, 5 repeticiones
python hilos_impresion.py -n 3 -r 5 -a   # pausas aleatorias
```

Requiere Python 3.8 o superior; no usa librerías externas.
