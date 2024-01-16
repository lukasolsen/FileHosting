import os
from src.handler.SMBHandler import SMBManager
from src.handler.LocalHandler import LocalManager


class FileHandler:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FileHandler, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.type = os.getenv("location_type")


    def list_files(self, limit=10, offset=0):
        if self.type.lower() == "local":
            return LocalManager().find_items()
        elif self.type.lower() == "smb":
            return SMBManager().find_items()

        return []

    def find_item(self, id):  # id is the folder name
        if self.type.lower() == "local":
            return LocalManager().find_item(id)
        elif self.type.lower() == "smb":
            return SMBManager().find_item(id)

        return None
