from spacy.training.example import Example
from pathlib import Path
from spacy.util import minibatch, compounding
import random
import spacy
nlp = spacy.load("en_core_web_sm")

train = [
    ("create new monil namespace", {"entities": [
     (0, 6, "ACTIVITY"), (17, 26, "PRODUCT")]}),
    ("delete namespace", {"entities": [
     (0, 6, "ACTIVITY"), (7, 16, "PRODUCT")]}),
    ("please remove last namespace", {"entities": [
     (7, 13, "ACTIVITY"), (19, 28, "PRODUCT")]}),
    ("remove ns i.e. monil", {"entities": [
     (0, 6, "ACTIVITY"), (7, 9, "PRODUCT")]}),
    ("create hhg ns", {"entities": [(0, 6, "ACTIVITY"), (11, 13, "PRODUCT")]}),
    ("show all namespace", {"entities": [
     (0, 4, "ACTIVITY"), (9, 18, "PRODUCT")]}),
    ("show all namespaces", {"entities": [
     (0, 4, "ACTIVITY"), (9, 19, "PRODUCT")]}),
    ("show all ns", {"entities": [(0, 4, "ACTIVITY"), (9, 11, "PRODUCT")]}),
    ("describe development namespace", {
     "entities": [(0, 8, "ACTIVITY"), (21, 30, "PRODUCT")]}),
    ("describe kube ns", {"entities": [
     (0, 8, "ACTIVITY"), (14, 16, "PRODUCT")]}),
    ("can you launch deployment with httpd image in monil namespace",
     {"entities": [(8, 14, "ACTIVITY"), (15, 25, "PRODUCT")]}),
    ("launch deploy in harry namespace", {
     "entities": [(0, 6, "ACTIVITY"), (7, 13, "PRODUCT")]}),
    ("run deploy in harry namespace", {
     "entities": [(0, 3, "ACTIVITY"), (4, 10, "PRODUCT")]}),
    ("create monild deployment", {"entities": [
     (0, 6, "ACTIVITY"), (14, 24, "PRODUCT")]}),
    ("delete gg deployment", {"entities": [
     (0, 6, "ACTIVITY"), (10, 20, "PRODUCT")]}),
    ("please remove ggdfd deploy", {"entities": [
     (7, 13, "ACTIVITY"), (20, 26, "PRODUCT")]}),
    ("show all deployments", {"entities": [
     (0, 4, "ACTIVITY"), (9, 20, "PRODUCT")]}),
    ("describe mccggg deployment", {"entities": [
     (0, 8, "ACTIVITY"), (16, 26, "PRODUCT")]}),
    ("list all the deploys in fff namespace", {
     "entities": [(0, 4, "ACTIVITY"), (13, 20, "PRODUCT")]}),
    ("get the deployments", {"entities": [
     (0, 3, "ACTIVITY"), (8, 19, "PRODUCT")]}),
    ("hey! can you delete myd deploy", {
     "entities": [(13, 19, "ACTIVITY"), (24, 30, "PRODUCT")]}),
    ("please run newdep deployment in ff ns", {
     "entities": [(7, 10, "ACTIVITY"), (18, 28, "PRODUCT")]}),
    ("can you launch pod with httpd image in monil namespace",
     {"entities": [(8, 14, "ACTIVITY"), (15, 18, "PRODUCT")]}),
    ("launch pod in harry namespace", {
     "entities": [(0, 6, "ACTIVITY"), (7, 10, "PRODUCT")]}),
    ("run pod in harry namespace", {
     "entities": [(0, 3, "ACTIVITY"), (4, 7, "PRODUCT")]}),
    ("create monild pod", {"entities": [
     (0, 6, "ACTIVITY"), (14, 17, "PRODUCT")]}),
    ("delete gg pod", {"entities": [(0, 6, "ACTIVITY"), (10, 13, "PRODUCT")]}),
    ("please remove ggdfd pod", {"entities": [
     (7, 13, "ACTIVITY"), (20, 23, "PRODUCT")]}),
    ("show all pods", {"entities": [(0, 4, "ACTIVITY"), (9, 13, "PRODUCT")]}),
    ("describe mccggg pod", {"entities": [
     (0, 8, "ACTIVITY"), (16, 19, "PRODUCT")]}),
    ("list all the pods in fff namespace", {
     "entities": [(0, 4, "ACTIVITY"), (13, 17, "PRODUCT")]}),
    ("get all the pods", {"entities": [
     (0, 3, "ACTIVITY"), (12, 16, "PRODUCT")]}),
    ("hey! can you delete myd pod", {"entities": [
     (13, 19, "ACTIVITY"), (24, 27, "PRODUCT")]}),
    ("please run newdep pod in ff ns", {
     "entities": [(7, 10, "ACTIVITY"), (18, 21, "PRODUCT")]}),
    ("remove all the pods", {"entities": [
     (0, 6, "ACTIVITY"), (15, 19, "PRODUCT")]}),
    ("please delete all pods", {"entities": [
     (7, 13, "ACTIVITY"), (18, 22, "PRODUCT")]}),
    ("remove all the deployments", {"entities": [
     (0, 6, "ACTIVITY"), (15, 26, "PRODUCT")]}),
    ("please delete all deployments", {
     "entities": [(7, 13, "ACTIVITY"), (18, 29, "PRODUCT")]}),
]

ner = nlp.get_pipe("ner")

for _, annotations in train:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

disable_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

with nlp.disable_pipes(*disable_pipes):
    optimizer = nlp.resume_training()
    for iteration in range(100):
        random.shuffle(train)
        losses = {}
        batches = minibatch(train, size=compounding(1.0, 4.0, 1.001))
        for batch in batches:
            for text, annotations in batch:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                nlp.update(
                    [example],
                    drop=0.5,
                    losses=losses,
                    sgd=optimizer
                )
        print("losses", losses)

ruler = nlp.get_pipe("attribute_ruler")
ruler.add(patterns=[[{"ORTH": "using"}]], attrs={"POS": "ADP"})
ruler.add(patterns=[[{"ORTH": "deploy"}]],
          attrs={"POS": "NOUN", "DEP": "dobj"})
