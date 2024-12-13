import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, Integer, String, Boolean, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import os

def sanitize_string(value):
    if isinstance(value, str): 
        return value.replace("'", "''")
    return str(value) 

Base = declarative_base()

DATABASE_URL = 'sqlite:///tareas.db'
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()

class Tarea(Base):
    __tablename__ = 'tareas'
    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    completada = Column(Boolean, default=False)

Base.metadata.create_all(engine)

@event.listens_for(engine, "before_cursor_execute")
def validate_query(conn, cursor, statement, parameters, context, executemany):
    if any(sanitize_string(param) in statement for param in parameters):
        raise ValueError("Se detectó una posible inyección SQL. Operación abortada.")

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("1280x720")
        self.root.configure(bg="#2c2f38")

        self.header = tk.Label(
            root, text="Gestor de Tareas", font=("Segoe UI", 20, "bold"),
            bg="#1f2328", fg="#f0f0f0", pady=15)
        self.header.pack(fill=tk.X)

        self.form_frame = tk.Frame(root, bg="#2c2f38")
        self.form_frame.pack(pady=15)
        self.titulo_label = tk.Label(self.form_frame, text="Título:", bg="#2c2f38", font=("Segoe UI", 12), fg="#f0f0f0")
        self.titulo_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.titulo_entry = tk.Entry(self.form_frame, width=40, font=("Segoe UI", 12), bg="#3d4149", fg="#f0f0f0", insertbackground="white")
        self.titulo_entry.grid(row=0, column=1, padx=10, pady=10)

        self.descripcion_label = tk.Label(self.form_frame, text="Descripción:", bg="#2c2f38", font=("Segoe UI", 12), fg="#f0f0f0")
        self.descripcion_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.descripcion_entry = tk.Entry(self.form_frame, width=40, font=("Segoe UI", 12), bg="#3d4149", fg="#f0f0f0", insertbackground="white")
        self.descripcion_entry.grid(row=1, column=1, padx=10, pady=10)

        self.add_button = tk.Button(
            self.form_frame, text="Agregar Tarea", bg="#4CAF50", fg="white", font=("Segoe UI", 12, "bold"),
            relief="raised", command=self.agregar_tarea)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=15)

        self.list_frame = tk.Frame(root, bg="#2c2f38")
        self.list_frame.pack(pady=15)
        self.tareas_listbox = tk.Listbox(self.list_frame, width=70, height=15, font=("Segoe UI", 12), bg="#3d4149", fg="#f0f0f0", selectbackground="#4CAF50", selectforeground="white")
        self.tareas_listbox.pack(side=tk.LEFT, padx=10, pady=10)

        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tareas_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.tareas_listbox.yview)

        self.actions_frame = tk.Frame(root, bg="#2c2f38")
        self.actions_frame.pack(pady=20)
        self.complete_button = tk.Button(
            self.actions_frame, text="Completar Tarea", bg="#FF9800", fg="white", font=("Segoe UI", 12, "bold"),
            relief="raised", command=self.completar_tarea)
        self.complete_button.grid(row=0, column=0, padx=15, pady=10)

        self.delete_button = tk.Button(
            self.actions_frame, text="Eliminar Tareas Completadas", bg="#F44336", fg="white", font=("Segoe UI", 12, "bold"),
            relief="raised", command=self.eliminar_tareas_completadas)
        self.delete_button.grid(row=0, column=1, padx=15, pady=10)

        self.export_button = tk.Button(
            self.actions_frame, text="Exportar Tareas", bg="#2196F3", fg="white", font=("Segoe UI", 12, "bold"),
            relief="raised", command=self.exportar_tareas)
        self.export_button.grid(row=0, column=2, padx=15, pady=10)

        self.import_button = tk.Button(
            self.actions_frame, text="Importar Tareas", bg="#2196F3", fg="white", font=("Segoe UI", 12, "bold"),
            relief="raised", command=self.importar_tareas)
        self.import_button.grid(row=0, column=3, padx=15, pady=10)

        self.cargar_tareas()

    def agregar_tarea(self):
        titulo = self.titulo_entry.get().strip()
        descripcion = self.descripcion_entry.get().strip()
        if titulo:
            nueva_tarea = Tarea(titulo=sanitize_string(titulo), descripcion=sanitize_string(descripcion))
            session.add(nueva_tarea)
            session.commit()
            self.titulo_entry.delete(0, tk.END)
            self.descripcion_entry.delete(0, tk.END)
            self.cargar_tareas()
            messagebox.showinfo("Éxito", "Tarea agregada correctamente.")
        else:
            messagebox.showwarning("Advertencia", "El título no puede estar vacío.")

    def cargar_tareas(self):
        self.tareas_listbox.delete(0, tk.END)
        tareas = session.query(Tarea).all()
        for tarea in tareas:
            estado = "[X]" if tarea.completada else "[ ]"
            self.tareas_listbox.insert(tk.END, f"{tarea.id}. {estado} {tarea.titulo} - {tarea.descripcion}")

    def completar_tarea(self):
        seleccion = self.tareas_listbox.curselection()
        if seleccion:
            tarea_id = int(self.tareas_listbox.get(seleccion[0]).split(".")[0])
            tarea = session.query(Tarea).filter_by(id=tarea_id).first()
            if tarea and not tarea.completada:
                tarea.completada = True
                session.commit()
                self.cargar_tareas()
                messagebox.showinfo("Éxito", "Tarea marcada como completada.")
            else:
                messagebox.showwarning("Advertencia", "La tarea ya está completada o no se encontró.")
        else:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para completar.")

    def eliminar_tareas_completadas(self):
        tareas_completadas = session.query(Tarea).filter_by(completada=True).all()
        if tareas_completadas:
            for tarea in tareas_completadas:
                session.delete(tarea)
            session.commit()
            self.cargar_tareas()
            messagebox.showinfo("Éxito", "Tareas completadas eliminadas correctamente.")
        else:
            messagebox.showwarning("Advertencia", "No hay tareas completadas para eliminar.")

    def exportar_tareas(self):
        tareas = session.query(Tarea).all()
        datos = [
            {
                "id": tarea.id,
                "titulo": tarea.titulo,
                "descripcion": tarea.descripcion,
                "completada": tarea.completada,
            }
            for tarea in tareas
        ]
        with open("tareas.json", "w") as archivo:
            json.dump(datos, archivo, indent=4)
        messagebox.showinfo("Éxito", "Tareas exportadas a 'tareas.json'.")

    def importar_tareas(self):
        try:
            with open("tareas.json", "r") as archivo:
                datos = json.load(archivo)
                for item in datos:
                    if not session.query(Tarea).filter_by(id=item["id"]).first():
                        nueva_tarea = Tarea(
                            id=item["id"],
                            titulo=sanitize_string(item["titulo"]),
                            descripcion=sanitize_string(item["descripcion"]),
                            completada=item["completada"],
                        )
                        session.add(nueva_tarea)
                session.commit()
            self.cargar_tareas()
            messagebox.showinfo("Éxito", "Tareas importadas desde 'tareas.json'.")
        except FileNotFoundError:
            messagebox.showwarning("Advertencia", "No se encontró el archivo 'tareas.json'.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error al leer el archivo JSON.")

def run_sonar():
    print("Usa SonarScanner desde tu terminal con el siguiente comando:")
    print("sonar-scanner -Dsonar.projectKey=task_manager -Dsonar.sources=. -Dsonar.host.url=http://localhost:9000 -Dsonar.login=<tu_token>")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
