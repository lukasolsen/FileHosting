import os
from ftplib import FTP


class FTPManager(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FTPManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.ftp_host = os.getenv('ftp_host')
        self.ftp_port = os.getenv('ftp_port')
        self.ftp_user = os.getenv('ftp_user')
        self.ftp_password = os.getenv('ftp_password')
        self.ftp_path = os.getenv('ftp_path')
        self.ftp = FTP(self.ftp_host, self.ftp_user, self.ftp_password)
        self.ftp.set_pasv(True)
        self.ftp.login(self.ftp_user, self.ftp_password)

    def list_files(self):
        return self.ftp.nlst()

    def list_folders(self):
        return self.ftp.nlst()

    def download_file(self, filepath):
        self.ftp.retrbinary('RETR ' + filepath, open(filepath, 'wb').write)

    def file_exists(self, filepath):
        try:
            self.ftp.cwd(filepath)
        except Exception as e:
            print("Error", e)
            return False

        return True

    def find_items(self):
        # Find each folder in the wanted directory and read the manifest.json if it exists.
        folders = self.list_folders()
        manifests = []

        for folder in folders:
            # Go into the folder and check if the manifest.json exist, if it does, read it.
            self.ftp.cwd(folder)
            manifest_path = os.path.join(folder, 'manifest.json')
            if not self.file_exists(manifest_path):
                print("Manifest not found", manifest_path)
                continue

            print("Reading file")
            manifest = self.read_file(manifest_path)

            if manifest:
                manifests.append(manifest)

            # Go back to the root directory.
            self.ftp.cwd(self.ftp_path)

        return manifests

    def read_file(self, filepath):
        try:
            with open(filepath, 'wb') as file:
                self.ftp.retrbinary('RETR ' + filepath, file.write)
        except Exception as e:
            print("Error", e)
            return None

        return self.parse_manifest(filepath)
