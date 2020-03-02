import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("A STAR IS BORN")
for token in doc:
    print(token.text, token.pos_, token.dep_)
