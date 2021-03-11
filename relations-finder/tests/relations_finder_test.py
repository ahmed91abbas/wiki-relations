import os
import sys
from unittest import TestCase
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath('..'))
from relations_finder import Relations_finder


class Test_relations_finder(TestCase):

    def setUp(self):
        self.finder = Relations_finder()

    @patch('relations_finder.displacy.render')
    def test_that_generate_html_renders_new_html_file(self, mock_render):
        nlp_doc = 'fake data'
        mock_render.return_value = 'fake html content'

        self.finder.generate_html(nlp_doc)

        mock_render.assert_called_once_with([nlp_doc], style='dep', page=True)

    @patch.object(Relations_finder, 'process_sentence')
    def test_that_find_relations_returns_correct_result(self, mock_process_sentence):
        subject = 'Foo'
        objects = ['Foo', 'Bar']
        url = 'foo.com'
        relation = {
            'subject': subject,
            'objects': objects,
            'relation': 'baz'
        }
        expected = {'subject': subject, 'url': url, 'relations': [relation]}
        mock_process_sentence.return_value = relation
        in_data = {'name': subject, 'url': url, 'content_chunks': ['test']}

        actual = self.finder.find_relations(in_data)

        self.assertDictEqual(expected, actual)

    @patch.object(Relations_finder, 'process_sentence')
    def test_that_find_relations_filters_none_values_from_relations(self, mock_process_sentence):
        subject = 'Foo'
        objects = ['Foo', 'Bar']
        url = 'foo.com'
        relation = {
            'subject': subject,
            'objects': objects,
            'relation': 'baz'
        }
        expected = {'subject': subject, 'url': url, 'relations': []}
        mock_process_sentence.return_value = None
        in_data = {'name': subject, 'url': url, 'content_chunks': ['test']}

        actual = self.finder.find_relations(in_data)

        self.assertDictEqual(expected, actual)

    @patch.object(Relations_finder, 'generate_html')
    @patch.object(Relations_finder, 'process_from_verb')
    def test_that_process_sentence_processes_sentences_with_single_verb(self, mock_process_from_verb, mock_generate_html):
        sentence = 'test'
        token = MagicMock()
        self.finder.nlp = MagicMock(return_value=[token])
        token.pos_ = 'VERB'
        processed_verb = {'foo': 'bar'}
        mock_process_from_verb.return_value = processed_verb
        expected = {'foo': 'bar', 'sentence': sentence}

        actual = self.finder.process_sentence(sentence)

        self.finder.nlp.assert_called_once_with(sentence)
        mock_process_from_verb.assert_called_once_with(token)
        self.assertDictEqual(expected, actual)

    @patch.object(Relations_finder, 'generate_html')
    @patch.object(Relations_finder, 'process_from_verb')
    def test_that_process_sentence_returns_none_if_any_value_is_none(self, mock_process_from_verb, mock_generate_html):
        sentence = 'test'
        token = MagicMock()
        self.finder.nlp = MagicMock(return_value=[token])
        token.pos_ = 'VERB'
        processed_verb = {'foo': None}
        mock_process_from_verb.return_value = processed_verb

        actual = self.finder.process_sentence(sentence)

        self.assertIsNone(actual)

    @patch.object(Relations_finder, 'get_subject_connected_to_token')
    @patch.object(Relations_finder, 'get_objects_connected_to_token')
    def test_that_process_from_verb_returns_correct_result(self, mock_get_objects, mock_get_subjects):
        relation = 'test'
        subject = 'foo'
        objects = ['foo', 'bar']
        token = MagicMock()
        token.rights = []
        token.lemma_ = relation
        mock_get_subjects.return_value = subject
        mock_get_objects.return_value = objects
        expected = {'subject': subject, 'objects': objects, 'relation': relation}

        actual = self.finder.process_from_verb(token)

        self.assertDictEqual(expected, actual)

    @patch.object(Relations_finder, 'get_subject_connected_to_token')
    @patch.object(Relations_finder, 'get_objects_connected_to_token')
    def test_that_process_from_verb_returns_adposition_relation(self, mock_get_objects, mock_get_subjects):
        lemma = 'influence'
        adposition_lemma = 'by'
        child = MagicMock()
        child.dep_ = 'agent'
        child.pos_ = 'ADP'
        child.lemma_ = adposition_lemma
        token = MagicMock()
        token.rights = [child]
        token.lemma_ = lemma
        expected = f'{lemma} {adposition_lemma}'

        actual = self.finder.process_from_verb(token)['relation']

        self.assertEqual(expected, actual)

    @patch.object(Relations_finder, 'get_proper_subject')
    def test_that_get_subject_connected_to_token_returns_subject(self, mock_get_proper_subject):
        child = MagicMock()
        token = MagicMock()
        token.lefts = [child]
        expected = 'Foo'
        mock_get_proper_subject.return_value = expected

        for deb in ['nsubj', 'nsubjpass']:
            for pos in ['PRON', 'NOUN', 'PROPN']:
                child.pos_ = pos
                child.dep_ = deb

                actual = self.finder.get_subject_connected_to_token(token)

                self.assertEqual(expected, actual)

    @patch.object(Relations_finder, 'get_proper_subject')
    def test_that_get_subject_connected_to_token_returns_none_if_token_not_subject(self, mock_get_proper_subject):
        child = MagicMock()
        token = MagicMock()
        token.lefts = [child]
        child.dep_ = 'not subject'

        actual = self.finder.get_subject_connected_to_token(token)

        self.assertIsNone(actual)

    @patch.object(Relations_finder, 'get_proper_noun')
    def test_that_get_objects_connected_to_token_list_of_objects(self, mock_get_proper_noun):
        child_obj = MagicMock()
        child_another_obj = MagicMock()
        child_not_obj = MagicMock()
        token = MagicMock()
        token.rights = [child_not_obj, child_obj, child_another_obj]
        child_not_obj.dep_ = 'not object'
        child_obj.dep_ = 'dobj'
        child_another_obj.dep_ = 'pobj'
        mock_get_proper_noun.side_effect = ['obj1', 'obj2']
        expected = ['obj1', 'obj2']

        actual = self.finder.get_objects_connected_to_token(token)

        self.assertListEqual(expected, actual)

    def test_that_get_proper_noun_returns_none_if_token_not_noun(self):
        token = MagicMock()
        token.pos_ = 'not noun'

        actual = self.finder.get_proper_noun(token)

        self.assertIsNone(actual)


    @patch.object(Relations_finder, 'get_compound_form')
    def test_that_get_proper_noun_returns_compound_form_of_propn_connected_to_noun(self, mock_get_compound_form):
        token = MagicMock()
        token.pos_ = 'PROPN'
        expected = 'fake compound form'
        mock_get_compound_form.return_value = expected

        actual = self.finder.get_proper_noun(token)

        self.assertEqual(expected, actual)

    @patch.object(Relations_finder, 'get_compound_form')
    def test_that_get_proper_noun_returns_compound_form_for_propn(self, mock_get_compound_form):
        child = MagicMock()
        token = MagicMock()
        token.rights = [child]
        token.pos_ = 'NOUN'
        child.pos_ = 'PROPN'
        expected = 'fake compound form'
        mock_get_compound_form.return_value = expected

        actual = self.finder.get_proper_noun(token)

        self.assertEqual(expected, actual)

    @patch.object(Relations_finder, 'get_compound_form')
    def test_that_get_proper_noun_returns_none_if_token_is_noun_with_no_propn_childs(self, mock_get_compound_form):
        child = MagicMock()
        token = MagicMock()
        token.rights = [child]
        token.pos_ = 'NOUN'
        child.pos_ = 'not PROPN'

        actual = self.finder.get_proper_noun(token)

        self.assertIsNone(actual)

    def test_that_get_compound_form_return_text_of_token_if_no_compound_child_found(self):
        token = MagicMock()
        expected = 'text form'
        token.text = expected
        token.lefts = []
        token.rights = []

        actual = self.finder.get_compound_form(token)

        self.assertEqual(expected, actual)

    def test_that_get_compound_form_return_correct_text_representation_of_token(self):
        token = MagicMock()
        left_child = MagicMock()
        right_child = MagicMock()
        left_child.dep_ = 'compound'
        right_child.dep_ = 'compound'
        token.pos_ = left_child.pos_ = right_child.pos_ = 'fake pos'
        left_text = 'foo'
        token_text = 'bar'
        right_text = 'baz'
        token.text = token_text
        left_child.text = left_text
        right_child.text = right_text
        token.lefts = [left_child]
        token.rights = [right_child]
        expected = f'{left_text} {token_text} {right_text}'

        actual = self.finder.get_compound_form(token)

        self.assertEqual(expected, actual)

    def test_that_get_proper_subject_returns_global_subject_if_token_is_pron(self):
        token = MagicMock()
        token.pos_ = 'PRON'
        expected = 'fake subject'
        temp = self.finder.subject
        self.finder.subject = expected

        actual = self.finder.get_proper_subject(token)

        self.assertEqual(expected, actual)
        self.finder.subject = temp

    @patch.object(Relations_finder, 'get_compound_form')
    def test_that_get_proper_subject_returns_compound_form_if_token_not_pron(self, mock_get_compound_form):
        token = MagicMock()
        token.pos_ = 'not PRON'
        expected = 'compound form'
        mock_get_compound_form.return_value = expected

        actual = self.finder.get_proper_subject(token)

        self.assertEqual(expected, actual)
