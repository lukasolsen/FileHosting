import os
from flask import Blueprint, jsonify, send_from_directory, request
from flask_jwt_extended import jwt_required
from src import utils

download = Blueprint('download', __name__)

download_links = {}


@download.route('/items')
@jwt_required()
def items():
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', default=10, type=int)

    downloads = utils.list_uploads(limit, offset)

    return {"downloads": downloads}


@download.route('/item/<fileid>')
@jwt_required()
def item(fileid):
    # Check if the id exist
    manifest = utils.find_upload(fileid)
    if not manifest:
        return {"message": "Item not found"}, 404

    download_uuid = utils.generate_uuid()

    # Store the UUID and associate it with the filename
    # You may want to store this mapping in the database or a separate data structure
    # For simplicity, let's use a global dictionary (consider using a more robust solution in production)
    download_links[download_uuid] = fileid

    return jsonify(download_link=download_uuid)


@download.route("/download_redirect/<uuid>")
def download_redirect(uuid):
    fileid = download_links.get(uuid)

    if fileid:
        download_links.pop(uuid, None)

        path = utils.find_upload_path(fileid)

        if not path:
            return {"message": "Invalid or expired download link"}, 404

        # Zip the folder
        zip_path = utils.zip_folder(path)
        name = os.path.basename(zip_path) # get the name of the zip file

        print(zip_path, name)

        # Send the zipped folder
        return send_from_directory(zip_path, name, as_attachment=True)
    else:
        return {"message": "Invalid or expired download link"}, 404
