import os
from flask import Flask, render_template, request, abort
from db_layer import MongoCloud, MongoDB
# from flask_pymongo import PyMongo

db = MongoDB("kiwi_db")


config = {
    "DEBUG": True,
    "CACHE_TYPE": "null",
    "CACHE_DEFAULT_TIMEOUT": 1
}

def get_tables():
    return_list = ["parts", "installs", "airplanes"]
    return return_list

app = Flask(__name__)
app.config.from_mapping(config)

@app.route('/')
def home_page():
    options = ["Part", "Assembly", "Installation"]
    return render_template("main_page.jinja2", options=options)

@app.route('/all')
def full_table():
    available_tables = get_tables()
    request_type = request.args["type"]
    if request_type in available_tables:
        titles, data = db.collection_search(request_type, {})
        return render_template("main_page_js.jinja2", titles=titles, data=data)
    else:
        abort(404)

@app.route('/nested')
def nested_page():
    #titles, data = db.collection_search("parts", {})
    return render_template("nested.jinja2")

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
