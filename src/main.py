import os
import json
import hashlib
from flask import Flask, request, jsonify, send_file
from flask_httpauth import HTTPBasicAuth

# Configuration
LFS_STORAGE_PATH = os.getenv("LFS_STORAGE_PATH", "/data/lfs")
USERNAME = "user"
PASSWORD = "password"

# Ensure the storage directory exists
os.makedirs(LFS_STORAGE_PATH, exist_ok=True)

app = Flask(__name__)
auth = HTTPBasicAuth()

# Hardcoded user authentication (for simplicity)
@auth.verify_password
def verify_password(username, password):
    return username == USERNAME and password == PASSWORD

def get_file_path(oid):
    """Returns the storage path of the LFS object based on its OID (SHA-256 hash)."""
    return os.path.join(os.getcwd(), LFS_STORAGE_PATH, oid)

@app.route('/objects/batch', methods=['POST'])
@auth.login_required
def batch():
    """Handles the Git LFS batch API."""
    data = request.get_json()
    operation = data.get("operation")
    objects = data.get("objects", [])

    response_objects = []
    for obj in objects:
        oid = obj["oid"]
        size = obj["size"]
        file_path = get_file_path(oid)
        
        if operation == "download":
            if os.path.exists(file_path):
                response_objects.append({
                    "oid": oid,
                    "size": size,
                    "actions": {
                        "download": {
                            "href": f"{request.host_url}objects/{oid}",
                            "expires_at": "2026-01-01T00:00:00Z"
                        }
                    }
                })
            else:
                return jsonify({"message": "Object not found", "oid": oid}), 404
        
        elif operation == "upload":
            response_objects.append({
                "oid": oid,
                "size": size,
                "actions": {
                    "upload": {
                        "href": f"{request.host_url}objects/{oid}",
                        "expires_at": "2026-01-01T00:00:00Z"
                    }
                }
            })

    return jsonify({"objects": response_objects})

@app.route('/objects/<oid>', methods=['PUT'])
@auth.login_required
def upload(oid):
    """Handles uploading LFS objects."""
    file_path = get_file_path(oid)
    
    with open(file_path, "wb") as f:
        f.write(request.data)
    
    return "", 200

@app.route('/objects/<oid>', methods=['GET'])
@auth.login_required
def download(oid):
    """Handles downloading LFS objects."""
    file_path = get_file_path(oid)

    if not os.path.exists(file_path):
        return jsonify({"message": "File not found"}), 404

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
