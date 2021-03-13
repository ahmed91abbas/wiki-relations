import os
import sys
from unittest import TestCase
from unittest.mock import MagicMock, patch
from parameterized import parameterized

sys.path.append(os.path.abspath('..'))
from relations_finder import Relations_finder


class Test_relations_finder(TestCase):

    def setUp(self):
        self.finder = Relations_finder()

    @parameterized.expand([
        ('Test influenced Baz.', 'Test', 'influence', ['Baz']),
        ('He influenced Baz.', 'Foo Bar', 'influence', ['Baz']),
        ('Bar influenced Foo.', 'Foo Bar', 'influence', ['Foo Bar']),
        ('he met fellow student Fake Name.', 'Foo Bar', 'meet', ['Fake Name']),
        ('Anna was also influenced by Fake Name, Ahmed, Carl Xon and Toto.', 'Anna', 'influence by', ['Fake Name', 'Ahmed', 'Carl Xon', 'Toto']),
        ('Goe eats exotic street food.', 'Goe', 'eat', ['exotic street food']),
    ])
    @patch.object(Relations_finder, 'generate_html')
    def test_for_subject_verb_object(self, sentence, subject, relation, objects, mock_generate_html):
        data = {
            'name': 'Foo Bar',
            'url': 'test.com',
            'content_chunks': [sentence]
        }
        expected = {
            'subject': subject,
            'relation': relation,
            'objects': objects,
            'sentence': sentence,
        }

        actual = self.finder.find_relations(data)['relations'][0]

        self.assertDictEqual(expected, actual)
