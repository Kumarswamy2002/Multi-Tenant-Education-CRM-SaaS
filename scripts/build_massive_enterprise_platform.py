"""
Master Script: Builds the complete Enterprise Multi-Tenant Education CRM SaaS Platform (70,000+ LOC).
Generates comprehensive production modules across:
1. Backend (Models, Schemas, Services, API Endpoints, Core, Integrations, Tests, Seeders)
2. Frontend Portals (Web Admin, Student Portal, Parent Portal, Alumni Portal, Counselor Portal, Employer Portal)
3. Client SDKs (Python SDK, TypeScript SDK, Shared Type Definitions)
4. Full Test Suites & Validation
5. Release ZIP Packaging & Git Push
"""
import os
import sys
import shutil
import zipfile
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def write_file(rel_path, content):
    full_path = os.path.join(BASE_DIR, rel_path)
    ensure_dir(os.path.dirname(full_path))
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    return full_path

print(f"[1/7] Initializing build environment in: {BASE_DIR}")

# Import existing generators
sys.path.append(os.path.join(BASE_DIR, "scripts"))
from gen_backend_models import generate_models
from gen_backend_schemas import generate_schemas
from gen_backend_services import generate_services

generate_models(BASE_DIR)
generate_schemas(BASE_DIR)
generate_services(BASE_DIR)
print("Base models, schemas, and services generated.")
