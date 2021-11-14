import json
import os

from flask import Flask, request, render_template
from markupsafe import escape

app = Flask(__name__)

# define path
path = "../wis-advanced-python-2021-2022/students/"


@app.route("/")
def main():
    return '''
    <h1>Search engine</h1>
    <div>
     <form action="/process" method="GET">
         <label for="phrase">Enter a search phrase:<br></label>
         <input id="phrase" name="phrase" placeholder="phrase">
         <input type="submit" value="Submit">
     </form>
     </div>
     '''


# list all people
@app.route("/all")
def all():
    return list_people(path)


# the search -- search through jsons, output only the names of the people where it was found, then sort and make a list out of it
@app.route("/process")
def search_phrase():
    phrase = request.args.get('phrase', '')
    result = f"""
    <nav>
        <ul>
            <li><a href="/">Home</a></li>
        </ul>
    </nav>
    <h1>Search results</h1>
    You have searched: {escape(phrase)} <br>
    """

    if phrase:
        _, sorted_names = find_phrase_students_name(path, escape(phrase))

    # result += f"<br>dict: <br> {sorted_names}<br>"
    result += """
        <h2>List of all students matching the phrase in any of the fields</h2>  
    <div>
    <ul>
    """
    if sorted_names:
        for name in sorted_names.keys():
            # create automatic redirection to github
            link = 'https://github.com/' + sorted_names[name]

            # check if name is present
            if "noname" in name:
                result += f'<li>This filename/student does not have a name: {name}</li>'
            else:
                result += f'<li><a href="{link}">{name}</a>, json details: <a href="person/{sorted_names[name]}">all information</a>, <a href="person/{sorted_names[name].split(".")[0]}/raw">raw</a></li>'
    else:
        result += "<p>No file matches the given phrase. </p>"
    # close tags
    result += "</ul></div>"+footer

    return result


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
        # create automatic redirection to github
        if not link:
            link = 'https://github.com/' + student.split(".")[0]

        # check if name is present
        if not name:
            students_page += f'<li>This filename/student does not have a name: {student}</li>'
        else:
            students_page += f'<li><a href="{link}">{name}</a>, json details: <a href="person/{student}">all information</a>, <a href="person/{student.split(".")[0]}/raw">raw</a></li>'

    # close tags
    students_page += "</ul></div>"

    return students_page


def find_phrase_students_name(path, phrase):
    """
    At the moment, returns both sorted name and github details (github name) as a dict and a dict of all the findings,
    ie. the exact fields and items where the searched phrase was found
    :param path: to the json files
    :param phrase: what to search for
    :return:
    """
    # create dict for all information
    findings = {}
    # create dict for names
    names = {}
    for i, filename in enumerate(os.listdir(path)):
        # print(filename)
        with open(os.path.join(path, filename)) as fh:
            data = json.load(fh)

        used_keys = []
        for key in data.keys():
            # check keys
            if phrase in key:
                used_keys.append(key)
                print("Found in key: ", key, data[key])
            # check values, avoid the None
            if data[key]:
                if phrase in data[key]:
                    used_keys.append(key)
                    findings[filename] = {"values": data[key]}
                    print("Found in value: ", key, data[key])

        # if there are any results, update the findings
        if used_keys:
            findings[filename] = {"keys": set(used_keys)}
            # save name and github link, prevent a blowup
            if data["name"]:
                names[data["name"]] = filename
            else:
                names["noname" + str(i)] = filename

        # sort the names based on alphabet
        sorted_names = dict(sorted(names.items()))

    return findings, sorted_names


footer = """
<footer style="position:fixed; bottom:0">
Powered by the best search engine (Jangine), designed by @JK. 
</footer>
"""