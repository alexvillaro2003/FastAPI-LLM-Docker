from fastapi.testclient import TestClient
from api_model import app

client = TestClient(app)

def test_get_recommendations_valid():
     
     input_data = {
          "tipo": "libro",
          "edad": "adulto",
          "genero": "comedia",
          "cantidad": 3
     }

     response = client.post("/get_recommendations", json=input_data)

     
     assert response.status_code == 200
     
     assert "result" in response.json()

def test_get_recommendations_invalid_edad():
     
     input_data = {
          "tipo": "libro",
          "edad": "anciano",  
          "genero": "comedia",
          "cantidad": 3
     }

     
     response = client.post("/get_recommendations", json=input_data)

     
     assert response.status_code == 422
     
     assert response.json() == {"detail": "La edad 'anciano' no es válida. Los valores permitidos son: infantil, juvenil, adulto."}

def test_get_recommendations_invalid_cantidad():
     
     input_data = {
          "tipo": "libro",
          "edad": "adulto",
          "genero": "comedia",
          "cantidad": 7  
     }


     response = client.post("/get_recommendations", json=input_data)

     assert response.status_code == 422

     assert response.json() == {"detail": "La cantidad máxima permitida es 6."}
