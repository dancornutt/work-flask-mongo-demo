import os
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)


@app.route('/')
def home_page():
    online_users = mongo.db.users.find({'online': True})
    # return render_template('index.html', online_users=online_users)
    return "This app is up!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
