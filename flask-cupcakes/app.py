from flask import Flask, jsonify, request
from models import db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.app = app
db.init_app(app)

# This route lists all cupcakes, retreives 
# data from the database and returns it in JSON format
@app.route('/api/cupcakes', methods=['GET'])
def list_cupcakes():
    cupcakes = Cupcake.query.all()
    cupcake_list = [{'id': cupcake.id, 'flavor': cupcake.flavor, 'size': cupcake.size, 'rating': cupcake.rating, 'image': cupcake.image} for cupcake in cupcakes]
    return jsonify(cupcakes=cupcake_list)

# Retreives data about a single cupcake by 
# it's ID and returns it in JSON format, if not found, returns 404
@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET'])
def get_cupcake(cupcake_id):
    cupcake = Cupcake.query.get(cupcake_id)
    if cupcake is None:
        return jsonify(message="Cupcake not found"), 404
    return jsonify(cupcake={'id': cupcake.id, 'flavor': cupcake.flavor, 'size': cupcake.size, 'rating': cupcake.rating, 'image': cupcake.image})

# Creates new cupcake using the data from the 
# request body and returns the created cupcake's data in JSOn format
@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    data = request.json
    flavor = data.get('flavor')
    size = data.get('size')
    rating = data.get('rating')
    image = data.get('image', "https://tinyurl.com/demo-cupcake")

    if not flavor or not size or rating is None:
        return jsonify(message="Incomplete data. Please provide flavor, size, and rating."), 400

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()

    return jsonify(cupcake={'id': new_cupcake.id, 'flavor': new_cupcake.flavor, 'size': new_cupcake.size, 'rating': new_cupcake.rating, 'image': new_cupcake.image}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

