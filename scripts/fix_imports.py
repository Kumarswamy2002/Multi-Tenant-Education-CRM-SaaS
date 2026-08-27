import os

base_dir = r"d:\ElevateIQ\github projectr -2\backend\app"

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            if "from backend.app" in content or "import backend.app" in content:
                new_content = content.replace("from backend.app.", "from app.").replace("import backend.app.", "import app.")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Fixed: {file}")

print("All imports unified to `app.`")
