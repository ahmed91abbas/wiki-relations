import click
from relations_finder import Relations_finder
from wikipedia_data_fetcher import Wikipedia_data_fetcher


@click.group()
def cli():
    pass


@cli.command('find-relations')
def find_relations():
    data = {
        'name': 'Foo Bar',
        'url': 'foo.bar.com',
        'content_chunks': [
            'Foo influenced Bar.',
        ]
    }
    finder = Relations_finder()
    result = finder.find_relations(data)
    print(result)


@cli.command('find-article')
def find_article():
    result = Wikipedia_data_fetcher().get_article('bill')
    print(result)


if __name__ == '__main__':
    cli()
