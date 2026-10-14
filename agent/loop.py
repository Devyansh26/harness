from tools.file_tools import read_file, write_file, create_file, edit_file, append_to_file
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
    }
]

TOOLS_FUNCTIONS = {
    "read_file": read_file, 
    "write_file": write_file,
    "create_file": create_file,
    "edit_file": edit_file,
    "append_to_file": append_to_file
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

