import os
from flask import Flask, render_template, request, abort
#from db_layer import MongoCloud, MongoDB
from azure_db import collection_search
# from flask_pymongo import PyMongo

#db = MongoDB("kiwi_db")


config = {
    "DEBUG": True,
    "CACHE_TYPE": "null",
    "CACHE_DEFAULT_TIMEOUT": 1
}

def get_tables():
    return_list = ["parts", "installs", "airplanes"]
    return return_list

def nested_data():
    tuple_test = (("ford", "company", "part 1", "part 1 info"),
                  ("ford", "company", "part 2", "part 2 info"),
                  ("ford", "company", "part 3", "part 3 info"),
                  ("chev", "company", "part 1", "part 1 info"),
                  ("chev", "company", "part 4", "part 4 info"),
                  ("Prosche", "company", "part 4", "part 4 info"),
                  ("ford", "company", "part 5", "part 5 info"),
                  ("ford", "company", "part 6", "part 6 info"),
                  ("Prosche", "company", "part 1", "part 1 info"))
    return tuple_test

app = Flask(__name__)
app.config.from_mapping(config)

@app.route('/')
def home_page():
    tables = get_tables()
    return render_template("home_page.jinja2", tables=tables)

@app.route('/all')
def full_table():
    available_tables = get_tables()
    request_type = request.args["type"]
    if request_type in available_tables:
        titles, data = collection_search(request_type)
        return render_template("main_page_js.jinja2", titles=titles, data=data)
    else:
        abort(404)

@app.route('/nested')
def nested_page():
    data = nested_data()
    return render_template("nested.jinja2", data=data)

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
