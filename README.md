# SoftwareFJ-Fase4-UNAD
Sistema de gestión de clientes, servicios y reservas desarrollado en Python 

# Software FJ - Sistema de Gestión de Clientes, Servicios y Reservas

## Descripción

Este proyecto fue desarrollado para la Fase 4 del curso Programación (213023) de la Universidad Nacional Abierta y a Distancia (UNAD). Consiste en un sistema desarrollado en Python que permite administrar clientes, servicios y reservas para una empresa ficticia llamada Software FJ. El programa utiliza programación orientada a objetos y no requiere bases de datos. La información se administra mediante objetos y listas durante la ejecución.

## Funcionalidades

- Registro y consulta de clientes.
- Registro de salas, equipos y asesorías especializadas.
- Creación, confirmación y cancelación de reservas.
- Cálculo de costos con descuentos e impuestos.
- Validación de datos y control de operaciones no permitidas.
- Manejo de excepciones personalizadas.
- Registro de eventos y errores en el archivo `sistema.log`.
- Menú interactivo desde la terminal.

## Conceptos de programación utilizados

El proyecto aplica abstracción, herencia, encapsulación y polimorfismo. También incluye manejo de excepciones mediante `try`, `except`, `else`, `finally` y encadenamiento de excepciones.

## Ejecución

El sistema fue desarrollado y probado con Python 3.14. Para ejecutarlo, se debe abrir el archivo `main.py` en Visual Studio Code y utilizar un intérprete de Python. También se puede ejecutar desde una terminal que tenga Python configurado mediante el comando `python main.py`. El programa muestra un menú con las opciones disponibles. La opción 9 permite ejecutar las simulaciones automáticas.

## Pruebas realizadas

Se implementaron 26 casos de prueba para verificar registros correctos e incorrectos, validaciones, cálculos, reservas, cancelaciones y manejo de errores.

En la ejecución realizada se obtuvieron los siguientes resultados:

- Pruebas realizadas: 26.
- Pruebas correctas: 26.
- Pruebas por revisar: 0.

Adicionalmente, se verificó manualmente el funcionamiento del menú y el procesamiento de una reserva.

## Registro de errores

El programa utiliza el módulo `logging` de Python para generar el archivo `sistema.log`, donde se registran las operaciones y las excepciones detectadas durante la ejecución.
