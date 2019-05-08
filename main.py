import os
from flask import Flask, render_template, request, abort
#from db_layer import MongoCloud, MongoDB
from azure_db import collection_search, part_lower_search, airplane_lower_search

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
    tuple_test = [["ford,ford Company", ["part 1,part 1 info", "part 2,part 2 info", "part 3,part 3 info"]],
                  ["chev,company", ["part 1,part 1 info","part 4,part 4 info"]],
                  ["Prosche,company", ["part 4,part 4 info","part 5,part 5 info","part 6,part 6 info"]]]
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

@app.route('/search')
def search_page():
    # if request.args["search_type"] == "parts":
    #     if request.args["level"] == "next_lower":
    #         titles, data, extra_titles, extra_data = part_lower_search(request.args["part_number"])
    #     elif request.args["level"] == "next_higher":
    #         titles, data, extra_titles, extra_data = part_higher_search(request.args["part_number"])
    # if request.args["search_type"] == "installs":
    #     if request.args["level"] == "next_lower":
    #         titles, data, extra_titles, extra_data = installs_lower_search(request.args["part_number"])
    #     elif request.args["level"] == "next_higher":
    #         titles, data, extra_titles, extra_data = installs_higher_search(request.args["part_number"])
    if request.args["search_type"] == "airplanes":
        if request.args["level"] == "next_lower":
            titles, data = airplane_lower_search(request.args["part_number"])
            extra_titles = None
            extra_data = None
            criteria = "Search Results for Airplane Lower, Line Number:" + request.args["part_number"]
        elif request.args["level"] == "next_higher":
            abort(404)
    return render_template("search.jinja2", criteria=criteria, titles=titles, data=data, extra_titles=extra_titles, extra_data=extra_data)

@app.route('/part/<int:part_id>')
def part_page_specific(part_id):
    return render_template("part.jinja2", part=part_id)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7779))
    app.run(host='0.0.0.0', port=port)
