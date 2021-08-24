#!/usr/bin/env python
import nlpparser
from k8soperations import ns, pod, deploy

from flask import Flask, request, render_template, jsonify
import os
import dockerOperations
from dotenv import load_dotenv
load_dotenv('cred.env')
app = Flask("myapp")

deployment = deployments = deploy
namespace = namespaces = ns
pods = pod


@ app.route("/", methods=['GET'])
def ajax():
    technology = os.listdir("./templates/tech")
    technology = [t.replace('.html', '') for t in technology]
    return render_template('index.html', coll=technology)


@ app.route("/docker/<resource>/<action>", methods=['POST'])
def docker(resource, action):
    if request.is_json:
        data = request.get_json()
        if resource == "container":
            return jsonify(getattr(dockerOperations.container(data), action)())
        elif resource == "image":
            return jsonify(getattr(dockerOperations.image(data), action)())
        else:
            return jsonify(1, {})
    return jsonify(1, {})


@ app.route("/kubernetes/<resource>/<action>", methods=['POST'])
def k8s(resource, action):
    if request.is_json:
        data = request.get_json()
        try:
            return jsonify(getattr(eval(resource)(data), action)())
        except:
            return jsonify(1, "sorry! there is something wrong")
    return jsonify(1, "sorry! there is something wrong")


@ app.route("/kubernetes/nlp", methods=['POST'])
def nlp():
    if request.is_json:
        mess = request.get_json()
        return jsonify(nlpparser.nlp(mess))


@ app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
