from app import app, jsonify, request
from app import api, Resource
import re

users = [
    { "id": 1, "username": "John", "email":"John@gmail.com", "reg_data":"19-11-2023"},
    { "id": 2, "name": "Jane", "email":"Jane@mail.ru", "reg_data":"19-05-2023"},
    { "id": 3, "name": "Alice", "email":"Alice@yandex.ru", "reg_data":"19-04-2024"}
]


@api.resource("/users", "/users/")
class Users(Resource):
    def get(self):
        return jsonify(users)
    
    def post(self):
        new_user = request.get_json()
        if not new_user:
            return {'message': "No input data provided"}, 400
        # try:
        if not re.match(r'[^@]+@[^@]+\.[^@]+', new_user.get("email", "")):
            return {"message": "Invalid email"}, 400
        # except  as err:
        #     return err.messages, 422
        user = next((user for user in users if user['id'] == id), None)
        if user:
            return {'message': "User exists"}, 409
        
        users.append(new_user)
        return new_user, 201

@api.resource("/users/<int:id>")
class oneUser(Resource):
    def get(self, id):
        if id is None:
            return jsonify(users)
        else:
            user = next((user for user in users if user['id'] == id), None)
            if user: return jsonify(user)
        return {"error": "User not found"}, 404

    def put(self, id):
        user = next((user for user in users if user['id'] == id), None)
        if not user:
            return {"error": "User not found"}, 404
        new_user = request.get_json()
        # try:
        if new_user.get("email", None):
            if not re.match(r'[^@]+@[^@]+\.[^@]+', new_user.get("email", "")):
                return {"message": "Invalid email"}, 400
            else: user["email"] = new_user["email"]

        if user.get("username", None):
            user["username"] = new_user["username"]
        if user.get("reg_date", None):
            user["reg_date"] = new_user["reg_date"]
        # except  as err:
        #     return err.messages, 422
        return user, 200
    
    def delete(self, id):
        user = next((user for user in users if user['id'] == id), None)
        if user:
            users.remove(user)
            return {"message": "User deleted"}, 200
        return {"error": "User not found"}, 404
    
	# def get(self):
	# 	return users_schema.dump(User.find_all()), 200

	# def put(self, id):
	# 	user_json = request.get_json()
	# 	if not user_json:
	# 		return {'message': "No input data provided"}, 400
	# 	try:
	# 		user_data = user_schema.load(user_json)
	# 		if not re.match(r'[^@]+@[^@]+\.[^@]+', user_data.email):
	# 			return 'Invalid email', 400
	# 	except ValidationError as err:
	# 		return err.messages, 422
	# 	user = User.find_by_id(id)
	# 	if not user:
	# 		return {'message': USER_NOT_FOUND}, 404
	# 	user.email = user_data.email
	# 	user.fullname = user_data.fullname
	# 	user.phoneNumber = user_data.phoneNumber
	# 	user.password = bcrypt.hashpw(user_data.password.encode('utf-8'),bcrypt.gensalt())
	# 	user.save_to_db()
	# 	return user_schema.dump(user), 200

	# def delete(self, id):
	# 	users_to_delete = User.find_by_id(id)
	# 	users_to_delete.delete_from_db()
	# 	return jsonify({"message": "User Deleted Successfully"}), 204
