import os
import sys
from unittest import TestCase
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath('..'))
from relations_finder import Relations_finder


class Test_relations_finder(TestCase):

    def setUp(self):
        self.finder = Relations_finder()
        self.data = {
            'name': 'Foo Bar',
            'url': 'test.com',
            'content_chunks': []
        }

    @patch.object(Relations_finder, 'generate_html')
    def test_for_subject_verb_object(self, mock_generate_html):
        sentence = 'Foo influenced Bar.'
        self.data['content_chunks'] = [sentence]
        expected = {
            'objects': ['Bar'],
            'relation': 'influence',
            'sentence': sentence,
            'subject': 'Foo Bar'
        }

        actual = self.finder.find_relations(self.data)['relations'][0]

        self.assertDictEqual(expected, actual)

    @patch.object(Relations_finder, 'generate_html')
    def test_for_pronoun_verb_object(self, mock_generate_html):
        sentence = 'He influenced Bar.'
        self.data['content_chunks'] = [sentence]
        expected = {
            'objects': ['Bar'],
            'relation': 'influence',
            'sentence': sentence,
            'subject': self.data['name']
        }

        actual = self.finder.find_relations(self.data)['relations'][0]

        self.assertDictEqual(expected, actual)
