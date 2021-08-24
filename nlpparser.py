
import inspect
import textacy
import json
from k8soperations import ns, pod, deploy
import spacy
newnlp = spacy.load("nr")


deployment = deployments = deploy
namespace = namespaces = ns
pods = pod


def checkclass(arg):
    try:
        inspect.isclass(eval(str(arg)))
        return True
    except:
        return False


def nlp(mess_from_client):
    doc = newnlp(mess_from_client)
    none = None
    resource = action = "none"
    for token in doc.ents:
        if token.label_ == "PRODUCT" and checkclass(token):
            resource = str(token)
    for token in doc.ents:
        if token.label_ == "ACTIVITY" and str(token) in [func for func in dir(eval(resource)) if not func.startswith("__") and callable(getattr(eval(resource), func))]:
            action = str(token.lemma_)
    try:
        pattern_for_all = [{"LOWER": "all"}, {
            "LOWER": "the", "OP": "?"}, {"ENT_TYPE": "PRODUCT"}]
        l_all = textacy.extract.token_matches(doc, pattern_for_all)
        for i in l_all:
            action = action+'_all'
            struct = json.loads(json.dumps(
                getattr(eval(resource), action).struct))
            for token in doc:
                if token.head.pos_ == "ADP":
                    listA = [child for child in token.children if not(
                        child.dep_ == "prep" or child.dep_ == "det")]
                    if len(listA) == 1 and str(token) in list(struct.keys()):
                        struct[str(token)]["value"] = str(listA[0])
            return 0, json.dumps(struct), resource, action

        struct = json.loads(json.dumps(getattr(eval(resource), action).struct))
        for token in doc:
            if token.head.pos_ == "ADP":
                listA = [child for child in token.children if not(
                    child.dep_ == "prep" or child.dep_ == "det")]
                if len(listA) == 1 and str(token) in list(struct.keys()):
                    struct[str(token)]["value"] = str(listA[0])
        name_pattern = [{"POS": "NOUN", "OP": "?"}, {"POS": "ADJ", "OP": "?"}, {
            "POS": "ADV", "OP": "?"}, {"ENT_TYPE": "PRODUCT"}]
        l = textacy.extract.token_matches(doc, name_pattern)
        for i in l:
            if len(str(i).split()) == 2 and str(i[1]) == resource and not str(i[0]) == action:
                struct["name"]["value"] = str(i[0])
        return 0, json.dumps(struct), resource, action
    except:
        return 1, "sorry! I am not able to understand"
