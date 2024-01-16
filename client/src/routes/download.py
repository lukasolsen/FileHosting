import os
from flask import Blueprint, jsonify, send_file, request
from flask_jwt_extended import jwt_required
from src import utils
from src.handler.FileHandler import FileHandler
import datetime

download = Blueprint('download', __name__)

download_links = {}


@download.route('/items')
@jwt_required()
def items():
    offset = request.args.get('offset', default=0, type=int)
    limit = request.args.get('limit', default=10, type=int)

    downloads = FileHandler().list_files(limit=limit, offset=offset)

    return {"downloads": downloads}


@download.route('/item/<fileid>')
@jwt_required()
def item(fileid):
    # Check if the id exist
    item = FileHandler().find_item(fileid)
    if not item:
        return {"message": "Item not found"}, 404

    file_path = item.get("path")
    if not file_path:
        return {"message": "Item not found"}, 404

    # Generate a download link
    token = utils.generate_download_token(file_path)
    utils.DOWNLOAD_LINKS[token] = file_path

    return jsonify({"download_link": f"/download/download_redirect/{token}"})


@download.route("/download_redirect/<token>")
def download_redirect(token):
    if not utils.is_valid_token(token):
        return {"message": "Invalid token"}, 404

    file_path = utils.get_file_identifier(token)
    print(file_path)

    return send_file(file_path, as_attachment=True)
