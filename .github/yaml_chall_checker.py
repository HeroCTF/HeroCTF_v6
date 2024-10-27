import os
import sys
import yaml
from yaml.loader import SafeLoader


REQUIRED_ATTRIBUTES = ["name", "author", "category", "description", "value", "type", "flags", "tags", "state", "version"]
OPTIONAL_ATTRIBUTES = ["image", "host", "hints", "files", "requirements", "extra"]
REQUIRED_CATEGORIES = [
    "Blockchain",
    "Crypto",
    "Forensics",
    "Forensic",
    "Misc",
    "OSINT",
    "Prog",
    "Pwn",
    "Reverse",
    "Sponsors",
    "Steganography",
    "System",
    "Web"
]

def find_challenge_files(directory: str) -> list[str]:
    """Find all challenge.yml files in subdirectories"""
    challenge_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file == "challenge.yml":
                challenge_files.append(os.path.join(root, file))
    return challenge_files

def syntax_check(challenge_file: str) -> None:
    """Validate the syntax, attributes, and types of a 'challenge.yml' file"""
    print(f"Checking syntax of '{challenge_file}'...")
    try:
        with open(os.path.join(challenge_file), "r") as f:
            yaml_data = yaml.load(f, Loader=SafeLoader)

        missing_attributes = []
        for attribute in REQUIRED_ATTRIBUTES:
            if attribute not in yaml_data:
                missing_attributes.append(attribute)

        if missing_attributes:
            print(f"Missing required attributes: {', '.join(missing_attributes)}")

        for key, value in yaml_data.items():
            if key not in REQUIRED_ATTRIBUTES + OPTIONAL_ATTRIBUTES:
                print(f"Unknown attribute '{key}'")

            match key:
                case "name":
                    if not isinstance(value, str):
                        print(f"Attribute '{key}' is not a string")
                case "author":
                    if not isinstance(value, str):
                        print(f"Attribute '{key}' is not a string")
                case "category":
                    if value not in REQUIRED_CATEGORIES:
                        print(f"Attribute '{key}' is not a valid category")
                case "description":
                    if not isinstance(value, str):
                        print(f"Attribute '{key}' is not a string")
                case "value":
                    if not (isinstance(value, int) or value is None):
                        print(f"Attribute '{key}' is not an integer or None")
                case "type":
                    if value != "dynamic":
                        print(f"Attribute '{key}' is not 'dynamic'")
                case "extra":
                    if not isinstance(value, dict):
                        print(f"Attribute '{key}' is not a dictionary")
                    if "initial" not in value or "decay" not in value or "minimum" not in value:
                        print(f"Attribute '{key}' is missing required sub-attributes")
                    if not isinstance(value["initial"], int) or not isinstance(value["decay"], int) or not isinstance(value["minimum"], int):
                        print(f"Attribute '{key}' sub-attributes are not integers")
                    if value["initial"] != 500:
                        print(f"Attribute '{key}' sub-attribute 'initial' is not 500")
                    if value["decay"] != 100:
                        print(f"Attribute '{key}' sub-attribute 'decay' is not 100")
                    if value["minimum"] < 1 or value["minimum"] > 50:
                        print(f"Attribute '{key}' sub-attribute 'minimum' is not between 1 and 50")
                case "image":
                    if value is not None:
                        print(f"Attribute '{key}' is not None")
                case "host":
                    if value is not None:
                        print(f"Attribute '{key}' is not None")
                case "flags":
                    if not isinstance(value, list):
                        print(f"Attribute '{key}' is not a list")
                case "tags":
                    if not isinstance(value, list):
                        print(f"Attribute '{key}' is not a list")
                case "files":
                    if not (isinstance(value, list) or value is None):
                        print(f"Attribute '{key}' is not a list or None")
                case "state":
                    if value not in ["hidden", "visible"]:
                        print(f"Attribute '{key}' is not 'hidden' or 'visible'")
                case "version":
                    if not isinstance(value, str):
                        print(f"Attribute '{key}' is not a string")
                case "requirements":
                    if not isinstance(value, list):
                        print(f"Attribute '{key}' is not a list")
                case "hints":
                    if not isinstance(value, list):
                        print(f"Attribute '{key}' is not a list")

        print("Syntax is valid")
    except yaml.YAMLError as exc:
        print(f"Syntax is invalid: {exc}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python yaml_chall_checker.py <directory>")
        sys.exit(1)

    challenge_files = find_challenge_files(sys.argv[1])
    for challenge_file in challenge_files:
        syntax_check(challenge_file)
