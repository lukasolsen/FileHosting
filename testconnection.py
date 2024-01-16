from smb.SMBConnection import SMBConnection
import os
from dotenv import load_dotenv
load_dotenv()

conn = SMBConnection(os.getenv("smb_user"), os.getenv("smb_pass"), 'my_client',
                     'server_name', use_ntlm_v2=True)
conn.connect(os.getenv("smb_ip"), 139)


def list_files():
    files = conn.listPath(os.getenv("smb_name"), os.getenv("smb_path"))
    return [file.filename for file in files]


def download_file(filename):
    file_obj = open(filename, 'wb')
    conn.retrieveFile(os.getenv("smb_name"), os.getenv(
        "smb_path") + filename, file_obj)
    file_obj.close()


def upload_file(filepath):
    file_obj = open(filepath, 'rb')
    # ['path', 'to', 'file.txt'] -> ['file.txt']
    splitted_filename = filepath.split('/')
    filename = splitted_filename[-1]  # ['file.txt'] -> 'file.txt'

    conn.storeFile(os.getenv("smb_name"), os.getenv(
        "smb_path") + filename, file_obj)
    file_obj.close()


def main():
    try:
        files = list_files()
        print("Files in the network share:", files)

        download_file("game")
        print("File downloaded successfully")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if 'conn' in locals():
            conn.close()


if __name__ == "__main__":
    main()
