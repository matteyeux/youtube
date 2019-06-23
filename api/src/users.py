from app import app

# endpoint to show all users
@app.route("/users", methods=["GET"])
def users():
	all_users = User.query.all()
	result = users_schema.dump(all_users)
	return jsonify(result.data)