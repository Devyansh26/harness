from tools.file_tools import read_file, write_file, create_file, edit_file, append_to_file
from tools.shell_tools import run_command, list_directory
import json

TOOLS = [
    {  
        "type":"function",
        "name":"read_file",
        "description":"Reads the content of a file in the workspace.",
        "parameters":{
            "type":"object",
            "properties":{
                "path":{
                    "type":"string",
                    "description":"The relative path to the file in the workspace."
                }
            },
            "required":["path"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type":"function",
        "name":"write_file",
        "description":"Writes content to a file in the workspace.",
        "parameters":{
            "type":"object",
            "properties":{
                "path":{
                    "type":"string",
                    "description":"The relative path to the file in the workspace."
                },
                "content":{
                    "type":"string",
                    "description":"The content to write to the file."
                }
            },
            "required":["path", "content"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type":"function",
        "name":"create_file",
        "description":"Creates a new file in the workspace with the specified content.",
        "parameters":{
            "type":"object",
            "properties":{
                "path":{
                    "type":"string",
                    "description":"The relative path to the new file in the workspace."
                },
                "content":{
                    "type":"string",
                    "description":"The content to write to the new file."
                }
            },
            "required":["path", "content"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type":"function",
        "name":"edit_file",
        "description":"Edits the content of a file in the workspace.",
        "parameters":{
            "type":"object",
            "properties":{
                "path":{
                    "type":"string",
                    "description":"The relative path to the file in the workspace."
                },
                "previous_content":{
                    "type":"string",
                    "description":"The previous content of the file."
                },
                "new_content":{
                    "type":"string",
                    "description":"The new content to write to the file."
                }
            },
            "required":["path", "previous_content", "new_content"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type":"function",
        "name":"append_to_file",
        "description":"Appends content to a file in the workspace.",
        "parameters":{
            "type":"object",
            "properties":{
                "path":{
                    "type":"string",
                    "description":"The relative path to the file in the workspace."
                },
                "content":{
                    "type":"string",
                    "description":"The content to append to the file."
                }
            },
            "required":["path", "content"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "run_command",
        "description": (
            "Execute a Bash command in the workspace or a relative subdirectory. "
            "Supports shell commands, pipelines, redirection, grep, find, git, "
            "Python, virtual environments, package installation, builds and tests. "
            "Returns stdout, stderr, exit_code, duration_seconds and timed_out. "
            "A nonzero exit code indicates command failure; inspect the output "
            "and decide how to proceed. Each call starts a new shell."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The Bash command to execute."
                },
                "cwd": {
                    "type": ["string", "null"],
                    "description": (
                        "Working directory relative to the workspace, "
                        "or null to use the workspace root."
                    )
                },
                "timeout": {
                    "type": "integer",
                    "description": "Execution timeout in seconds, from 1 to 300."
                }
            },
            "required": ["command", "cwd", "timeout"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "list_directory",
        "description": "List file and directory names in a workspace directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "cwd": {
                    "type": ["string", "null"],
                    "description": (
                        "Directory relative to the workspace, "
                        "or null for the workspace root."
                    )
                }
            },
            "required": ["cwd"],
            "additionalProperties": False
        },
        "strict": True
    }
]

TOOLS_FUNCTIONS = {
    "read_file": read_file, 
    "write_file": write_file,
    "create_file": create_file,
    "edit_file": edit_file,
    "append_to_file": append_to_file,
    "run_command": run_command,
    "list_directory": list_directory,
}

def execute_tool(tool_name: str, arguments: object) -> str:
    if tool_name not in TOOLS_FUNCTIONS:
        raise ValueError(f"Tool '{tool_name}' is not available.")

    try:

        function = TOOLS_FUNCTIONS.get(tool_name)
        if not function:
            raise ValueError(f"Function for tool '{tool_name}' is not defined.")

        import inspect
        expected = set(inspect.signature(function).parameters.keys())

        if set(arguments.keys()) != expected:
            raise ValueError(f"Arguments do not match the expected parameters for tool '{tool_name}'.")


        result = function(**arguments)
        return json.dumps({"result": result})
    
    except Exception as e:
        return json.dumps({"error": str(e)})

