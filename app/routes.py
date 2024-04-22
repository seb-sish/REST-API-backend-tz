from app import request, api, Resource
from app import db

from app.models import User
from datetime import datetime
import re

@api.resource("/users", "/users/")
class Users(Resource):
    def get(self):
        return [i.serialize for i in User.query.all()]
    
    def post(self):
        new_user = request.get_json()
        if not new_user:
            return {'error': "No input data provided"}, 400
        if not re.match(r'[^@]+@[^@]+\.[^@]+', new_user.get("email", "")):
            return {"error": "Invalid email"}, 400
        if not new_user.get("username", None):
            return {"error": "Invalid username"}, 400
        if len(User.query.filter((User.username == new_user.get("username", None)) | (User.email == new_user.get("email", None))).all())!=0:
            return {"error": "username or email already taken"}, 409
        if new_user.get("id", None):
            if not User.query.get(new_user["id"]):
                u = User(id=new_user["id"], username=new_user["username"], email=new_user["email"])
            else: return {"error": "ID already exists"}, 409
        else: u = User(username=new_user["username"], email=new_user["email"])
        db.session.add(u)
        db.session.commit()
        return u.serialize, 201

@api.resource("/users/<int:id>")
class oneUser(Resource):
    def get(self, id):
        user = User.query.get(id)
        if user: return user.serialize, 200
        return {"error": "User not found"}, 404

    def put(self, id):
        user = User.query.get(id)
        if not user: return {"error": "User not found"}, 404
        new_user = request.get_json()
        
        if len(User.query.filter((User.username == new_user.get("username", None)) | (User.email == new_user.get("email", None))).all())!=0:
            return {'error': "username or email already taken"}, 409
        
        if new_user.get("email", None):
            if not re.match(r'[^@]+@[^@]+\.[^@]+', new_user.get("email", "")):
                return {"error": "Invalid email"}, 400
            else: user.email = new_user["email"]
        if new_user.get("username", None):
            user.username = new_user["username"]
        if new_user.get("id", None):
            if not User.query.get(new_user["id"]):
                user.id = new_user["id"]
            else: return {"error": "ID already exists"}, 409
        if new_user.get("reg_date", None):
            try: user.reg_date = datetime.strptime(" ".join(new_user["reg_date"]), "%d-%m-%Y %H:%M:%S")
            except ValueError: return {"error": f"time data {new_user["reg_date"]} does not match format '%d-%m-%Y %H:%M:%S'"}, 400
        db.session.commit()
        return user.serialize, 200
    
    def delete(self, id):
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return user.serialize, 200
        return {"error": "User not found"}, 404
@api.resource("/users/<id>")
class oneUserStr(Resource):
    def get(self, id):
        return {"error": "Invalid ID supplied"}, 400
    def put(self, id):
        return {"error": "Invalid ID supplied"}, 400
    def delete(self, id):
        return {"error": "Invalid ID supplied"}, 400