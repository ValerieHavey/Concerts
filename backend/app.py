from flask import Flask, jsonify, request, g
from flask_cors import CORS
from dotenv import load_dotenv
import os
import psycopg2, psycopg2.extras
import jwt
import bcrypt
from auth_middleware import token_required

load_dotenv()

app = Flask(__name__)
cors = CORS(app, origins='*')

def get_db_connection():
    connection = psycopg2.connect(
        host='localhost',
        database='concerttracker_db',
        user=os.environ('POSTGRES_USER'),
        password=os.environ('POSTGRES_PASSWORD'))
    return connection


# JWT Authentication

@app.route('/sign-token', methods=['GET'])
def sign_token():
    token = jwt.encode(user, os.getenv('JWT_SECRET'), algorithm="HS256")
    return jsonify({"token": token})



@app.route('/verify-token', methods=['POST'])
def verify_token():
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        decoded_token = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=["HS256"])
        return jsonify({"user": decoded_token})
    except Exception as err:
       return jsonify({"err": err})
    


@app.route('/auth/sign-up', methods=['POST'])
def sign_up():
    try:
        new_user_data = request.get_json()
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s;", (new_user_data["username"],))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.close()
            return jsonify({"err": "Username already taken"}), 400
        hashed_password = bcrypt.hashpw(bytes(new_user_data["password"], 'utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id, username", (new_user_data["username"], hashed_password.decode('utf-8')))
        created_user = cursor.fetchone()
        connection.commit()
        connection.close()
        # Construct the payload
        payload = {"username": created_user["username"], "id": created_user["id"]}
        # Create the token, attaching the payload
        token = jwt.encode({ "payload": payload }, os.getenv('JWT_SECRET'))
        # Send the token instead of the user
        return jsonify({"token": token}), 201
    except Exception as err:
        return jsonify({"err": str(err)}), 401
    


@app.route('/auth/sign-in', methods=["POST"])
def sign_in():
    try:
        sign_in_form_data = request.get_json()
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s;", (sign_in_form_data["username"]))
        existing_user = cursor.fetchone()
        if existing_user is None:
            return jsonify({"err": "Invalid credentials."}), 401
        password_is_valid = bcrypt.checkpw(bytes(sign_in_form_data["password"], 'utf-8'), bytes(existing_user["password"], 'utf-8'))
        if not password_is_valid:
            return jsonify({"err": "Invalid credentials."}), 401
        # Construct the payload
        payload = {"username": existing_user["username"], "id": existing_user["id"]}
        # Create the token, attaching the payload
        token = jwt.encode({ "payload": payload }, os.getenv('JWT_SECRET'))
        # Send the token instead of the user
        return jsonify({"token": token}), 200
    except Exception as err:
        return jsonify({"err": err.message}), 500
    finally:
        connection.close()

@app.route('/verify-token', methods=['POST'])
def verify_token():
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        decoded_token = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=["HS256"])
        return jsonify({decoded_token})
    except Exception as err:
       return jsonify({"err": err})
    

@app.route('/users')
@token_required
def users_index():
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT id, username FROM users;")
    users = cursor.fetchall()
    connection.close()
    return jsonify(users), 200

# Route that allows any user to view any other user's data:
@app.route('/users/<user_id>')
@token_required
def users_index(user_id):
    if user_id != g.user["id"]:
        return jsonify({"err": "Unauthorized"}), 403
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT id, username FROM users WHERE id = %s;", (user_id))
    user = cursor.fetchone()
    connection.close()
    if user is None:
        return jsonify({"err": "User not found"}), 404
    return jsonify(user), 200

    


# CRUD Routes
@app.route("/")
def index():
    return "Hello world"

@app.route('/concerts', methods= ['GET'])
def index():
  try:
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM concerts;")
    concerts = cursor.fetchall()
    connection.close()
    return concerts
  except:
     return "Application Error", 500
  

@app.route('/concerts', methods=['POST'])
def create_concert():
  try:
    new_concert = request.json
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("INSERT INTO concerts (headliner, openers, date, location) VALUES (%s, %s, %s, %s) RETURNING *", 
                   (new_concert['headliner'], new_concert['openers'], new_concert['date'], (new_concert['location'])))
    created_concert = cursor.fetchone()
    connection.commit()
    connection.close()
    return created_concert, 201
  except Exception as e:
     return str(e), 500
  
@app.route('/concerts/<concert_id>', methods=['GET'])
def show_concert(concert_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM concerts WHERE id = %s", (concert_id,))
        concert = cursor.fetchone()
        if concert is None:
            connection.close()
            return "Concert Not Found", 404
        connection.close()
        return concert, 200
    except Exception as e:
        return str(e), 500
    

@app.route('/concerts/<concert_id>', methods=['DELETE'])
def delete_concert(concert_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("DELETE FROM concerts WHERE id = %s", (concert_id,))
        if cursor.rowcount == 0:
            return "Concert not found", 404
        connection.commit()
        cursor.close()
        return "Concert deleted successfully", 204
    except Exception as e:
        return str(e), 500


@app.route('/concerts/<concert_id>', methods=['PUT'])
def update_concert(concert_id):
    try:
      connection = get_db_connection()
      cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      cursor.execute("UPDATE concerts SET headliner = %s, openers = %s, date = %s, location = %s WHERE id = %s RETURNING *", (request.json['headliner'], request.json['openers'], request.json['date'], request.json['location'], concert_id))
      updated_concert = cursor.fetchone()
      if updated_concert is None:
        return "Concert Not Found", 404
      connection.commit()
      connection.close()
      return updated_concert, 202
    except Exception as e:
      return str(e), 500


app.run(debug=True, port=8080)