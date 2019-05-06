import os
from flask import Flask, render_template, request
from flask_pymongo import PyMongo

config = {
    "DEBUG": True,
    "CACHE_TYPE": "null",
    "CACHE_DEFAULT_TIMEOUT": 1,
    "MONGO_URI": "mongodb+srv://kiwi-admin:Test777Boeing@kiwi-jwnc9.azure.mongodb.net/test?retryWrites=true"
}

app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb+srv://kiwi-admin:Test777Boeing@kiwi-jwnc9.azure.mongodb.net/test?retryWrites=true"
app.config.from_mapping(config)
mongo = PyMongo(app)

@app.route('/')
def home_page():
    options = ["Part", "Assembly", "Installation"]
    return render_template("main_page.jinja2", options=options)

@app.route('/part')
def part_page():
    print(request.args)
    part_id = request.args["part_number"]
    # online_users = mongo.db.users.find({'online': True})
    # return render_template('index.html', online_users=online_users)
    return render_template("part.jinja2",part=part_id)

@app.route('/part/<int:part_id>')
def part_page_specific(part_id):
    # online_users = mongo.db.users.find({'online': True})
    # return render_template('index.html', online_users=online_users)
    return render_template("part.jinja2", part=part_id)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7779))
    app.run(host='0.0.0.0', port=port)
