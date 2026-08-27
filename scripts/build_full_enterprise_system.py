"""
Master Enterprise Codebase Generator for Multi-Tenant Education CRM SaaS.
Builds complete backend services, API routers, core systems, frontend portals,
Python/TS SDKs, seeders, test suites, verifies LOC count (70k+), packages ZIP, and pushes to Git.
"""
import os
import sys
import shutil
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

print("Starting Enterprise Suite generation...")
