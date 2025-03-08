from flask import Flask, request, jsonify
import bcrypt
import jwt
import datetime
import pickle

app = Flask(__name__)

# Secret key for JWT
SECRET_KEY = "your_secret_key_here"

# In-memory user storage (for demonstration purposes)
users = {}
def save_db():
    with open('db.pkl', 'wb') as f:
        pickle.dump(users, f)

def load_db():
    global users
    try:
        with open('db.pkl', 'rb') as f:
            users = pickle.load(f)
    except FileNotFoundError:
        users = {}




# Helper function to generate JWT token
def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Helper function to verify JWT token
def verify_token(token):
    try:
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Signup route
@app.route("/signup", methods=["POST"])
def signup():
    payload = request.json
    username = payload.get("username")
    password = payload.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if username in users:
        return jsonify({"error": "Username already exists"}), 400

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    users[username] = {"password": hashed_password}

    save_db()

    return jsonify({"message": "User created successfully"}), 201

# Login route
@app.route("/login", methods=["POST"])
def login():
    payload = request.json
    username = payload.get("username")
    password = payload.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = users.get(username)
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

    # Generate JWT token
    token = generate_token(username)
    return jsonify({"token": token}), 200

# Delete user route
@app.route("/delete", methods=["DELETE"])
def delete_user():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is required"}), 401

    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401

    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    # Delete the user
    del users[user_id]
    return jsonify({"message": "User deleted successfully"}), 200

    # Route to check the validity of the user
@app.route("/me", methods=["GET"])
def me():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is required"}), 401

    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Invalid or expired token"}), 401

    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user_id": user_id}), 200

if __name__ == "__main__":
    # Load the database when the application starts
    load_db()
    app.run(debug=True)