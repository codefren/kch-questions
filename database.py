"""
Database configuration and models for KCH Forms API
"""

import os
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone

# Database URL - configurable via environment variable
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/kacha-questions"
)

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class FormSubmission(Base):
    """
    Tabla principal para almacenar todas las respuestas de formularios
    """
    __tablename__ = "form_submissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    form = Column(String(50), nullable=False, index=True)
    received_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    data = Column(JSON, nullable=False)
    
    # Campos específicos para facilitar consultas y reportes
    # Edad
    age_range = Column(String(10), nullable=True, index=True)
    
    # Datos personales
    customer_name = Column(String(255), nullable=True, index=True)
    street = Column(String(255), nullable=True)
    number = Column(String(20), nullable=True)
    floor = Column(String(20), nullable=True)
    door = Column(String(20), nullable=True)
    stair = Column(String(20), nullable=True)
    
    # Identificación
    document_type = Column(String(50), nullable=True)
    document_number = Column(String(50), nullable=True, index=True)
    phone = Column(String(50), nullable=True, index=True)
    
    # Marketing
    discovery_source = Column(String(100), nullable=True, index=True)
    favorite_store = Column(String(100), nullable=True, index=True)
    delivery_type = Column(String(100), nullable=True, index=True)
    
    # Productos (almacenado como JSON pero también como texto para búsquedas)
    products_text = Column(Text, nullable=True)  # Para búsquedas full-text
    
    # Promociones
    weekly_promos_answer = Column(String(100), nullable=True, index=True)
    
    # Contacto
    email = Column(String(255), nullable=True, index=True)
    large_family = Column(Boolean, nullable=True, index=True)


def create_tables():
    """Crear todas las tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency para obtener una sesión de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def extract_fields_from_data(form_type: str, data: dict) -> dict:
    """
    Extrae campos específicos del JSON data para almacenarlos en columnas separadas
    Esto facilita las consultas y reportes
    """
    fields = {}
    
    if form_type == "age":
        fields["age_range"] = data.get("age")
    
    elif form_type == "personal-data":
        fields["customer_name"] = data.get("name")
        fields["street"] = data.get("street")
        fields["number"] = data.get("number")
        fields["floor"] = data.get("floor")
        fields["door"] = data.get("door")
        fields["stair"] = data.get("stair")
    
    elif form_type == "identification":
        fields["document_type"] = data.get("document_type")
        fields["document_number"] = data.get("document_number")
        fields["phone"] = data.get("phone")
    
    elif form_type == "discovery":
        fields["discovery_source"] = data.get("source")
    
    elif form_type == "favorite-store":
        fields["favorite_store"] = data.get("store")
    
    elif form_type == "delivery-type":
        fields["delivery_type"] = data.get("service_type")
    
    elif form_type == "products":
        products = data.get("products", [])
        fields["products_text"] = ", ".join(products) if products else None
    
    elif form_type == "weekly-promos-knowledge":
        fields["weekly_promos_answer"] = data.get("answer")
    
    elif form_type == "contact":
        fields["email"] = data.get("email")
        fields["large_family"] = data.get("large_family")
    
    return fields
