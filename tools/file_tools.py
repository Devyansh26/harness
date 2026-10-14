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

def create_file(path: str, content: str) -> None:
    target = (WORKSPACE / path).resolve()

    if target.exists():
        raise ValueError(f"File already exists: {target}")

    if target.name.lower() in {".env", ".env.local", "credentials.json"}:
        raise ValueError(f"Access to file is restricted: {target}")

    target.parent.mkdir(parents=True, exist_ok=True)

    with open(target, "w", encoding="utf-8") as f:
        f.write(content)

    return f"Successfully created file: {target}"

def edit_file(path: str, previous_content: str, new_content: str) -> None:  
    
    target = resolve_path(path)

    if not target.is_file():
        raise ValueError(f"Path is not a file: {target}")

    if target.name.lower() in {".env", ".env.local", "credentials.json"}:
        raise ValueError(f"Access to file is restricted: {target}")

    with open(target, "r", encoding="utf-8") as f:
        current_content = f.read()

    if current_content != previous_content:
        raise ValueError(f"File content has changed since last read. Current content: {current_content}")

    with open(target, "w", encoding="utf-8") as f:
        f.write(new_content)

    return f"Successfully edited file: {target}"


def append_to_file(path: str, content: str) -> None:
    target = resolve_path(path)

    if not target.is_file():
        raise ValueError(f"Path is not a file: {target}")

    if target.name.lower() in {".env", ".env.local", "credentials.json"}:
        raise ValueError(f"Access to file is restricted: {target}")

    with open(target, "a", encoding="utf-8") as f:
        f.write(content)

    return f"Successfully appended to file: {target}"