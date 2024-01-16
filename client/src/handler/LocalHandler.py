import os
import json


class LocalManager:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(LocalManager, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.local_path = os.getenv("local_path")

    def list_folders(self):
        return os.listdir(self.local_path)

    def find_items(self):
        indexes_path = os.path.join(self.local_path, "indexes")
        items = []

        for item in os.listdir(indexes_path):
            item_path = os.path.join(indexes_path, item)
            if os.path.isfile(item_path):
                # This is a JSON or CSV file
                if item.endswith(".json"):
                    items.append(self.read_manifest(item_path))
            else:
                print("This is a folder")
                break

        return items

    def find_item(self, id):
        indexes_path = os.path.join(self.local_path, "indexes")

        for item in os.listdir(indexes_path):
            item_path = os.path.join(indexes_path, item)
            if os.path.isfile(item_path):
                # This is a JSON or CSV file
                if item.endswith(".json"):
                    manifest = self.read_manifest(item_path)
                    for item in manifest:
                        if int(item.get("id")) == int(id):
                            return item
            else:
                print("This is a folder")
                break

        return None

    def file_exists(self, filepath):
        return os.path.exists(filepath)

    def read_manifest(self, filepath):
        with open(filepath, "r") as f:
            return json.load(f)
