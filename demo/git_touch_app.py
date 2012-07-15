from flask import Flask, jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

from git import Repo, GitCmdObjectDB

def make_json_app(import_name, **kwargs):
    """
    Creates a JSON-oriented Flask app.

    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    """
    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    app = Flask(import_name, **kwargs)

    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    return app

app = make_json_app(__name__)
repo = Repo("sample-repo", odbt=GitCmdObjectDB)

@app.route("/diff")
def diff():
    return jsonify(response="hello")

@app.route("/log")
def log():
    """ Get all logs and return them in json format """
    data = {}
    for head in repo.heads:
        log_entries = []
        for log_entry in head.log():
            log_entries.append({
                'message': log_entry.message,
                'commit': log_entry.newhexsha,
                'parent': log_entry.oldhexsha,
                'author': str(log_entry.actor),
                'committer': str(log_entry.actor), #fix this 
                'time': log_entry.time
            })
        data[head.name] = log_entries
    return jsonify(data)

def _commit_tree(commit):
    """ genereate a commit tree starting from a commit """
    return {
            "commit": commit.hexsha,
            "parents": [_commit_tree(c) for c in commit.parents],
            "tree": commit.tree.hexsha,
            "author": str(commit.author),
            "authored_date": commit.authored_date,
            "committer": str(commit.committer),
            "committed_date": commit.committed_date,
            "message": commit.message
    }

@app.route("/commits")
def commits(branch="master", start=0, offset=100):
    """Get all starting from the head"""
    commit = repo.commit(branch)
    commit_tree = _commit_tree(commit)
    return jsonify(commit_tree)

@app.route("/")
def index():
    return open("index.html").read()

if __name__ == "__main__":
    app.run(debug=True)
