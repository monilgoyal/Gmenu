#!/usr/bin/env python
from flask import Flask, request, render_template, jsonify
import os
import dockerOperations
app = Flask("myapp")


@ app.route("/", methods=['GET'])
def ajax():
    technology = os.listdir("./templates/tech")
    technology = [t.replace('.html', '') for t in technology]
    return render_template('index.html', coll=technology)


@ app.route("/docker/<resource>/<action>", methods=['POST'])
def action(resource, action):
    if request.is_json:
        data = request.get_json()
        if resource == "container":
            return jsonify(getattr(dockerOperations.container(data), action)())
        elif resource == "image":
            return jsonify(getattr(dockerOperations.image(data), action)())
        else:
            return jsonify(1, {})
    return jsonify(1, {})


@ app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
