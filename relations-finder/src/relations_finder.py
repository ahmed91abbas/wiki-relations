import en_core_web_sm
from spacy import displacy


class Relations_finder:
    def __init__(self):
        self.subject = ''
        self.nlp = en_core_web_sm.load()

    def generate_html(self, nlp_doc):
        html = displacy.render([nlp_doc], style="dep", page=True)
        with open('spacy.html', 'w') as out_file:
            out_file.write(html)

    def find_relations(self, data):
        self.subject = data['name']
        result = {'subject': data['name'], 'url': data['url'], 'relations': []}
        for content in data['content_chunks']:
            doc = self.nlp(content)
            for sentence in list(doc.sents):
                relations = self.process_sentence(sentence.text)
                result['relations'].append(relations)
        result['relations'] = list(filter(None, result['relations']))
        return result

    def process_sentence(self, sentence):
        doc = self.nlp(sentence)
        self.generate_html(doc)
        result = {}
        for token in doc:
            if token.pos_ == 'VERB':
                result = self.process_from_verb(token)
                result['sentence'] = sentence
        if not all(list(result.values())):
            result = None
        return result

    def process_from_verb(self, token):
        relation = token.lemma_
        r_head = token
        for r_token in token.rights:
            if r_token.dep_ == 'agent' and r_token.pos_ == 'ADP':
                r_head = r_token
                relation = f'{relation} {r_token.lemma_}'
        subject = self.get_subject_connected_to_token(token)
        objects = self.get_objects_connected_to_token(r_head)
        return {'subject': subject, 'objects': objects, 'relation': relation}

    def get_subject_connected_to_token(self, token):
        for parent in token.lefts:
            if parent.dep_ in ['nsubj', 'nsubjpass'] and parent.pos_ in ['PRON', 'NOUN', 'PROPN']:
                return self.get_proper_subject(parent)
        return None

    def get_objects_connected_to_token(self, token):
        objects = []
        for child in token.rights:
            if child.dep_ in ['dobj', 'pobj']:
                objects.append(self.get_proper_noun(child))
                objects += self.get_conjunctions(child)
        return list(filter(None, objects))

    def get_proper_noun(self, token):
        if token.pos_ not in ['PROPN', 'NOUN']:
            return None
        if token.pos_ == 'PROPN':
            return self.get_compound_form(token)
        for child in token.rights:
            if child.pos_ == 'PROPN':
                return self.get_compound_form(child)
        return None

    def get_compound_form(self, token):
        compound_form = token.text
        for child in token.lefts:
            if child.dep_ == 'compound' and token.pos_ == child.pos_:
                compound_form = f'{child.text} {compound_form}'
        for child in token.rights:
            if child.dep_ == 'compound' and token.pos_ == child.pos_:
                compound_form = f'{compound_form} {child.text}'
        if compound_form.lower() in self.subject.lower().split(' '):
            return self.subject
        return compound_form

    def get_proper_subject(self, token):
        if token.pos_ == 'PRON':
            return self.subject
        name = self.get_compound_form(token)
        return name

    def get_conjunctions(self, token):
        result = []
        queue = set(token.rights)
        while queue:
            child = queue.pop()
            queue.update(child.rights)
            if child.dep_ == 'conj':
                result.append(self.get_proper_noun(child))
        return result
