# KCH - Documentación de API con ejemplos cURL

Esta documentación proporciona ejemplos prácticos de cómo usar la API de formularios KCH con cURL.

## Configuración inicial

Asegúrate de que el servidor esté ejecutándose:
```bash
python main.py
```

El servidor estará disponible en: `http://localhost:8000`

---

## 1. Formulario de Edad
**Endpoint:** `POST /form/age`

### Ejemplo básico:
```bash
curl -X POST "http://localhost:8000/form/age" \
     -H "Content-Type: application/json" \
     -d '{"age": "25-35"}'
```

### Todas las opciones válidas:
```bash
# Opción 1: 18-24 años
curl -X POST "http://localhost:8000/form/age" \
     -H "Content-Type: application/json" \
     -d '{"age": "18-24"}'

# Opción 2: 25-35 años
curl -X POST "http://localhost:8000/form/age" \
     -H "Content-Type: application/json" \
     -d '{"age": "25-35"}'

# Opción 3: 35-44 años
curl -X POST "http://localhost:8000/form/age" \
     -H "Content-Type: application/json" \
     -d '{"age": "35-44"}'

# Opción 4: 45+ años
curl -X POST "http://localhost:8000/form/age" \
     -H "Content-Type: application/json" \
     -d '{"age": "45+"}'
```

### Respuesta esperada:
```json
{
  "id": "f9d0b4e2-9a9a-4fa7-9c6c-5c3b7bc9e123",
  "form": "age",
  "received_at": "2025-09-26T12:00:00Z",
  "data": {
    "age": "25-35"
  }
}
```

---

## 2. Datos Personales
**Endpoint:** `POST /form/personal-data`

### Ejemplo completo:
```bash
curl -X POST "http://localhost:8000/form/personal-data" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Ana Pérez García",
       "street": "Gran Vía",
       "number": "123",
       "floor": "4",
       "door": "B",
       "stair": "2"
     }'
```

### Ejemplo mínimo (solo campos obligatorios):
```bash
curl -X POST "http://localhost:8000/form/personal-data" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Juan López",
       "street": "Calle Mayor",
       "number": "456"
     }'
```

### Ejemplo con dirección compleja:
```bash
curl -X POST "http://localhost:8000/form/personal-data" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "María González Rodríguez",
       "street": "Avenida de la Constitución",
       "number": "789",
       "floor": "Bajo",
       "door": "Izquierda",
       "stair": "A"
     }'
```

---

## 3. Identificación
**Endpoint:** `POST /form/identification`

### Ejemplo con DNI:
```bash
curl -X POST "http://localhost:8000/form/identification" \
     -H "Content-Type: application/json" \
     -d '{
       "document_type": "DNI",
       "document_number": "12345678Z",
       "phone": "+34 600 123 456"
     }'
```

### Ejemplo con NIE:
```bash
curl -X POST "http://localhost:8000/form/identification" \
     -H "Content-Type: application/json" \
     -d '{
       "document_type": "NIE",
       "document_number": "X1234567L",
       "phone": "600 123 456"
     }'
```

### Ejemplo con Pasaporte:
```bash
curl -X POST "http://localhost:8000/form/identification" \
     -H "Content-Type: application/json" \
     -d '{
       "document_type": "Pasaporte",
       "document_number": "ABC123456",
       "phone": "(+34) 600-123-456"
     }'
```

### Diferentes formatos de teléfono válidos:
```bash
# Formato internacional
curl -X POST "http://localhost:8000/form/identification" \
     -H "Content-Type: application/json" \
     -d '{
       "document_type": "DNI",
       "document_number": "87654321Y",
       "phone": "+34 600 123 456"
     }'

# Formato nacional
curl -X POST "http://localhost:8000/form/identification" \
     -H "Content-Type: application/json" \
     -d '{
       "document_type": "DNI",
       "document_number": "87654321Y",
       "phone": "600123456"
     }'

# Con paréntesis
curl -X POST "http://localhost:8000/form/identification" \
     -H "Content-Type: application/json" \
     -d '{
       "document_type": "DNI",
       "document_number": "87654321Y",
       "phone": "(600) 123 456"
     }'
```

---

## 4. Descubrimiento de Descuentos
**Endpoint:** `POST /form/discovery`

### Ejemplos por canal:
```bash
# Instagram
curl -X POST "http://localhost:8000/form/discovery" \
     -H "Content-Type: application/json" \
     -d '{"source": "Instagram"}'

# Google
curl -X POST "http://localhost:8000/form/discovery" \
     -H "Content-Type: application/json" \
     -d '{"source": "Google"}'

# Recomendación de amigos
curl -X POST "http://localhost:8000/form/discovery" \
     -H "Content-Type: application/json" \
     -d '{"source": "Amigos"}'

# Folleto publicitario
curl -X POST "http://localhost:8000/form/discovery" \
     -H "Content-Type: application/json" \
     -d '{"source": "Folleto"}'

# Facebook
curl -X POST "http://localhost:8000/form/discovery" \
     -H "Content-Type: application/json" \
     -d '{"source": "Facebook"}'

# TikTok
curl -X POST "http://localhost:8000/form/discovery" \
     -H "Content-Type: application/json" \
     -d '{"source": "TikTok"}'

# Otros canales
curl -X POST "http://localhost:8000/form/discovery" \
     -H "Content-Type: application/json" \
     -d '{"source": "Televisión"}'
```

---

## 5. Tienda Favorita
**Endpoint:** `POST /form/favorite-store`

### Ejemplos de tiendas:
```bash
# Tienda del centro
curl -X POST "http://localhost:8000/form/favorite-store" \
     -H "Content-Type: application/json" \
     -d '{"store": "KCH Centro"}'

# Tienda del norte
curl -X POST "http://localhost:8000/form/favorite-store" \
     -H "Content-Type: application/json" \
     -d '{"store": "KCH Norte"}'

# Tienda del sur
curl -X POST "http://localhost:8000/form/favorite-store" \
     -H "Content-Type: application/json" \
     -d '{"store": "KCH Sur"}'

# Compras online
curl -X POST "http://localhost:8000/form/favorite-store" \
     -H "Content-Type: application/json" \
     -d '{"store": "KCH Online"}'

# Centro comercial específico
curl -X POST "http://localhost:8000/form/favorite-store" \
     -H "Content-Type: application/json" \
     -d '{"store": "KCH Plaza Mayor"}'
```

---

## 6. Tipo de Servicio a Domicilio
**Endpoint:** `POST /form/delivery-type`

### Opciones de envío:
```bash
# Envío estándar
curl -X POST "http://localhost:8000/form/delivery-type" \
     -H "Content-Type: application/json" \
     -d '{"service_type": "Envío estándar"}'

# Envío express
curl -X POST "http://localhost:8000/form/delivery-type" \
     -H "Content-Type: application/json" \
     -d '{"service_type": "Express"}'

# Recogida en tienda
curl -X POST "http://localhost:8000/form/delivery-type" \
     -H "Content-Type: application/json" \
     -d '{"service_type": "Recogida en tienda"}'

# Envío el mismo día
curl -X POST "http://localhost:8000/form/delivery-type" \
     -H "Content-Type: application/json" \
     -d '{"service_type": "Same day"}'

# Envío programado
curl -X POST "http://localhost:8000/form/delivery-type" \
     -H "Content-Type: application/json" \
     -d '{"service_type": "Envío programado"}'
```

---

## 7. Productos de Interés
**Endpoint:** `POST /form/products`

### Ejemplo básico:
```bash
curl -X POST "http://localhost:8000/form/products" \
     -H "Content-Type: application/json" \
     -d '{
       "products": ["Champú", "Acondicionador", "Serum"]
     }'
```

### Ejemplo con un solo producto:
```bash
curl -X POST "http://localhost:8000/form/products" \
     -H "Content-Type: application/json" \
     -d '{
       "products": ["Champú anticaspa"]
     }'
```

### Ejemplo con múltiples productos de belleza:
```bash
curl -X POST "http://localhost:8000/form/products" \
     -H "Content-Type: application/json" \
     -d '{
       "products": [
         "Champú hidratante",
         "Acondicionador reparador",
         "Mascarilla capilar",
         "Serum facial",
         "Crema hidratante",
         "Protector solar"
       ]
     }'
```

### Ejemplo con productos de cuidado personal:
```bash
curl -X POST "http://localhost:8000/form/products" \
     -H "Content-Type: application/json" \
     -d '{
       "products": [
         "Gel de ducha",
         "Desodorante",
         "Pasta de dientes",
         "Enjuague bucal",
         "Jabón de manos"
       ]
     }'
```

---

## 8. Conocimiento de Promociones Semanales
**Endpoint:** `POST /form/weekly-promos-knowledge`

### Respuestas típicas:
```bash
# Respuesta afirmativa
curl -X POST "http://localhost:8000/form/weekly-promos-knowledge" \
     -H "Content-Type: application/json" \
     -d '{"answer": "Sí"}'

# Respuesta negativa
curl -X POST "http://localhost:8000/form/weekly-promos-knowledge" \
     -H "Content-Type: application/json" \
     -d '{"answer": "No"}'

# Conocimiento parcial
curl -X POST "http://localhost:8000/form/weekly-promos-knowledge" \
     -H "Content-Type: application/json" \
     -d '{"answer": "Algo"}'

# Un poco
curl -X POST "http://localhost:8000/form/weekly-promos-knowledge" \
     -H "Content-Type: application/json" \
     -d '{"answer": "Un poco"}'

# Bastante
curl -X POST "http://localhost:8000/form/weekly-promos-knowledge" \
     -H "Content-Type: application/json" \
     -d '{"answer": "Bastante"}'

# Respuesta personalizada
curl -X POST "http://localhost:8000/form/weekly-promos-knowledge" \
     -H "Content-Type: application/json" \
     -d '{"answer": "Solo las de productos capilares"}'
```

---

## 9. Información de Contacto
**Endpoint:** `POST /form/contact`

### Ejemplo con familia numerosa:
```bash
curl -X POST "http://localhost:8000/form/contact" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "ana.perez@gmail.com",
       "large_family": true
     }'
```

### Ejemplo sin familia numerosa:
```bash
curl -X POST "http://localhost:8000/form/contact" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "juan.lopez@hotmail.com",
       "large_family": false
     }'
```

### Ejemplos con diferentes proveedores de email:
```bash
# Gmail
curl -X POST "http://localhost:8000/form/contact" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "usuario@gmail.com",
       "large_family": false
     }'

# Yahoo
curl -X POST "http://localhost:8000/form/contact" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "usuario@yahoo.es",
       "large_family": true
     }'

# Outlook
curl -X POST "http://localhost:8000/form/contact" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "usuario@outlook.com",
       "large_family": false
     }'

# Email corporativo
curl -X POST "http://localhost:8000/form/contact" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "maria.gonzalez@empresa.com",
       "large_family": true
     }'
```

---

## Endpoint de Debug
**Endpoint:** `GET /debug/dump`

### Ver todos los datos almacenados:
```bash
curl -X GET "http://localhost:8000/debug/dump"
```

### Respuesta típica:
```json
{
  "count": 2,
  "items": {
    "f9d0b4e2-9a9a-4fa7-9c6c-5c3b7bc9e123": {
      "form": "age",
      "data": {"age": "25-35"}
    },
    "a1b2c3d4-5e6f-7g8h-9i0j-k1l2m3n4o5p6": {
      "form": "contact",
      "data": {"email": "ana@example.com", "large_family": true}
    }
  }
}
```

---

## Script de Ejemplo Completo

Aquí tienes un script que envía datos a todos los formularios:

```bash
#!/bin/bash

# URL base de la API
BASE_URL="http://localhost:8000"

echo "=== Enviando datos a todos los formularios KCH ==="

# 1. Edad
echo "1. Enviando edad..."
curl -X POST "$BASE_URL/form/age" \
     -H "Content-Type: application/json" \
     -d '{"age": "25-35"}' \
     -w "\nStatus: %{http_code}\n\n"

# 2. Datos personales
echo "2. Enviando datos personales..."
curl -X POST "$BASE_URL/form/personal-data" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Ana Pérez García",
       "street": "Gran Vía",
       "number": "123",
       "floor": "4",
       "door": "B"
     }' \
     -w "\nStatus: %{http_code}\n\n"

# 3. Identificación
echo "3. Enviando identificación..."
curl -X POST "$BASE_URL/form/identification" \
     -H "Content-Type: application/json" \
     -d '{
       "document_type": "DNI",
       "document_number": "12345678Z",
       "phone": "+34 600 123 456"
     }' \
     -w "\nStatus: %{http_code}\n\n"

# 4. Descubrimiento
echo "4. Enviando canal de descubrimiento..."
curl -X POST "$BASE_URL/form/discovery" \
     -H "Content-Type: application/json" \
     -d '{"source": "Instagram"}' \
     -w "\nStatus: %{http_code}\n\n"

# 5. Tienda favorita
echo "5. Enviando tienda favorita..."
curl -X POST "$BASE_URL/form/favorite-store" \
     -H "Content-Type: application/json" \
     -d '{"store": "KCH Centro"}' \
     -w "\nStatus: %{http_code}\n\n"

# 6. Tipo de envío
echo "6. Enviando tipo de envío..."
curl -X POST "$BASE_URL/form/delivery-type" \
     -H "Content-Type: application/json" \
     -d '{"service_type": "Express"}' \
     -w "\nStatus: %{http_code}\n\n"

# 7. Productos
echo "7. Enviando productos..."
curl -X POST "$BASE_URL/form/products" \
     -H "Content-Type: application/json" \
     -d '{
       "products": ["Champú", "Acondicionador", "Serum facial"]
     }' \
     -w "\nStatus: %{http_code}\n\n"

# 8. Conocimiento de promociones
echo "8. Enviando conocimiento de promociones..."
curl -X POST "$BASE_URL/form/weekly-promos-knowledge" \
     -H "Content-Type: application/json" \
     -d '{"answer": "Sí"}' \
     -w "\nStatus: %{http_code}\n\n"

# 9. Contacto
echo "9. Enviando información de contacto..."
curl -X POST "$BASE_URL/form/contact" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "ana.perez@gmail.com",
       "large_family": true
     }' \
     -w "\nStatus: %{http_code}\n\n"

# Ver todos los datos
echo "=== Verificando datos almacenados ==="
curl -X GET "$BASE_URL/debug/dump" | python -m json.tool

echo -e "\n=== Proceso completado ==="
```

### Para usar el script:
1. Guarda el contenido en un archivo llamado `test_api.sh`
2. Dale permisos de ejecución: `chmod +x test_api.sh`
3. Ejecuta: `./test_api.sh`

---

## Códigos de Respuesta HTTP

- **200 OK**: Solicitud exitosa
- **422 Unprocessable Entity**: Error de validación (datos inválidos)
- **404 Not Found**: Endpoint no encontrado
- **500 Internal Server Error**: Error del servidor

## Consejos para usar cURL

1. **Formato JSON**: Siempre incluye el header `Content-Type: application/json`
2. **Escapar comillas**: En Windows, usa comillas dobles y escapa las internas con `\"`
3. **Archivos**: Puedes guardar el JSON en un archivo y usar `@archivo.json`
4. **Verbose**: Usa `-v` para ver detalles de la petición
5. **Silent**: Usa `-s` para suprimir la barra de progreso

### Ejemplo con archivo JSON:
```bash
# Crear archivo datos.json
echo '{"age": "25-35"}' > datos.json

# Usar el archivo
curl -X POST "http://localhost:8000/form/age" \
     -H "Content-Type: application/json" \
     -d @datos.json
```
