import os
import uuid
import json
import shutil

import datetime

UPLOAD_FOLDER = 'uploads'
AUTH_EXPIRATION_TIME = datetime.timedelta(days=7)  # 7 days


def file_exists(filename):
    return os.path.exists(os.path.join(UPLOAD_FOLDER, filename))


def find_information(foldername):
    """Returns the manifest.json file for the given foldername"""
    manifest_path = os.path.join(UPLOAD_FOLDER, foldername, 'manifest.json')

    if not os.path.exists(manifest_path):
        return None

    return get_manifest(manifest_path)


def find_upload(id):
    for root, dirs, files in os.walk(UPLOAD_FOLDER):
        manifest_path = os.path.join(root, 'manifest.json')

        if not os.path.exists(manifest_path):
            continue

        manifest = get_manifest(manifest_path)

        if manifest and int(manifest["id"]) == int(id):
            return manifest

    return None


def find_upload_path(id):
    for root, dirs, files in os.walk(UPLOAD_FOLDER):
        manifest_path = os.path.join(root, 'manifest.json')

        if not os.path.exists(manifest_path):
            continue

        manifest = get_manifest(manifest_path)

        if manifest and int(manifest.get("id")) == int(id):
            return root

    return None


def get_manifest(manifest_path):
    data = {}

    with open(manifest_path, 'r') as f:
        data = json.load(f)

    # Append information about the file
    data["files"] = [filename for filename in os.listdir(os.path.dirname(manifest_path))
                     if filename != 'manifest.json']

    return data


def generate_uuid():
    return str(uuid.uuid4())


def list_uploads(limit=10, offset=0):
    """Returns a list of manifest contents for the given limit and offset"""
    folders = sorted(os.listdir(UPLOAD_FOLDER))[offset:offset + limit]

    return [get_manifest(os.path.join(UPLOAD_FOLDER, folder, 'manifest.json')) for folder in folders]


def zip_folder(path):
    """Zips the given folder"""
    zip_filename = f"{os.path.basename(path)}.zip"
    zip_path = os.path.join(os.environ['TEMP'], zip_filename)

    try:
        shutil.make_archive(
            zip_path[:-4], 'zip', os.path.dirname(path), os.path.basename(path))
    except Exception as e:
        return {"message": f"Error zipping folder: {str(e)}"}, 500

    return zip_path
