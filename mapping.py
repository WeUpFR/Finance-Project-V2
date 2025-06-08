import json
from typing import Dict, Any

def load_mapping_template(file_path: str) -> Dict[str, Any]:
    """
    Loads the account-to-financial-statement mapping from a JSON file.

    Args:
        file_path (str): The path to the mapping JSON file.

    Returns:
        Dict[str, Any]: A dictionary representing the mapping structure.
    """
    try:
        with open(file_path, 'r') as f:
            mapping = json.load(f)
        print(f"Successfully loaded mapping template from {file_path}")
        return mapping
    except FileNotFoundError:
        print(f"Error: The mapping file '{file_path}' was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: The mapping file '{file_path}' is not a valid JSON file.")
        return {}
