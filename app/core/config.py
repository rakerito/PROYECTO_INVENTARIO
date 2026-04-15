import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
# SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Faltan las variables SUPABASE_URL o SUPABASE_KEY en el archivo .env")
