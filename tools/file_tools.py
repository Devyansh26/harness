from pathlib import Path

WORKSPACE = (Path.cwd() / "workspace").resolve()

def resolve_path(path: str) -> Path:
    target = (WORKSPACE / path).resolve()
    if not target.exists():
        raise FileNotFoundError(f"File not found: {target}")
    return target

# print(resolve_path("test.txt"))

def read_file(path: str) -> str:
    target = resolve_path(path)

    if not target.is_file():
        raise ValueError(f"Path is not a file: {target}")

    if target.name.lower() in {".env", ".env.local", "credentials.json"}:
        raise ValueError(f"Access to file is restricted: {target}")

    with open(target, "r", encoding="utf-8") as f:
        return f.read()

# result = read_file("test.txt")
# print(result)

def write_file(path: str, content: str) -> None:
    target = resolve_path(path)

    
    if not target.is_file():
        
        raise ValueError(f"Path is not a file: {target}")

    if target.name.lower() in {".env", ".env.local", "credentials.json"}:
        raise ValueError(f"Access to file is restricted: {target}")

    with open(target, "w", encoding="utf-8") as f:
        f.write(content)

    return f"Successfully wrote to file: {target}"  

# write_file("test.txt", "Hello, World!")