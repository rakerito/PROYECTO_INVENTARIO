from fastapi import FastAPI

app = FastAPI()


products = [
    {"id": "1", "name": "Laptop", "price": 1200.0},
    {"id": "2", "name": "Mouse", "price": 25.0},
    {"id": "3", "name": "Teclado", "price": 50.0},
    {"id": "4", "name": "Monitor", "price": 300.0},
    {"id": "5", "name": "USB", "price": 10.0},
    {"id": "6", "name": "Audífonos", "price": 80.0},
    {"id": "7", "name": "Webcam", "price": 60.0},
    {"id": "8", "name": "Impresora", "price": 200.0},
    {"id": "9", "name": "Tablet", "price": 250.0},
    {"id": "10", "name": "Celular", "price": 500.0},
    {"id": "11", "name": "Cargador", "price": 20.0},
    {"id": "12", "name": "Bocina", "price": 90.0},
]

@app.get("/products")
def get_products():
    return products

@app.get("/products/{product_id}")
def get_product(product_id: str):
    return next((p for p in products if p["id"] == product_id), {"error": "No encontrado"})