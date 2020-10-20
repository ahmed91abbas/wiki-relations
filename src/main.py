import os
import click
from neo4j_handler import Neo4j_handler
from relations_finder import Relations_finder


@click.group()
def cli():
    pass


@cli.command('create-graph')
def create_graph():
    gdb = Neo4j_handler(os.environ['NEO4J_URI'], os.environ['NEO4J_USERNAME'],
                        os.environ['NEO4J_PASSWORD'])
    # TODO replace with actual data
    for i in range(5):
        qid = str(i)
        gdb.create_node(qid, f'person{qid}', f'http://{qid}.com')
    gdb.create_directed_edge('1', '2', 'relation12', 'sentence12', 'relation_url12')
    gdb.create_directed_edge('2', '1', 'relation21', 'sentence21', 'relation_url21')
    gdb.create_directed_edge('2', '3', 'relation23', 'sentence23', 'relation_url23')


@cli.command('clean-graph')
def clean_graph():
    gdb = Neo4j_handler(os.environ['NEO4J_URI'], os.environ['NEO4J_USERNAME'],
                        os.environ['NEO4J_PASSWORD'])
    gdb.clean_gdb()


@cli.command('find-relations')
def find_relations():
    finder = Relations_finder()
    result = finder.find_relations('Foo influenced Bar.')
    print(result)


if __name__ == '__main__':
    cli()
