# KCH – Formularios de Captación

API REST con 9 endpoints para recopilar datos de clientes a través de formularios específicos.

## Características

- **9 endpoints POST** organizados por categorías
- **Validación estricta** con Pydantic v2
- **Documentación automática** con OpenAPI/Swagger
- **Ejemplos incluidos** para facilitar las pruebas
- **Almacenamiento en memoria** (demo - cambiar por BD en producción)
- **CORS habilitado** para desarrollo

## Instalación

1. Clona o descarga el proyecto
2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # o
   venv\Scripts\activate     # Windows
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

```bash
# Opción 1: Usando uvicorn directamente
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Opción 2: Ejecutando el archivo main.py
python main.py
```

La API estará disponible en: http://localhost:8000

## Documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints Disponibles

### 1. Edad - `POST /form/age`
```json
{
  "age": "25-35"
}
```
Opciones: `"18-24"`, `"25-35"`, `"35-44"`, `"45+"`

### 2. Datos Personales - `POST /form/personal-data`
```json
{
  "name": "Ana Pérez",
  "street": "Gran Vía",
  "number": "123",
  "floor": "4",
  "door": "B",
  "stair": "2"
}
```

### 3. Identificación - `POST /form/identification`
```json
{
  "document_type": "DNI",
  "document_number": "12345678Z",
  "phone": "+34 600 123 456"
}
```

### 4. Descubrimiento - `POST /form/discovery`
```json
{
  "source": "Instagram"
}
```

### 5. Tienda Favorita - `POST /form/favorite-store`
```json
{
  "store": "KCH Centro"
}
```

### 6. Tipo de Envío - `POST /form/delivery-type`
```json
{
  "service_type": "Express"
}
```

### 7. Productos - `POST /form/products`
```json
{
  "products": ["Champú", "Acondicionador", "Serum"]
}
```

### 8. Promociones Semanales - `POST /form/weekly-promos-knowledge`
```json
{
  "answer": "Sí"
}
```

### 9. Contacto - `POST /form/contact`
```json
{
  "email": "ana@example.com",
  "large_family": true
}
```

### Debug - `GET /debug/dump`
Endpoint para ver todos los datos almacenados en memoria (solo para desarrollo).

## Respuesta Estándar

Todos los endpoints POST devuelven:

```json
{
  "id": "f9d0b4e2-9a9a-4fa7-9c6c-5c3b7bc9e123",
  "form": "age",
  "received_at": "2025-09-26T12:00:00Z",
  "data": {
    // datos del formulario enviado
  }
}
```

## Estructura del Proyecto

```
kch-questions/
├── main.py              # Aplicación FastAPI principal
├── requirements.txt     # Dependencias Python
├── README.md           # Este archivo
└── venv/               # Entorno virtual (creado automáticamente)
```

## Notas de Desarrollo

- Los datos se almacenan en memoria (`DB` dict) solo para demo
- En producción, reemplazar por una base de datos real
- CORS está configurado para permitir todos los orígenes (ajustar en producción)
- Todos los campos tienen validación estricta y ejemplos
- La documentación se genera automáticamente con OpenAPI

## Tests

### Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests con información detallada
pytest -v

# Ejecutar tests con cobertura
pytest --cov=main

# Ejecutar un test específico
pytest test_main.py::TestAgeEndpoint::test_submit_age_valid

# Ejecutar tests de una clase específica
pytest test_main.py::TestAgeEndpoint
```

### Estructura de Tests

Los tests están organizados en clases por endpoint:

- `TestAgeEndpoint` - Tests para `/form/age`
- `TestPersonalDataEndpoint` - Tests para `/form/personal-data`
- `TestIdentificationEndpoint` - Tests para `/form/identification`
- `TestDiscoveryEndpoint` - Tests para `/form/discovery`
- `TestFavoriteStoreEndpoint` - Tests para `/form/favorite-store`
- `TestDeliveryTypeEndpoint` - Tests para `/form/delivery-type`
- `TestProductsEndpoint` - Tests para `/form/products`
- `TestWeeklyPromosKnowledgeEndpoint` - Tests para `/form/weekly-promos-knowledge`
- `TestContactEndpoint` - Tests para `/form/contact`
- `TestDebugEndpoint` - Tests para `/debug/dump`
- `TestResponseFormat` - Tests para verificar formato de respuesta
- `TestErrorHandling` - Tests para manejo de errores

### Cobertura de Tests

Los tests cubren:

✅ **Casos válidos**: Todos los endpoints con datos correctos  
✅ **Validación de campos**: Campos requeridos y opcionales  
✅ **Validación de tipos**: Enums, emails, teléfonos, etc.  
✅ **Casos límite**: Listas vacías, strings vacíos, etc.  
✅ **Formato de respuesta**: Estructura consistente en todas las respuestas  
✅ **Manejo de errores**: JSON inválido, endpoints inexistentes  
✅ **Almacenamiento**: Verificación de datos en memoria  

## Pruebas Manuales

También puedes usar la interfaz Swagger en `/docs` para probar todos los endpoints interactivamente, o utiliza curl/Postman con los ejemplos proporcionados.

Ejemplo con curl:
```bash
curl -X POST "http://localhost:8000/form/age" \
     -H "Content-Type: application/json" \
     -d '{"age": "25-35"}'
```
