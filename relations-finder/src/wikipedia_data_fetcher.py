import re

import wikipedia


class Wikipedia_data_fetcher:
    def get_article(self, article_name):
        result = {}
        try:
            page = wikipedia.page(f'"{article_name}"')
            result['name'] = page.title
            result['url'] = page.url
            result['content_chunks'] = self.chunk_page_content(page)
        except wikipedia.exceptions.PageError:
            pass
        return result

    def get_sections_titels(self, content):
        return [x.group(1) for x in re.finditer('[\\n]+=+ +([A-Za-z ]+) +=+[\\n]+', content)]

    def filter_sections(self, sections):
        sections_to_remove = {'Publications', 'References', 'External links', 'Further reading'}
        return [section for section in sections if section not in sections_to_remove]

    def clean_text(self, text):
        return text.replace('\"', '').replace('\n', ' ')

    def chunk_page_content(self, page):
        result = [self.clean_text(page.summary)]
        sections = self.get_sections_titels(page.content)
        filtered_sections = self.filter_sections(sections)
        for section in filtered_sections:
            result.append(self.clean_text(page.section(section)))
        return result
