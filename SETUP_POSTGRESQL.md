# Configuración de PostgreSQL para KCH Forms API

## Opción 1: Usando Docker (Recomendado)

### Prerrequisitos
- Docker y Docker Compose instalados

### Pasos:

1. **Iniciar PostgreSQL con Docker Compose:**
```bash
docker-compose up -d postgres
```

2. **Instalar dependencias Python:**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la API:**
```bash
python main.py
```

La API creará automáticamente las tablas al iniciar.

### Comandos útiles:
```bash
# Ver logs de PostgreSQL
docker-compose logs postgres

# Conectar a PostgreSQL directamente
docker-compose exec postgres psql -U kch_user -d kch_forms

# Parar los servicios
docker-compose down

# Parar y eliminar datos
docker-compose down -v
```

---

## Opción 2: PostgreSQL Local

### 1. Instalar PostgreSQL
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# CentOS/RHEL
sudo yum install postgresql-server postgresql-contrib
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql

# macOS (con Homebrew)
brew install postgresql
brew services start postgresql
```

### 2. Crear base de datos y usuario
```bash
# Conectar como usuario postgres
sudo -u postgres psql

# En el prompt de PostgreSQL:
CREATE DATABASE kch_forms;
CREATE USER kch_user WITH PASSWORD 'kch_password';
GRANT ALL PRIVILEGES ON DATABASE kch_forms TO kch_user;
\q
```

### 3. Configurar variables de entorno
```bash
export DATABASE_URL="postgresql://kch_user:kch_password@localhost:5432/kch_forms"
```

O crear un archivo `.env`:
```
DATABASE_URL=postgresql://kch_user:kch_password@localhost:5432/kch_forms
```

### 4. Ejecutar la aplicación
```bash
python main.py
```

---

## Estructura de la Base de Datos

### Tabla: `form_submissions`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | UUID | Identificador único (Primary Key) |
| `form` | VARCHAR(50) | Tipo de formulario |
| `received_at` | TIMESTAMP | Fecha de recepción |
| `data` | JSON | Datos completos del formulario |
| `age_range` | VARCHAR(10) | Rango de edad (indexado) |
| `customer_name` | VARCHAR(255) | Nombre del cliente (indexado) |
| `street` | VARCHAR(255) | Calle |
| `number` | VARCHAR(20) | Número |
| `floor` | VARCHAR(20) | Piso |
| `door` | VARCHAR(20) | Puerta |
| `stair` | VARCHAR(20) | Escalera |
| `document_type` | VARCHAR(50) | Tipo de documento |
| `document_number` | VARCHAR(50) | Número de documento (indexado) |
| `phone` | VARCHAR(50) | Teléfono (indexado) |
| `discovery_source` | VARCHAR(100) | Canal de descubrimiento (indexado) |
| `favorite_store` | VARCHAR(100) | Tienda favorita (indexado) |
| `delivery_type` | VARCHAR(100) | Tipo de envío (indexado) |
| `products_text` | TEXT | Productos como texto |
| `weekly_promos_answer` | VARCHAR(100) | Respuesta promociones (indexado) |
| `email` | VARCHAR(255) | Email (indexado) |
| `large_family` | BOOLEAN | Familia numerosa (indexado) |

### Ventajas del diseño:

1. **Flexibilidad**: Los datos completos se almacenan en JSON
2. **Performance**: Campos importantes indexados para consultas rápidas
3. **Reportes**: Fácil generación de reportes y estadísticas
4. **Búsquedas**: Campos específicos permiten filtros eficientes

---

## Consultas SQL Útiles

### Ver todos los formularios por tipo:
```sql
SELECT form, COUNT(*) as total 
FROM form_submissions 
GROUP BY form 
ORDER BY total DESC;
```

### Clientes por rango de edad:
```sql
SELECT age_range, COUNT(*) as total 
FROM form_submissions 
WHERE age_range IS NOT NULL 
GROUP BY age_range;
```

### Canales de descubrimiento más populares:
```sql
SELECT discovery_source, COUNT(*) as total 
FROM form_submissions 
WHERE discovery_source IS NOT NULL 
GROUP BY discovery_source 
ORDER BY total DESC;
```

### Productos más solicitados:
```sql
SELECT products_text, COUNT(*) as total 
FROM form_submissions 
WHERE products_text IS NOT NULL 
GROUP BY products_text 
ORDER BY total DESC;
```

### Clientes con familia numerosa:
```sql
SELECT COUNT(*) as familias_numerosas 
FROM form_submissions 
WHERE large_family = true;
```

### Formularios por fecha:
```sql
SELECT DATE(received_at) as fecha, COUNT(*) as total 
FROM form_submissions 
GROUP BY DATE(received_at) 
ORDER BY fecha DESC;
```

---

## Backup y Restauración

### Crear backup:
```bash
# Con Docker
docker-compose exec postgres pg_dump -U kch_user kch_forms > backup.sql

# PostgreSQL local
pg_dump -U kch_user -h localhost kch_forms > backup.sql
```

### Restaurar backup:
```bash
# Con Docker
docker-compose exec -T postgres psql -U kch_user kch_forms < backup.sql

# PostgreSQL local
psql -U kch_user -h localhost kch_forms < backup.sql
```

---

## Monitoreo y Mantenimiento

### Ver conexiones activas:
```sql
SELECT * FROM pg_stat_activity WHERE datname = 'kch_forms';
```

### Ver tamaño de la base de datos:
```sql
SELECT pg_size_pretty(pg_database_size('kch_forms'));
```

### Ver estadísticas de la tabla:
```sql
SELECT * FROM pg_stat_user_tables WHERE relname = 'form_submissions';
```

---

## Troubleshooting

### Error de conexión:
1. Verificar que PostgreSQL esté ejecutándose
2. Comprobar credenciales en `DATABASE_URL`
3. Verificar que el puerto 5432 esté disponible

### Error de permisos:
```sql
GRANT ALL PRIVILEGES ON DATABASE kch_forms TO kch_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO kch_user;
```

### Reiniciar desde cero:
```bash
# Con Docker
docker-compose down -v
docker-compose up -d postgres

# PostgreSQL local
sudo -u postgres psql -c "DROP DATABASE IF EXISTS kch_forms;"
sudo -u postgres psql -c "CREATE DATABASE kch_forms;"
```
