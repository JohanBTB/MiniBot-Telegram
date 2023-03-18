import subprocess
import json

def generate_environment_json(file_path):
    result = subprocess.run(["pip", "freeze"], stdout=subprocess.PIPE)
    libraries = result.stdout.decode("utf-8").strip().split("\n")
    environment = {}
    for library in libraries:
        name, version = library.split("==")
        environment[name] = version
    with open(file_path, "w") as f:
        json.dump(environment, f)

generate_environment_json(r"D:\\")