import os
import zipfile
import shutil

def package_repo():
    workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    parent_dir = os.path.abspath(os.path.join(workspace_dir, ".."))
    
    zip_targets = [
        os.path.join(parent_dir, "Multi-Tenant-Education-CRM-SaaS.zip"),
        os.path.join(parent_dir, "Multi-Tenant-Education-CRM-SaaS-Enterprise-v2.0.zip"),
        os.path.join(workspace_dir, "Multi-Tenant-Education-CRM-SaaS.zip"),
        os.path.join(workspace_dir, "Multi-Tenant-Education-CRM-SaaS-Enterprise-v2.0.zip"),
    ]
    
    # Target 1 first
    primary_zip = zip_targets[0]
    print(f"Creating primary archive: {primary_zip} from {workspace_dir}")
    
    ignore_dirs = {"__pycache__", ".pytest_cache", "node_modules", ".next"}
    
    total_files = 0
    with zipfile.ZipFile(primary_zip, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        for root, dirs, files in os.walk(workspace_dir):
            # Filter out ignored dirs
            dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.endswith(".egg-info")]
            
            for file in files:
                if file.endswith(".pyc") or file.endswith(".zip"):
                    continue
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, workspace_dir)
                zipf.write(file_path, rel_path)
                total_files += 1

    size_mb = os.path.getsize(primary_zip) / (1024 * 1024)
    print(f"Primary zip created: {size_mb:.2f} MB ({total_files} files)")

    for target in zip_targets[1:]:
        print(f"Copying to {target}...")
        shutil.copy2(primary_zip, target)
        
    print("All zip archives updated successfully!")

if __name__ == "__main__":
    package_repo()
