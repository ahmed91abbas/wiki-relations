import os
import sys
from unittest import TestCase
from unittest.mock import patch

import wikipedia

sys.path.append(os.path.abspath('..'))
from wikipedia_data_fetcher import Wikipedia_data_fetcher


class Test_wikipedia_data_fetcher(TestCase):

    def setUp(self):
        self.fetcher = Wikipedia_data_fetcher()

    @patch('wikipedia_data_fetcher.wikipedia.page')
    @patch.object(Wikipedia_data_fetcher, 'chunk_page_content')
    def test_that_get_article_returns_correct_result(self, mock_chunk_page_content,
                                                     mock_wikipedia_page):
        url = 'fake url'
        title = 'fake title'
        content = 'fake content'
        class Object:
            def __init__(self):
                self.url = url
                self.title = title
        mock_wikipedia_page.return_value = Object()
        mock_chunk_page_content.return_value = content
        expected =  {'name': title, 'url': url, 'content_chunks': content}

        actual = self.fetcher.get_article('')

        self.assertDictEqual(expected, actual)

    @patch('wikipedia_data_fetcher.wikipedia.page')
    def test_that_get_article_returns_empty_dict_on_page_error(self, mock_wikipedia_page):
        page_error = wikipedia.exceptions.PageError('fake page id')
        mock_wikipedia_page.side_effect = page_error
        expected =  {}

        actual = self.fetcher.get_article('')

        self.assertDictEqual(expected, actual)

    def test_that_get_section_titles_strips_title_names_from_text(self):
        content = '\n\n\n= First Title =\n text...\n\n\n== Second Title '\
                  '==\n\n more text...\n=== Sub Title ===\n finish.'
        expected = ['First Title', 'Second Title', 'Sub Title']

        actual = self.fetcher.get_sections_titels(content)

        self.assertListEqual(expected, actual)

    def test_that_filter_sections_removes_unwanted_sections(self):
        sections = ['Foo', 'Publications', 'References', 'External links', 'Further reading', 'Bar']
        sections_to_remove = {'Publications', 'References', 'External links', 'Further reading'}
        expected = ['Foo', 'Bar']

        actual = self.fetcher.filter_sections(sections)

        self.assertListEqual(expected, actual)

    def test_that_clean_text_removes_quotes_and_newlines(self):
        text = 'Some text\n"quoted text"\nend.'
        expected = 'Some text quoted text end.'

        actual = self.fetcher.clean_text(text)

        self.assertEqual(expected, actual)

    def test_that_chunk_page_content_returns_list_with_sections_contents(self):
        summary = 'summary'
        content = '\n= Foo =\nFirst chunk\n\n== Bar ==\nSecond chunk.'
        expected = ['summary', 'First chunk', 'Second chunk.']
        class Object:
            def __init__(self):
                self.summary = summary
                self.content = content
            def section(self, title):
                if title == 'Foo':
                    return 'First chunk'
                elif title == 'Bar':
                    return 'Second chunk.'

        actual = self.fetcher.chunk_page_content(Object())

        self.assertEqual(expected, actual)
