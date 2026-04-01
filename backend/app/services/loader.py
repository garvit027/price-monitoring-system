import os
import json

DATASET_PATH = "backend/dataset"

def load_products():
    for filename in os.listdir(DATASET_PATH):
        if not filename.endswith(".json"):
            continue

        file_path = os.path.join(DATASET_PATH, filename)

        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            yield data, filename

        except Exception as e:
            print(f"Error reading {filename}: {e}")