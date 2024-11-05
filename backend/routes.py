from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for pic in data:
        if pic["id"] == id:
            return jsonify(pic), 200
    return jsonify({"msg": "No such resource."}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    pic = request.get_json()

    for existing_pic in data:
        if existing_pic["id"] == pic["id"]:
            return jsonify({"Message": f"picture with id {pic['id']} already present"}), 302
    
    data.append(pic)
    # with open(json_url, "w") as f:
    #     f.write(json.dumps(data))
    return jsonify(pic), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pic = request.get_json()
    for i, p in enumerate(data):
        if p["id"] == pic["id"] == id:
            data[i] = pic
            return jsonify({"msg": "updated the picture"}), 200
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for i, pic in enumerate(data):
        if pic["id"] == id:
            del data[i]
            return jsonify({"message": "pic removed"}), 204
    return jsonify({"message": "picture not found"}), 404
