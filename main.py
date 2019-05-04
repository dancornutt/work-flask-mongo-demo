import os
from flask import Flask, render_template
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://kiwi-admin:Test777Boeing@kiwi-jwnc9.azure.mongodb.net/test?retryWrites=true"
mongo = PyMongo(app)


@app.route('/')
def home_page():
    # online_users = mongo.db.users.find({'online': True})
    # return render_template('index.html', online_users=online_users)
    options = ["Part", "Assembly", "Installation"]
    return render_template("main_page.jinja2", options=options)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7779))
    app.run(host='0.0.0.0', port=port)
