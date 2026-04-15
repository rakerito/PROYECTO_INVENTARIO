from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from app.core.config import SUPABASE_URL, SUPABASE_KEY
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI(title="Inventario API")

# CORS para permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE = "products"

# ── Modelos ────────────────────────────────────────────────────────────────────

class ProductCreate(BaseModel):
    name: str
    quantity: int
    ingreso_date: Optional[str] = None   # formato "YYYY-MM-DD"
    min_stock: int
    max_stock: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    ingreso_date: Optional[str] = None
    min_stock: Optional[int] = None
    max_stock: Optional[int] = None

# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.get("/products/")
def get_products(limit: int = 20, offset: int = 0):
    """Devuelve la lista paginada de productos con total."""
    try:
        # Una sola query con count="exact" — forma correcta en supabase-py v2
        res = (
            supabase.table(TABLE)
            .select("*", count="exact")
            .order("created_at", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )
        total = res.count if res.count is not None else len(res.data)
        return {"total": total, "items": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/products/{product_id}")
def get_product(product_id: str):
    """Devuelve un producto por su UUID."""
    try:
        res = supabase.table(TABLE).select("*").eq("id", product_id).single().execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return res.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/products/", status_code=201)
def create_product(product: ProductCreate):
    """Crea un nuevo producto."""
    try:
        data = product.model_dump()
        data["id"] = str(uuid.uuid4())
        res = supabase.table(TABLE).insert(data).execute()
        return res.data[0] if res.data else {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/products/{product_id}")
def update_product(product_id: str, product: ProductUpdate):
    """Actualiza un producto por su UUID."""
    try:
        data = {k: v for k, v in product.model_dump().items() if v is not None}
        if not data:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
        res = supabase.table(TABLE).update(data).eq("id", product_id).execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return res.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    """Elimina un producto por su UUID."""
    try:
        res = supabase.table(TABLE).delete().eq("id", product_id).execute()
        return {"deleted": True, "id": product_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))