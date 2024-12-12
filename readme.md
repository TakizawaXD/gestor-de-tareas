# Gestor de Tareas

Una aplicación de escritorio sencilla pero eficiente para gestionar tus tareas diarias. Desarrollada con Python utilizando **Tkinter** y SQLAlchemy, permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en tareas, exportar/importar a JSON y manejar el estado de completado.

## Características
- **Agregar tareas** con título y descripción.
- **Listar tareas** pendientes y completadas.
- **Marcar tareas como completadas**.
- **Eliminar tareas completadas**.
- **Exportar** tareas a un archivo `JSON`.
- **Importar** tareas desde un archivo `JSON`.

## Requisitos
1. Python 3.8 o superior.
2. Instalación de dependencias:
    ```bash
    pip install sqlalchemy
    ```

## Instalación
1. Clona este repositorio:
    ```bash
    git clone https://github.com/tu-usuario/gestor-de-tareas.git
    ```
2. Navega al directorio del proyecto:
    ```bash
    cd gestor-de-tareas
    ```
3. Ejecuta la aplicación:
    ```bash
    python app.py
    ```

## Uso
1. **Añade tareas** ingresando un título y una descripción opcional.
2. **Marca tareas como completadas** seleccionándolas de la lista.
3. **Elimina tareas completadas** con un clic en el botón correspondiente.
4. **Exporta tus tareas** a un archivo JSON para respaldarlas.
5. **Importa tus tareas** desde un archivo JSON existente.

