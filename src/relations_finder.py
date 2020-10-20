import en_core_web_sm
from spacy import displacy


class Relations_finder:
    def __init__(self):
        self.nlp = en_core_web_sm.load()

    def find_relations(self, sentence):
        result = {'subject': '', 'objects': [], 'relation': ''}
        doc = self.nlp(sentence)
        self.generate_html(doc)
        for token in doc:
            if token.dep_ == 'nsubj':
                result['subject'] = token.text
            elif token.dep_ == 'dobj':
                result['objects'].append(token.text)
            elif token.dep_ == 'ROOT' and token.pos_ == 'VERB':
                result['relation'] = token.lemma_
        return result

    def generate_html(self, nlp_doc):
        html = displacy.render([nlp_doc], style="dep", page=True)
        with open('spacy.html', 'w') as out_file:
            out_file.write(html)
