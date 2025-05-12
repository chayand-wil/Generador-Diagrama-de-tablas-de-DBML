# SQL to DBML Converter

Este script convierte esquemas SQL (`CREATE TABLE` con `FOREIGN KEY`) al formato [DBML](https://www.dbml.org/) usado por herramientas como [DBDiagram.io](https://dbdiagram.io/).

---

## 🧠 ¿Qué hace?

- Lee texto `sql` con definiciones de tablas y claves foráneas.
- Extrae las tablas, campos y relaciones.
- Genera la representación en **DBML**.
- Puedes exportar el resultado a un archivo o imprimirlo en consola.

---

## 🛠️ Requisitos

- Python 3.6 o superior

---

## 🚀 Uso

### 1. Ejecutar desde archivo `.sql`

```bash
 
python3 generador_diag_tablas.py
Luego pega tu SQL directamente y presiona Ctrl+D (Linux/macOS) o Ctrl+Z y Enter (Windows) para procesar.
