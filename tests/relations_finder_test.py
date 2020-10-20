import os
import sys
import unittest
import mock

sys.path.append(os.path.abspath('..'))
from relations_finder import Relations_finder


class Test_relations_finder(unittest.TestCase):

    def setUp(self):
        self.finder = Relations_finder()

    @mock.patch.object(Relations_finder, 'generate_html')
    def test_that_find_relations_returns_correct_result(self, mock_generate_html):
        sentence = 'Foo influenced Bar.'
        expected = {'subject': 'Foo', 'objects': ['Bar'], 'relation': 'influence'}

        actual = self.finder.find_relations(sentence)

        self.assertDictEqual(expected, actual)

    @mock.patch('relations_finder.displacy.render')
    def test_that_generate_html_renders_new_html_file(self, mock_render):
        nlp_doc = 'fake data'
        mock_render.return_value = 'fake html content'

        self.finder.generate_html(nlp_doc)

        mock_render.assert_called_once_with([nlp_doc], style='dep', page=True)
