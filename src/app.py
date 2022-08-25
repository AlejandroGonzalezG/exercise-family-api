"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    
    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def create_member():
    first_name = request.json.get('first_name')
    lucky_numbers = request.json.get('lucky_numbers')
    age = request.json.get('age')

    if not first_name: return jsonify({'error': 400})
    if not lucky_numbers: return jsonify({'error': 400})
    if not age: return jsonify({'error': 400})
    
    nuevoMiembro = {
            'id': request.json.get('id') if request.json.get('id') is not None else jackson_family._generateId(),
            'first_name': first_name,
            'last_name': jackson_family.last_name,
            'age': age,
            'lucky_numbers': lucky_numbers
            }
    response = jackson_family.add_member(nuevoMiembro)

    return jsonify({'message': response})

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):

    miembro = jackson_family.get_member(id)
    if miembro:
        return jsonify(miembro), 200
    else:
        return jsonify({"error": 400}) 

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    miembro = jackson_family.get_member(id)
    
    if miembro:
        jackson_family.delete_member(id)
        return jsonify({"status_code": 200, "done": True})
    
    if not miembro:
        return jsonify({"status_code": 400, "done": False})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
