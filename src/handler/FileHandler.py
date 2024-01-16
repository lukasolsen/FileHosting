import os
from src.handler.SMBHandler import SMBHandler


class FileHandler:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FileHandler, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.type = os.getenv("location_type")

    def list_files(self):
        print("Calling here..", self.type)
        if self.type == "local":
            return self.list_files_local()
        elif self.type == "SMB":
            return SMBHandler().find_items()

        return []

    def list_files_local(self):
        return os.listdir(os.getenv("local_path"))

    def download_file(self, filename):
        if self.type == "local":
            return self.download_file_local(filename)
        elif self.type == "smb":
            print("Downloading file from SMB")
            return SMBHandler().download_file_link(filename)

        return None

    def find_upload_id(self, id):
        if self.type == "local":
            return self.find_upload_id_local(id)
        elif self.type == "smb":
            return self.find_upload_id_smb(id)

        return None
