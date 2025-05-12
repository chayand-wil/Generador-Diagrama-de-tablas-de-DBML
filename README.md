# SQL to DBML Converter

**Convierte esquemas SQL a formato DBML** para visualización en [dbdiagram.io](https://dbdiagram.io/).

## 📦 Instalación
```bash
git clone https://github.com/tu-usuario/sql-to-dbml.git
cd sql-to-dbml


Convertir archivo SQL
python3 sql_to_dbml.py esquema.sql -o salida.dbml

Pegar SQL directamente
python3 sql_to_dbml.py
# Pega tu SQL y presiona Ctrl+D (Linux/Mac) o Ctrl+Z+Enter (Windows)

EJEMPLO
Entrada SQL
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);

Salida DBML:
Table users {
  id INT
  name VARCHAR(100)
}

Características
✅ Extrae tablas, campos y relaciones
✅ Soporta: INT, VARCHAR, DECIMAL, etc.
✅ Maneja claves foráneas (FOREIGN KEY)
✅ Entrada desde archivo o terminal


