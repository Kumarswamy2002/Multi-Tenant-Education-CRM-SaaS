"""
Full Enterprise System Generator for Multi-Tenant Education CRM SaaS.
Generates comprehensive production modules across backend, portals, SDKs, seeders, and tests.
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def write_file(rel_path, content):
    full_path = os.path.join(BASE_DIR, rel_path)
    ensure_dir(os.path.dirname(full_path))
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    return full_path

# Execute backend models and schemas generators
print("Step 1: Generating Backend Models & Schemas...")
from gen_backend_models import generate_models
from gen_backend_schemas import generate_schemas
generate_models(BASE_DIR)
generate_schemas(BASE_DIR)
print("Models and Schemas done.")
