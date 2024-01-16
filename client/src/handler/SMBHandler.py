import urllib
from smb.SMBConnection import SMBConnection
from smb.SMBHandler import SMBHandler
import os
from pathlib import Path


class SMBManager(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SMBManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        print("Initializing SMBManager", os.getenv("smb_user"))
        self.smb = SMBConnection(os.getenv("smb_user"), os.getenv("smb_pass"), 'my_client',
                                 'server_name', use_ntlm_v2=True)

        self.connect()

    def connect(self):
        try:
            self.smb.connect(os.getenv("smb_ip"),
                             os.getenv("smb_port"), timeout=30)
        except Exception as e:
            print("Error", e)

    def list_files(self, path=os.getenv("smb_path")):
        files = self.smb.listPath(os.getenv("smb_name"), path)
        return [file.filename for file in files]

    def list_folders(self):
        folders = self.smb.listPath(
            os.getenv("smb_name"), os.getenv("smb_path"))
        return [folder.filename for folder in folders if folder.isDirectory]

    def find_items(self):
        folders = self.list_folders()
        manifests = []
        for folder in folders:
            folder_path = os.path.join(folder)

            manifest_path = os.path.join(folder_path, 'manifest.json')

            if not self.file_exists(manifest_path):
                print("Manifest not found", manifest_path)
                continue

            print("Reading file")
            manifest = self.read_file(manifest_path)

            if manifest:
                manifests.append(manifest)

        return manifests

    def file_exists(self, filepath):
        try:
            if (self.smb.getAttributes(os.getenv("smb_name"), filepath).isDirectory):
                return False
        except Exception as e:
            print("Error", e)
            return False

        return True

    def read_file(self, filepath):
        # Read the actual contents of the file, then parse it as JSON
        try:
            file_obj = open(Path(filepath).resolve(), 'rb')
            data = file_obj.read()
            file_obj.close()
            return data

        except Exception as e:
            print("Error", e)
            return None

    def download_file(self, filename):
        file_obj = open(filename, 'wb')
        self.smb.retrieveFile(os.getenv("smb_name"), os.getenv(
            "smb_path") + filename, file_obj)
        file_obj.close()

    def download_file_link(self, filename):
        # Returns a link to download the file from the SMB server
        return os.getenv("smb_ip") + os.getenv("smb_path") + filename

    def find_file_id(self, id):
        for root, dirs, files in os.walk(os.getenv("smb_path")):
            if not os.path.exists(os.path.join(root, 'manifest.json')):
                continue

            # manifest = get_manifest(os.path.join(root, 'manifest.json'))

            # if manifest and int(manifest.get("id")) == int(id):
            #    return root

        return None

    def upload_file(self, filepath):
        file_obj = open(filepath, 'rb')
        # ['path', 'to', 'file.txt'] -> ['file.txt']
        splitted_filename = filepath.split('/')
        filename = splitted_filename[-1]  # ['file.txt'] -> 'file.txt'

        self.smb.storeFile(os.getenv("smb_name"), os.getenv(
            "smb_path") + filename, file_obj)
        file_obj.close()

    def close(self):
        self.smb.close()
