from flask import Flask, jsonify, request, g, render_template, abort
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
import psycopg2, psycopg2.extras
import jwt
import bcrypt
from auth_middleware import token_required
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin123@localhost/concerttracker_db'
cors = CORS(app, origins='*')
# db=SQLAlchemy(app)


def get_db_connection():
    connection = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST','localhost'),
        database=os.getenv('POSTGRES_DATABASE','concerttracker_db'),
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'])
    return connection

# class Concert(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     headliner = db.Column(db.String(100), nullable=False)
#     openers = db.Column(db.String(200), nullable=True)
#     date = db.Column(db.DateTime, nullable=False)
#     location = db.Column(db.String(100), nullable=False)
#     notes = db.Column(db.String(500), nullable=True)

    # def __repr__(self):
    #     return f"Concert: {self.headliner}"
    
    # def __init__(self, headliner, openers, date, location, notes):
    #     self.headliner = headliner


# JWT Authentication

@app.route('/sign-token', methods=['GET'])
def sign_token():
    token = jwt.encode(user, os.getenv('JWT_SECRET'), algorithm="HS256")
    return jsonify({"token": token})


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
        payload = {"username": created_user["username"], "id": created_user["id"]}       
        token = jwt.encode({ "payload": payload }, os.getenv('JWT_SECRET'))
    
        return jsonify({"token": token}), 201
    except Exception as err:
        raise 
        return jsonify({"err": str(err)}), 401
    


@app.route('/auth/sign-in', methods=["POST"])
def sign_in():
    try:
        sign_in_form_data = request.get_json()
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s;", (sign_in_form_data["username"],))
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
        raise
        return jsonify({"err": err}), 500
    finally:
        connection.close()

    
@app.route('/verify-token', methods=['POST'])
def verify_token():
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        decoded_token = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=["HS256"])
        return jsonify({"user": decoded_token})
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
# @app.route('/users/<user_id>')
# @token_required
# def users_user_index(user_id):
#     if user_id != g.user["id"]:
#         return jsonify({"err": "Unauthorized"}), 403
#     connection = get_db_connection()
#     cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#     cursor.execute("SELECT id, username FROM users WHERE id = %s;", (user_id))
#     user = cursor.fetchone()
#     connection.close()
#     if user is None:
#         return jsonify({"err": "User not found"}), 404
#     return jsonify(user), 200

    


# CRUD Routes
@app.route("/")
def index():
    return render_template('base.html', name='index')

def get_user():
  token = request.headers.get('Authorization').split(' ')[1]
  decoded_token = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=["HS256"])
  user = decoded_token.get('payload',{}).get('id', 0)
  if not user:
      abort(401)
  return user

@app.route('/createtables')
def create_tables():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute('CREATE TABLE if not exists concerts (id serial Primary key, headliner text not null, openers text, date Date not null, location text not null, notes text, concert_goer integer not null)')
        cursor.execute('CREATE TABLE if not exists users (id serial Primary Key, user text not null, password text not null)')
        connection.commit()
        # concerts = cursor.fetchall()
        connection.close()
    except:
        raise
        return "Application Error", 500

@app.route('/concerts', methods= ['GET'])
def list_concerts():
  user = get_user()
  try:
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM concerts WHERE concert_goer = %s;", (user,))
    concerts = cursor.fetchall()
    connection.close()
    return concerts
  except:
     return "Application Error", 500
  

@app.route('/concerts', methods=['POST'])
def create_concert():
  user = get_user()
  try:
    new_concert = request.json
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("INSERT INTO concerts (headliner, openers, date, location, concert_goer) VALUES (%s, %s, %s, %s, %s) RETURNING *", 
                   (new_concert['headliner'], new_concert['openers'], new_concert['date'], new_concert['location'], user))
    created_concert = cursor.fetchone()
    connection.commit()
    connection.close()
    return created_concert, 201
  except Exception as e:
     return str(e), 500
  
@app.route('/concerts/<concert_id>', methods=['GET'])
def show_concert(concert_id):
    user = get_user()
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM concerts WHERE id = %s AND concert_goer = %s", (concert_id, user))
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
    user = get_user()
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("DELETE FROM concerts WHERE id = %s AND concert_goer = %s", (concert_id, user))
        if cursor.rowcount == 0:
            return "Concert not found", 404
        connection.commit()
        cursor.close()
        return "Concert deleted successfully", 204
    except Exception as e:
        return str(e), 500


@app.route('/concerts/<concert_id>', methods=['PUT'])
def update_concert(concert_id):
    user = get_user()
    try:
      connection = get_db_connection()
      cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
      cursor.execute("UPDATE concerts SET headliner = %s, openers = %s, date = %s, location = %s WHERE id = %s AND concert_goer = %s RETURNING *", (request.json['headliner'], request.json['openers'], request.json['date'], request.json['location'], concert_id, user))
      updated_concert = cursor.fetchone()
      if updated_concert is None:
        return "Concert Not Found", 404
      connection.commit()
      connection.close()
      return updated_concert, 202
    except Exception as e:
      return str(e), 500


app.run(debug=True, host='0.0.0.0', port=os.getenv('PORT', 5000))