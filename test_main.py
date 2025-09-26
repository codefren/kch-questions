import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import json

from main import app, DB

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    """Limpia la base de datos en memoria antes de cada test"""
    DB.clear()
    yield
    DB.clear()


class TestAgeEndpoint:
    """Tests para el endpoint /form/age"""
    
    def test_submit_age_valid(self):
        response = client.post("/form/age", json={"age": "25-35"})
        assert response.status_code == 200
        
        data = response.json()
        assert data["form"] == "age"
        assert data["data"]["age"] == "25-35"
        assert "id" in data
        assert "received_at" in data
        
        # Verificar que se guardó en DB
        assert len(DB) == 1
        assert list(DB.values())[0]["form"] == "age"
    
    def test_submit_age_all_options(self):
        """Test todas las opciones válidas de edad"""
        valid_ages = ["18-24", "25-35", "35-44", "45+"]
        
        for age in valid_ages:
            response = client.post("/form/age", json={"age": age})
            assert response.status_code == 200
            assert response.json()["data"]["age"] == age
    
    def test_submit_age_invalid(self):
        response = client.post("/form/age", json={"age": "invalid-age"})
        assert response.status_code == 422
    
    def test_submit_age_missing_field(self):
        response = client.post("/form/age", json={})
        assert response.status_code == 422


class TestPersonalDataEndpoint:
    """Tests para el endpoint /form/personal-data"""
    
    def test_submit_personal_data_complete(self):
        payload = {
            "name": "Ana Pérez",
            "street": "Gran Vía",
            "number": "123",
            "floor": "4",
            "door": "B",
            "stair": "2"
        }
        
        response = client.post("/form/personal-data", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["form"] == "personal-data"
        assert data["data"]["name"] == "Ana Pérez"
        assert data["data"]["street"] == "Gran Vía"
        assert data["data"]["number"] == "123"
        assert data["data"]["floor"] == "4"
        assert data["data"]["door"] == "B"
        assert data["data"]["stair"] == "2"
    
    def test_submit_personal_data_minimal(self):
        """Test con campos mínimos requeridos"""
        payload = {
            "name": "Juan García",
            "street": "Calle Mayor",
            "number": "456"
        }
        
        response = client.post("/form/personal-data", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["data"]["name"] == "Juan García"
        assert data["data"]["floor"] is None
        assert data["data"]["door"] is None
        assert data["data"]["stair"] is None
    
    def test_submit_personal_data_empty_name(self):
        payload = {
            "name": "",
            "street": "Calle Mayor",
            "number": "456"
        }
        
        response = client.post("/form/personal-data", json=payload)
        assert response.status_code == 422
    
    def test_submit_personal_data_whitespace_trimming(self):
        """Test que se eliminan espacios en blanco"""
        payload = {
            "name": "  María López  ",
            "street": "  Avenida Central  ",
            "number": "  789  "
        }
        
        response = client.post("/form/personal-data", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["data"]["name"] == "María López"
        assert data["data"]["street"] == "Avenida Central"
        assert data["data"]["number"] == "789"


class TestIdentificationEndpoint:
    """Tests para el endpoint /form/identification"""
    
    def test_submit_identification_valid(self):
        payload = {
            "document_type": "DNI",
            "document_number": "12345678Z",
            "phone": "+34 600 123 456"
        }
        
        response = client.post("/form/identification", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["form"] == "identification"
        assert data["data"]["document_type"] == "DNI"
        assert data["data"]["document_number"] == "12345678Z"
        assert data["data"]["phone"] == "+34 600 123 456"
    
    def test_submit_identification_different_document_types(self):
        """Test diferentes tipos de documento"""
        document_types = ["DNI", "NIE", "Pasaporte", "Cedula"]
        
        for doc_type in document_types:
            payload = {
                "document_type": doc_type,
                "document_number": "ABC123456",
                "phone": "600123456"
            }
            
            response = client.post("/form/identification", json=payload)
            assert response.status_code == 200
            assert response.json()["data"]["document_type"] == doc_type
    
    def test_submit_identification_phone_formats(self):
        """Test diferentes formatos de teléfono válidos"""
        valid_phones = [
            "+34 600 123 456",
            "600123456",
            "+1-555-123-4567",
            "(555) 123-4567",
            "+44 20 7946 0958"
        ]
        
        for phone in valid_phones:
            payload = {
                "document_type": "DNI",
                "document_number": "12345678Z",
                "phone": phone
            }
            
            response = client.post("/form/identification", json=payload)
            assert response.status_code == 200, f"Failed for phone: {phone}"
    
    def test_submit_identification_invalid_phone(self):
        """Test teléfonos inválidos"""
        invalid_phones = ["123", "abc", ""]
        
        for phone in invalid_phones:
            payload = {
                "document_type": "DNI",
                "document_number": "12345678Z",
                "phone": phone
            }
            
            response = client.post("/form/identification", json=payload)
            assert response.status_code == 422


class TestDiscoveryEndpoint:
    """Tests para el endpoint /form/discovery"""
    
    def test_submit_discovery_valid(self):
        sources = ["Instagram", "Google", "Amigos", "Folleto", "Facebook", "TikTok"]
        
        for source in sources:
            payload = {"source": source}
            response = client.post("/form/discovery", json=payload)
            assert response.status_code == 200
            assert response.json()["data"]["source"] == source
    
    def test_submit_discovery_empty_source(self):
        response = client.post("/form/discovery", json={"source": ""})
        assert response.status_code == 422


class TestFavoriteStoreEndpoint:
    """Tests para el endpoint /form/favorite-store"""
    
    def test_submit_favorite_store_valid(self):
        stores = ["KCH Centro", "KCH Norte", "KCH Sur", "KCH Online"]
        
        for store in stores:
            payload = {"store": store}
            response = client.post("/form/favorite-store", json=payload)
            assert response.status_code == 200
            assert response.json()["data"]["store"] == store


class TestDeliveryTypeEndpoint:
    """Tests para el endpoint /form/delivery-type"""
    
    def test_submit_delivery_type_valid(self):
        service_types = ["Envío estándar", "Express", "Recogida en tienda", "Same day"]
        
        for service_type in service_types:
            payload = {"service_type": service_type}
            response = client.post("/form/delivery-type", json=payload)
            assert response.status_code == 200
            assert response.json()["data"]["service_type"] == service_type


class TestProductsEndpoint:
    """Tests para el endpoint /form/products"""
    
    def test_submit_products_valid(self):
        payload = {"products": ["Champú", "Acondicionador", "Serum"]}
        
        response = client.post("/form/products", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["form"] == "products"
        assert data["data"]["products"] == ["Champú", "Acondicionador", "Serum"]
    
    def test_submit_products_single_item(self):
        payload = {"products": ["Champú"]}
        
        response = client.post("/form/products", json=payload)
        assert response.status_code == 200
        assert len(response.json()["data"]["products"]) == 1
    
    def test_submit_products_empty_list(self):
        payload = {"products": []}
        
        response = client.post("/form/products", json=payload)
        assert response.status_code == 422
    
    def test_submit_products_empty_strings(self):
        """Test que no se permiten strings vacíos en la lista"""
        payload = {"products": ["Champú", "", "Serum"]}
        
        response = client.post("/form/products", json=payload)
        assert response.status_code == 422


class TestWeeklyPromosKnowledgeEndpoint:
    """Tests para el endpoint /form/weekly-promos-knowledge"""
    
    def test_submit_weekly_promos_knowledge_valid(self):
        answers = ["Sí", "No", "Algo", "Un poco", "Bastante"]
        
        for answer in answers:
            payload = {"answer": answer}
            response = client.post("/form/weekly-promos-knowledge", json=payload)
            assert response.status_code == 200
            assert response.json()["data"]["answer"] == answer


class TestContactEndpoint:
    """Tests para el endpoint /form/contact"""
    
    def test_submit_contact_valid(self):
        payload = {
            "email": "ana@example.com",
            "large_family": True
        }
        
        response = client.post("/form/contact", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["form"] == "contact"
        assert data["data"]["email"] == "ana@example.com"
        assert data["data"]["large_family"] is True
    
    def test_submit_contact_large_family_false(self):
        payload = {
            "email": "juan@test.com",
            "large_family": False
        }
        
        response = client.post("/form/contact", json=payload)
        assert response.status_code == 200
        assert response.json()["data"]["large_family"] is False
    
    def test_submit_contact_invalid_email(self):
        invalid_emails = ["invalid-email", "test@", "@example.com", ""]
        
        for email in invalid_emails:
            payload = {
                "email": email,
                "large_family": True
            }
            
            response = client.post("/form/contact", json=payload)
            assert response.status_code == 422


class TestDebugEndpoint:
    """Tests para el endpoint /debug/dump"""
    
    def test_debug_dump_empty(self):
        response = client.get("/debug/dump")
        assert response.status_code == 200
        
        data = response.json()
        assert data["count"] == 0
        assert data["items"] == {}
    
    def test_debug_dump_with_data(self):
        # Agregar algunos datos
        client.post("/form/age", json={"age": "25-35"})
        client.post("/form/discovery", json={"source": "Instagram"})
        
        response = client.get("/debug/dump")
        assert response.status_code == 200
        
        data = response.json()
        assert data["count"] == 2
        assert len(data["items"]) == 2


class TestResponseFormat:
    """Tests para verificar el formato de respuesta común"""
    
    def test_response_format_consistency(self):
        """Verifica que todas las respuestas tengan el formato correcto"""
        endpoints_and_payloads = [
            ("/form/age", {"age": "25-35"}),
            ("/form/personal-data", {"name": "Test", "street": "Test St", "number": "123"}),
            ("/form/identification", {"document_type": "DNI", "document_number": "123", "phone": "600123456"}),
            ("/form/discovery", {"source": "Instagram"}),
            ("/form/favorite-store", {"store": "KCH Centro"}),
            ("/form/delivery-type", {"service_type": "Express"}),
            ("/form/products", {"products": ["Test Product"]}),
            ("/form/weekly-promos-knowledge", {"answer": "Sí"}),
            ("/form/contact", {"email": "test@example.com", "large_family": True}),
        ]
        
        for endpoint, payload in endpoints_and_payloads:
            response = client.post(endpoint, json=payload)
            assert response.status_code == 200
            
            data = response.json()
            
            # Verificar campos obligatorios
            assert "id" in data
            assert "form" in data
            assert "received_at" in data
            assert "data" in data
            
            # Verificar tipos
            assert isinstance(data["id"], str)
            assert isinstance(data["form"], str)
            assert isinstance(data["received_at"], str)
            assert isinstance(data["data"], dict)
            
            # Verificar formato de fecha
            datetime.fromisoformat(data["received_at"].replace("Z", "+00:00"))


class TestErrorHandling:
    """Tests para manejo de errores"""
    
    def test_invalid_json(self):
        """Test con JSON inválido"""
        response = client.post(
            "/form/age",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_missing_content_type(self):
        """Test sin Content-Type"""
        response = client.post("/form/age", data='{"age": "25-35"}')
        # FastAPI maneja esto automáticamente, debería funcionar
        assert response.status_code in [200, 422]
    
    def test_nonexistent_endpoint(self):
        """Test endpoint que no existe"""
        response = client.post("/form/nonexistent", json={"test": "data"})
        assert response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
