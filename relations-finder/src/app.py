import json
import os

from flask import Flask, request, Response
from neo4j_handler import Neo4j_handler
from relations_finder import Relations_finder
from wikipedia_data_fetcher import Wikipedia_data_fetcher


app = Flask(__name__)
wiki = Wikipedia_data_fetcher()
finder = Relations_finder()
gdb = Neo4j_handler(os.environ['NEO4J_URI'], os.environ['NEO4J_USERNAME'],
                    os.environ['NEO4J_PASSWORD'])


@app.route('/relations-finder', methods=['POST'])
def find_relations():
    request_data = request.get_json()
    if not request_data or 'title' not in request_data:
        return Response('no data', status=400)
    data = process(request_data['title'])
    return Response(json.dumps(data), status=200, mimetype='application/json')


def process(title):
    wiki_data = wiki.get_article(title)
    wiki_relations = finder.find_relations(wiki_data)
    for relation in wiki_relations['relations']:
        gdb.create_node(relation['subject'], relation['subject'], wiki_relations['url'])
        for relation_object in relation['objects']:
            gdb.create_node(relation_object, relation_object, '')
            gdb.create_directed_edge(relation['subject'], relation_object, relation['relation'],
                                     relation['sentence'], wiki_relations['url'])
    return wiki_relations


if __name__ == "__main__":
    app.run(threaded=True, host=os.environ['FLASK_HOST'], port=os.environ['FLASK_PORT'])
