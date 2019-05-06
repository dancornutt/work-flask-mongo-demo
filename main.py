import os
from flask import Flask, render_template, request
from db_layer import MongoCloud, MongoDB
# from flask_pymongo import PyMongo

db = MongoDB("kiwi_db")


config = {
    "DEBUG": True,
    "CACHE_TYPE": "null",
    "CACHE_DEFAULT_TIMEOUT": 1
}

app = Flask(__name__)
app.config.from_mapping(config)
#mongo = PyMongo(app)

@app.route('/')
def home_page():
    options = ["Part", "Assembly", "Installation"]
    return render_template("main_page.jinja2", options=options)

@app.route('/main')
def home_page_js():
    titles, data = db.collection_search("parts", {})
    # titles = "Titles to use for the thing".split(" ")
    # data = [[1, 2, 3, 4, 5, 6], [2, 3, 4, 5, 6, 7]]
    return render_template("main_page_js.jinja2", titles=titles, data=data)

@app.route('/part')
def part_page():
    print(request.args)
    part_id = request.args["part_number"]
    return render_template("part.jinja2",part=part_id)

@app.route('/part/<int:part_id>')
def part_page_specific(part_id):
    return render_template("part.jinja2", part=part_id)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7779))
    app.run(host='0.0.0.0', port=port)
