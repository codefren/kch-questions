#!/usr/bin/env python3
"""
Script para inicializar la base de datos PostgreSQL para KCH Forms API
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuración de la base de datos
DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_NAME = "kacha-questions"

# URL de conexión para crear la base de datos (sin especificar la DB)
ADMIN_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"
# URL de conexión final
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def test_postgresql_connection():
    """Prueba la conexión a PostgreSQL"""
    try:
        logger.info("Probando conexión a PostgreSQL...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database="postgres"  # Conectar a la DB por defecto
        )
        conn.close()
        logger.info("✅ Conexión a PostgreSQL exitosa")
        return True
    except psycopg2.Error as e:
        logger.error(f"❌ Error conectando a PostgreSQL: {e}")
        return False


def create_database():
    """Crea la base de datos si no existe"""
    try:
        logger.info(f"Creando base de datos '{DB_NAME}'...")
        
        # Conectar a PostgreSQL con la base de datos por defecto
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar si la base de datos ya existe
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_NAME,))
        exists = cursor.fetchone()
        
        if exists:
            logger.info(f"✅ La base de datos '{DB_NAME}' ya existe")
        else:
            # Crear la base de datos
            cursor.execute(f'CREATE DATABASE "{DB_NAME}"')
            logger.info(f"✅ Base de datos '{DB_NAME}' creada exitosamente")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        logger.error(f"❌ Error creando la base de datos: {e}")
        return False


def create_tables():
    """Crea las tablas usando SQLAlchemy"""
    try:
        logger.info("Creando tablas...")
        
        # Importar después de que la base de datos exista
        from database import Base, engine, create_tables as db_create_tables
        
        # Crear todas las tablas
        db_create_tables()
        logger.info("✅ Tablas creadas exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creando las tablas: {e}")
        return False


def verify_tables():
    """Verifica que las tablas se hayan creado correctamente"""
    try:
        logger.info("Verificando tablas...")
        
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            # Verificar que la tabla form_submissions existe
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'form_submissions'
            """))
            
            if result.fetchone():
                logger.info("✅ Tabla 'form_submissions' verificada")
                
                # Mostrar estructura de la tabla
                result = conn.execute(text("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns 
                    WHERE table_name = 'form_submissions'
                    ORDER BY ordinal_position
                """))
                
                columns = result.fetchall()
                logger.info("📋 Estructura de la tabla 'form_submissions':")
                for column in columns:
                    logger.info(f"  - {column[0]}: {column[1]} ({'NULL' if column[2] == 'YES' else 'NOT NULL'})")
                
                return True
            else:
                logger.error("❌ Tabla 'form_submissions' no encontrada")
                return False
                
    except Exception as e:
        logger.error(f"❌ Error verificando las tablas: {e}")
        return False


def main():
    """Función principal para inicializar la base de datos"""
    logger.info("🚀 Iniciando configuración de la base de datos...")
    
    # Paso 1: Probar conexión a PostgreSQL
    if not test_postgresql_connection():
        logger.error("No se pudo conectar a PostgreSQL. Verifica que esté ejecutándose.")
        sys.exit(1)
    
    # Paso 2: Crear la base de datos
    if not create_database():
        logger.error("No se pudo crear la base de datos.")
        sys.exit(1)
    
    # Paso 3: Crear las tablas
    if not create_tables():
        logger.error("No se pudieron crear las tablas.")
        sys.exit(1)
    
    # Paso 4: Verificar las tablas
    if not verify_tables():
        logger.error("No se pudieron verificar las tablas.")
        sys.exit(1)
    
    logger.info("🎉 ¡Base de datos inicializada exitosamente!")
    logger.info(f"📍 URL de conexión: {DATABASE_URL}")
    logger.info("🔧 Para usar en tu aplicación, exporta:")
    logger.info(f"   export DATABASE_URL={DATABASE_URL}")


if __name__ == "__main__":
    main()
