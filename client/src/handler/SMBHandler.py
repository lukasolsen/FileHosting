import urllib.request
from smb.SMBConnection import SMBConnection
from smb.SMBHandler import SMBHandler
import os
import json


class SMBManager(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SMBManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        print("Initializing SMBManager", os.getenv("smb_user"))
        self.director = urllib.request.build_opener(SMBHandler)
        self.predefined_path = f'smb://{os.getenv("smb_user")}:{os.getenv("smb_pass")}@{os.getenv("smb_ip")}/{os.getenv("smb_name")}{os.getenv("smb_path")}'

        self.smb = SMBConnection(os.getenv("smb_user"), os.getenv("smb_pass"), 'file_hosting_api',
                                 'server_name', use_ntlm_v2=True)

        self.connect()

    def connect(self):
        try:
            self.smb.connect(os.getenv("smb_ip"),
                             os.getenv("smb_port"), timeout=30)
        except Exception as e:
            print("Error", e)

    def bytes_to_json(self, bytes):
        return json.loads(bytes.decode("utf-8"))

    def list_files(self, path=os.getenv("smb_path")):
        folders = self.smb.listPath(
            os.getenv("smb_name"), path)
        return [folder.filename for folder in folders if not folder.isDirectory]

    def find_items(self):
        files = self.list_files(os.getenv("smb_path") + "indexes/")

        for file in files:
            if file.endswith(".json"):
                print(self.predefined_path + "indexes/" + file)
                fh = self.director.open(
                    self.predefined_path + "indexes/" + file)
                data = fh.read()
                fh.close()
                return self.bytes_to_json(data)
        return None

    def find_item(self, id):
        files = self.list_files(os.getenv("smb_path") + "indexes/")

        for file in files:
            if file.endswith(".json"):
                fh = self.director.open(
                    self.predefined_path + "indexes/" + file)
                data = self.bytes_to_json(fh.read())
                fh.close()

                for item in data:
                    if int(item.get("id")) == int(id):
                        return item
        return None

    def download_file(self, filename):
        # Assuming SMBHandler is correctly implemented for retrieving files
        file_obj = open(filename, 'wb')
        try:
            fh = self.director.open(self.predefined_path + filename)
            file_obj.write(fh.read())
        finally:
            file_obj.close()

    def download_file_link(self, filename):
        # Returns a link to download the file from the SMB server
        return os.getenv("smb_ip") + os.getenv("smb_path") + filename

    def find_file_id(self, id):
        # Adjust this method based on your requirements
        # It currently seems to be commented out
        return None

    def upload_file(self, filepath):
        # Adjust this method based on your requirements
        # It currently seems to be commented out
        pass

    def correct_filepath(self, filepath):
        # Add the SMB stuff to it if it's not already there since this is a example of the path: "test.txt"
        return self.predefined_path + "files/" + filepath

    def close(self):
        # Assuming SMBHandler handles connection closure appropriately
        pass
