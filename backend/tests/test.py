import json
path = "courses_data.json"

with open(path, "r") as f:
    input_data = json.load(f)
print(input_data)