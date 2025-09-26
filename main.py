"""
KCH – Formularios de captación: Especificación mejorada
=======================================================
Objetivo: exponer **9 endpoints** (uno por pregunta/formulario) para recopilar datos de clientes.
Cada endpoint:
  - Método: **POST** (idempotencia no requerida; se considera una captura de respuesta).
  - Cuerpo: JSON con los campos descritos.
  - Respuesta: eco del payload validado + metadatos (timestamp, formulario, id).
  - Validación estricta de tipos y opciones.
  - Ejemplos en OpenAPI para facilitar pruebas desde `/docs`.
  - Tag por categoría para mantener la documentación ordenada.

Requisitos funcionales por endpoint
-----------------------------------
1) **Edad**  
   - Ruta: `/form/age`  
   - Campo: `age` (enum) con opciones **"18-24", "25-35", "35-44", "45+"**.

2) **Datos personales**  
   - Ruta: `/form/personal-data`  
   - Campos: `name` (str), `street` (str), `number` (str|int como str), `floor` (str|None), `door` (str|None), `stair` (str|None).

3) **Identificación**  
   - Ruta: `/form/identification`  
   - Campos: `document_type` (str, p.ej. "DNI", "NIE", "Pasaporte"), `document_number` (str), `phone` (str con validación básica E.164 o local).

4) **¿Cómo te enteraste de que KCH tiene descuentos?**  
   - Ruta: `/form/discovery`  
   - Campo: `source` (str) p.ej. "Instagram", "Google", "Amigos", "Folleto", etc.

5) **¿Qué tienda visitas más?**  
   - Ruta: `/form/favorite-store`  
   - Campo: `store` (str).

6) **Tipo de servicio a domicilio**  
   - Ruta: `/form/delivery-type`  
   - Campo: `service_type` (str) p.ej. "Envío estándar", "Express", "Recogida en tienda".

7) **¿Qué productos deseas comprar?**  
   - Ruta: `/form/products`  
   - Campo: `products` (list[str], mínimo 1).

8) **¿Conoces las promociones semanales?**  
   - Ruta: `/form/weekly-promos-knowledge`  
   - Campo: `answer` (str) p.ej. "Sí", "No", "Algo".

9) **Contacto adicional**  
   - Ruta: `/form/contact`  
   - Campos: `email` (EmailStr), `large_family` (bool) — indica si tiene familia numerosa.

Notas técnicas
--------------
- Framework: FastAPI (Pydantic v2).
- CORS abierto para facilitar pruebas (ajustar en producción).
- Almacenamiento: en memoria (dict) a modo de demo; sustituir por DB más adelante.
- Se proveen ejemplos y descripciones en los modelos para una mejor DX en Swagger UI.
- Nombres de variables en inglés para alinearse con la preferencia del usuario.

"""

from enum import Enum
from typing import List, Optional
from uuid import uuid4
from datetime import datetime, timezone

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr, constr
from sqlalchemy.orm import Session
from sqlalchemy import text

from database import get_db, create_tables, FormSubmission, extract_fields_from_data

app = FastAPI(
    title="KCH – Formularios de Captación",
    description=(
        "API de ejemplo con 9 endpoints (uno por pregunta de formulario) "
        "para capturar respuestas de clientes con validación y ejemplos."
    ),
    version="1.0.0",
)

# CORS (ajustar allow_origins en producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------
# Utilidades comunes
# -----------------
class FormResponse(BaseModel):
    id: str = Field(..., description="Identificador único de la respuesta")
    form: str = Field(..., description="Nombre del formulario / endpoint")
    received_at: datetime = Field(..., description="Fecha ISO de recepción (UTC)")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "f9d0b4e2-9a9a-4fa7-9c6c-5c3b7bc9e123",
                "form": "age",
                "received_at": "2025-09-26T12:00:00Z",
            }
        }

# Crear tablas al iniciar la aplicación
create_tables()


def make_meta(form: str) -> FormResponse:
    return FormResponse(
        id=str(uuid4()),
        form=form,
        received_at=datetime.now(timezone.utc),
    )


# 1) Edad
class AgeEnum(str, Enum):
    a_18_24 = "18-24"
    a_25_35 = "25-35"
    a_35_44 = "35-44"
    a_45_plus = "45+"


class AgePayload(BaseModel):
    age: AgeEnum = Field(..., description="Rango de edad")

    class Config:
        json_schema_extra = {"example": {"age": "25-35"}}


class AgeResponse(FormResponse):
    data: AgePayload


@app.post("/form/age", response_model=AgeResponse, tags=["01 – Edad"])
async def submit_age(payload: AgePayload, db: Session = Depends(get_db)):
    meta = make_meta("age")
    data_dict = payload.model_dump()
    
    # Extraer campos específicos
    specific_fields = extract_fields_from_data("age", data_dict)
    
    # Crear registro en la base de datos
    db_submission = FormSubmission(
        id=meta.id,
        form=meta.form,
        received_at=meta.received_at,
        data=data_dict,
        **specific_fields
    )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    return AgeResponse(**meta.model_dump(), data=payload)


# 2) Datos personales
class PersonalDataPayload(BaseModel):
    name: constr(strip_whitespace=True, min_length=1) = Field(..., description="Nombre completo")
    street: constr(strip_whitespace=True, min_length=1) = Field(..., description="Calle")
    number: constr(strip_whitespace=True, min_length=1) = Field(..., description="Número de portal (como texto)")
    floor: Optional[constr(strip_whitespace=True, min_length=1)] = Field(None, description="Piso")
    door: Optional[constr(strip_whitespace=True, min_length=1)] = Field(None, description="Puerta")
    stair: Optional[constr(strip_whitespace=True, min_length=1)] = Field(None, description="Escalera")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Ana Pérez",
                "street": "Gran Vía",
                "number": "123",
                "floor": "4",
                "door": "B",
                "stair": "2",
            }
        }


class PersonalDataResponse(FormResponse):
    data: PersonalDataPayload


@app.post("/form/personal-data", response_model=PersonalDataResponse, tags=["02 – Datos personales"])
async def submit_personal_data(payload: PersonalDataPayload, db: Session = Depends(get_db)):
    meta = make_meta("personal-data")
    data_dict = payload.model_dump()
    
    specific_fields = extract_fields_from_data("personal-data", data_dict)
    
    db_submission = FormSubmission(
        id=meta.id,
        form=meta.form,
        received_at=meta.received_at,
        data=data_dict,
        **specific_fields
    )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    return PersonalDataResponse(**meta.model_dump(), data=payload)


# 3) Identificación
class IdentificationPayload(BaseModel):
    document_type: constr(strip_whitespace=True, min_length=2) = Field(
        ..., description="Tipo de documento (DNI, NIE, Pasaporte, etc.)"
    )
    document_number: constr(strip_whitespace=True, min_length=3) = Field(
        ..., description="Número de documento"
    )
    phone: constr(strip_whitespace=True, min_length=6, pattern=r"^[+]?[- 0-9()]{6,}$") = Field(
        ..., description="Teléfono (se acepta formato local o E.164)")

    class Config:
        json_schema_extra = {
            "example": {
                "document_type": "DNI",
                "document_number": "12345678Z",
                "phone": "+34 600 123 456",
            }
        }


class IdentificationResponse(FormResponse):
    data: IdentificationPayload


@app.post("/form/identification", response_model=IdentificationResponse, tags=["03 – Identificación"])
async def submit_identification(payload: IdentificationPayload, db: Session = Depends(get_db)):
    meta = make_meta("identification")
    data_dict = payload.model_dump()
    
    specific_fields = extract_fields_from_data("identification", data_dict)
    
    db_submission = FormSubmission(
        id=meta.id,
        form=meta.form,
        received_at=meta.received_at,
        data=data_dict,
        **specific_fields
    )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    return IdentificationResponse(**meta.model_dump(), data=payload)


# 4) Descubrimiento de descuentos
class DiscoveryPayload(BaseModel):
    source: constr(strip_whitespace=True, min_length=2) = Field(
        ..., description="¿Cómo te enteraste de los descuentos?"
    )

    class Config:
        json_schema_extra = {"example": {"source": "Instagram"}}


class DiscoveryResponse(FormResponse):
    data: DiscoveryPayload


@app.post("/form/discovery", response_model=DiscoveryResponse, tags=["04 – Marketing / Descubrimiento"])
async def submit_discovery(payload: DiscoveryPayload, db: Session = Depends(get_db)):
    meta = make_meta("discovery")
    data_dict = payload.model_dump()
    
    specific_fields = extract_fields_from_data("discovery", data_dict)
    
    db_submission = FormSubmission(
        id=meta.id,
        form=meta.form,
        received_at=meta.received_at,
        data=data_dict,
        **specific_fields
    )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    return DiscoveryResponse(**meta.model_dump(), data=payload)


# 5) Tienda favorita
class FavoriteStorePayload(BaseModel):
    store: constr(strip_whitespace=True, min_length=1) = Field(..., description="Tienda que visita más")

    class Config:
        json_schema_extra = {"example": {"store": "KCH Centro"}}


class FavoriteStoreResponse(FormResponse):
    data: FavoriteStorePayload


@app.post("/form/favorite-store", response_model=FavoriteStoreResponse, tags=["05 – Preferencias de tienda"])
async def submit_favorite_store(payload: FavoriteStorePayload, db: Session = Depends(get_db)):
    meta = make_meta("favorite-store")
    data_dict = payload.model_dump()
    
    specific_fields = extract_fields_from_data("favorite-store", data_dict)
    
    db_submission = FormSubmission(
        id=meta.id,
        form=meta.form,
        received_at=meta.received_at,
        data=data_dict,
        **specific_fields
    )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    return FavoriteStoreResponse(**meta.model_dump(), data=payload)


# 6) Tipo de servicio a domicilio
class DeliveryTypePayload(BaseModel):
    service_type: constr(strip_whitespace=True, min_length=2) = Field(
        ..., description="Tipo de servicio a domicilio"
    )

    class Config:
        json_schema_extra = {"example": {"service_type": "Express"}}


class DeliveryTypeResponse(FormResponse):
    data: DeliveryTypePayload


@app.post("/form/delivery-type", response_model=DeliveryTypeResponse, tags=["06 – Envíos"])
async def submit_delivery_type(payload: DeliveryTypePayload, db: Session = Depends(get_db)):
    meta = make_meta("delivery-type")
    data_dict = payload.model_dump()
    
    specific_fields = extract_fields_from_data("delivery-type", data_dict)
    
    db_submission = FormSubmission(
        id=meta.id,
        form=meta.form,
        received_at=meta.received_at,
        data=data_dict,
        **specific_fields
    )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    return DeliveryTypeResponse(**meta.model_dump(), data=payload)


# 7) Lista de productos a comprar
class ProductsPayload(BaseModel):
    products: List[constr(strip_whitespace=True, min_length=1)] = Field(
        ..., min_length=1, description="Listado de productos de interés"
    )

    class Config:
        json_schema_extra = {"example": {"products": ["Champú", "Acondicionador", "Serum"]}}


class ProductsResponse(FormResponse):
    data: ProductsPayload


@app.post("/form/products", response_model=ProductsResponse, tags=["07 – Productos"])
async def submit_products(payload: ProductsPayload, db: Session = Depends(get_db)):
    meta = make_meta("products")
    data_dict = payload.model_dump()
    
    specific_fields = extract_fields_from_data("products", data_dict)
    
    db_submission = FormSubmission(
        id=meta.id,
        form=meta.form,
        received_at=meta.received_at,
        data=data_dict,
        **specific_fields
    )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    return ProductsResponse(**meta.model_dump(), data=payload)


# 8) Conocimiento de promociones semanales
class WeeklyPromosKnowledgePayload(BaseModel):
    answer: constr(strip_whitespace=True, min_length=1) = Field(
        ..., description="Respuesta a si conoces las promociones semanales (Sí/No/…)"
    )

    class Config:
        json_schema_extra = {"example": {"answer": "Sí"}}


class WeeklyPromosKnowledgeResponse(FormResponse):
    data: WeeklyPromosKnowledgePayload


@app.post(
    "/form/weekly-promos-knowledge",
    response_model=WeeklyPromosKnowledgeResponse,
    tags=["08 – Promociones"],
)
async def submit_weekly_promos_knowledge(payload: WeeklyPromosKnowledgePayload, db: Session = Depends(get_db)):
    meta = make_meta("weekly-promos-knowledge")
    data_dict = payload.model_dump()
    
    specific_fields = extract_fields_from_data("weekly-promos-knowledge", data_dict)
    
    db_submission = FormSubmission(
        id=meta.id,
        form=meta.form,
        received_at=meta.received_at,
        data=data_dict,
        **specific_fields
    )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    return WeeklyPromosKnowledgeResponse(**meta.model_dump(), data=payload)


# 9) Contacto adicional (email + familia numerosa)
class ContactPayload(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico")
    large_family: bool = Field(..., description="¿Tiene familia numerosa? true/false")

    class Config:
        json_schema_extra = {"example": {"email": "ana@example.com", "large_family": True}}


class ContactResponse(FormResponse):
    data: ContactPayload


@app.post("/form/contact", response_model=ContactResponse, tags=["09 – Contacto"])
async def submit_contact(payload: ContactPayload, db: Session = Depends(get_db)):
    meta = make_meta("contact")
    data_dict = payload.model_dump()
    
    specific_fields = extract_fields_from_data("contact", data_dict)
    
    db_submission = FormSubmission(
        id=meta.id,
        form=meta.form,
        received_at=meta.received_at,
        data=data_dict,
        **specific_fields
    )
    
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    return ContactResponse(**meta.model_dump(), data=payload)


# Endpoint utilitario para ver (demo) los datos en memoria (no usar en prod)
class DebugDump(BaseModel):
    count: int
    items: dict


@app.get("/debug/dump", response_model=DebugDump, tags=["_debug"])
async def dump(db: Session = Depends(get_db)):
    submissions = db.query(FormSubmission).all()
    items = {}
    for submission in submissions:
        items[str(submission.id)] = {
            "form": submission.form,
            "data": submission.data,
            "received_at": submission.received_at.isoformat()
        }
    return DebugDump(count=len(submissions), items=items)


# Health check endpoint for Docker
@app.get("/health", tags=["_system"])
async def health_check():
    """Health check endpoint for Docker container monitoring"""
    try:
        # Test database connection
        from database import engine
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
