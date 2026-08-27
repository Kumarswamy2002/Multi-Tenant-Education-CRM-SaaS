"""
Enterprise Code Generator for Multi-Tenant Education CRM SaaS.
Generates full-scale production modules across Backend, 6 Frontend Portals,
Python SDK, TypeScript SDK, Shared Types, Integration Clients, Test Suites, and Seeders.
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Written: {os.path.relpath(path, BASE_DIR)}")

print(f"Base Directory: {BASE_DIR}")
