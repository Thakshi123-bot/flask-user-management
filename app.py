from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated database (dictionary)
users = {}

# GET: Retrieve all users or a specific user
@app.route('/users', methods=['GET'])
def get_users():
    user_id = request.args.get('id')  # Check for query parameter 'id'
    if user_id:
        # If an id is provided, try to fetch that specific user
        user = users.get(user_id)
        if user:
            return jsonify({'id': user_id, 'details': user}), 200
        return jsonify({'error': 'User not found'}), 404
    # If no 'id' is provided, return all users
    return jsonify(users), 200

# POST: Add new users
@app.route('/users', methods=['POST'])
def add_users():
    data = request.json  # Get the JSON data from the request body
    
    # Check if the incoming data is a list of users
    if isinstance(data, list):
        for user in data:
            user_id = user.get('id')
            details = user.get('details')
            if not user_id or not details:
                return jsonify({'error': 'Missing user id or details for some user'}), 400
            if user_id in users:
                return jsonify({'error': f'User with id {user_id} already exists'}), 400
            users[user_id] = details
        return jsonify({'message': 'Users added successfully'}), 201
    
    # If data is not a list, return an error
    return jsonify({'error': 'Expected an array of users'}), 400

# PUT: Update an existing user
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.json
    users[user_id] = data.get('details')  # Update user details
    return jsonify({'message': 'User updated successfully'}), 200

# DELETE: Remove a user
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    
    # Delete the user from the simulated database
    del users[user_id]
    return jsonify({'message': 'User deleted successfully'}), 200

if __name__ == '__main__':
    # Running the app on port 5001
    app.run(debug=True, port=5001)
