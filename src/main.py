import os
import click
from neo4j_handler import Neo4j_handler


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = Neo4j_handler(os.environ['NEO4J_URI'],
                            os.environ['NEO4J_USERNAME'],
                            os.environ['NEO4J_PASSWORD'])


@cli.command('create-graph')
@click.pass_context
def create_graph(ctx):
    # TODO replace with actual data
    for i in range(5):
        qid = str(i)
        ctx.obj.create_node(qid, f'person{qid}', f'http://{qid}.com')
    ctx.obj.create_directed_edge('1', '2', 'relation12', 'sentence12', 'relation_url12')
    ctx.obj.create_directed_edge('2', '1', 'relation21', 'sentence21', 'relation_url21')
    ctx.obj.create_directed_edge('2', '3', 'relation23', 'sentence23', 'relation_url23')


@cli.command('clean-graph')
@click.pass_context
def clean_graph(ctx):
    ctx.obj.clean_gdb()


if __name__ == '__main__':
    cli()
