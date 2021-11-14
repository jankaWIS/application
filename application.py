#
import json
import os

from flask import Flask, request, render_template
from markupsafe import escape

app = Flask(__name__)

# define path
path = "../wis-advanced-python-2021-2022/students/"


@app.route("/")
def main():
    return render_template("main.html", title="People")


# list all people
@app.route("/all")
def all():
    return list_people(path)


# # show personal details, no template
# @app.route("/person/<filename>")
# def person(filename):
#     person_details = f"""
#     <h1>Personal details</h1>
#
#     <h2>Personal json</h2>
#     <p>{escape(filename)}</p>
#
#     <h2>Details</h2>
#     <div>
#         <ul>
#     """
#
#     # check if the file exists
#     if filename not in os.listdir(path):
#         return 'This person does not exist', 400
#     else:
#         # load the json
#         with open(os.path.join(path, filename)) as fh:
#             data = json.load(fh)
#         # if "name" in data.keys():
#         #     print(data["name"])
#         # else:
#         #     print("This filename does not have name", filename)
#         for item in data.keys():
#             person_details += f"<li>{item}: {data[item]}</li>"
#
#     person_details += "</ul></div>"
#
#     return person_details


# show personal details
@app.route("/person/<filename>")
def person(filename):
    person_details = "<div><ul>"

    # check if the file exists
    if filename not in os.listdir(path):
        return 'This person does not exist', 400
    else:
        # load the json
        with open(os.path.join(path, filename)) as fh:
            data = json.load(fh)
        # go over keys and print the info out
        for item in data.keys():
            person_details += f"<li>{item}: {data[item]}</li>"

    person_details += "</ul></div>"

    return render_template('show_details.html', full_list=person_details, json_name=escape(filename))


# show the raw json file
@app.route("/person/<filename>/raw")
def raw_json(filename):
    return show_raw_code(os.path.join(path, filename + ".json"))


# without a helper function
# @app.route("/list_students.py")
# def show_list_students():
#     f = open('list_students.py', 'r')
#     return render_template('python_script.html', n=f.read())
@app.route("/list_students.py")
def show_list_students():
    return show_raw_code('list_students.py')

@app.route("/list_students_search_engine.py")
def show_list_students():
    return show_raw_code('list_students_search_engine.py')


##
@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"


## helper funtions
def show_raw_code(file):
    f = open(file, 'r')
    return render_template('show_raw.html', n=f.read())


def fetch_name_link(path2json):
    """
    Fetch the json file and return name and link values if exist
    :param path2json:
    :return:
    """
    name = None
    link = ""
    with open(path2json) as fh:
        data = json.load(fh)

    if "name" in data.keys():
        name = data["name"]

    if "link" in data.keys():
        link = data["link"]

    return name, link


def list_people(path_students):
    """
    go over all json files in a given path, list the filenames, fetch their name and link from the corresponding json
    and render it
    :return: string of an HTML list of students with links
    """
    # list all json files
    students = sorted([x for x in os.listdir(path_students) if x.endswith(".json")])
    # initialise list
    students_page = """
    <nav>
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/all">All</a> the people</li>
        </ul>
    </nav>
    
    <h1>List of all students</h1>  
    <div>
    <ul>
    """
    for student in students:
        # get the details
        name, link = fetch_name_link(os.path.join(path_students, student))
        # create automatic redirection to github if link does not exit
        if not link:
            link = 'https://github.com/'+student.split(".")[0]
            
        # check if name is present
        if not name:
            students_page += f'<li>This filename/student does not have a name: {student}</li>'
        else:
            students_page += f'<li><a href="{link}">{name}</a>, json details: <a href="person/{student}">all information</a>, <a href="person/{student.split(".")[0]}/raw">raw</a></li>'

    # close tags
    students_page += "</ul></div>"

    return students_page
