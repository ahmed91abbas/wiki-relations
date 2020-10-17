import os
import sys
import unittest
import mock

sys.path.append(os.path.abspath('..'))
from neo4j_handler import Neo4j_handler


class Test_neo4j_handler(unittest.TestCase):

    @mock.patch('neo4j_handler.GraphDatabase.driver')
    def setUp(self, mock_driver):
        self.gdb = Neo4j_handler('', '', '')

    @mock.patch('neo4j_handler.GraphDatabase.driver')
    def test_that_init_creates_driver_with_correct_args(self, mock_driver):
        uri = 'foo.com'
        user = 'foo'
        password = 'bar'

        Neo4j_handler(uri, user, password)

        mock_driver.assert_called_once_with(uri, auth=(user, password))

    @mock.patch('neo4j_handler.GraphDatabase.driver')
    def test_that_close_calls_driver_close_once(self, mock_driver):
        self.gdb.close()

        self.gdb.driver.close.assert_called_once()

    @mock.patch('neo4j_handler.GraphDatabase.driver')
    def test_that_close_calls_driver_close_once(self, mock_driver):
        self.gdb.close()

        self.gdb.driver.close.assert_called_once()

    def test_that_create_node_runs_correct_query(self):
        tx = mock.MagicMock()
        qid = 'foo'
        name = 'bar'
        url = 'baz'

        self.gdb._create_node(tx, qid, name, url)

        tx.run.assert_called_once_with('MERGE (a:Person {qid:$qid}) SET a.name = $name SET a.url = $url',
                                       qid=qid, name=name, url=url)

    def test_that_create_directed_edge_runs_correct_query(self):
        tx = mock.MagicMock()
        from_qid = 'foo'
        to_qid = 'bar'
        relation = 'baz'
        sentence = 'foobar'
        relation_url = 'foo.com'

        self.gdb._create_directed_edge(tx, from_qid, to_qid, relation, sentence, relation_url)

        tx.run.assert_called_once_with('MATCH (a:Person),(b:Person) WHERE a.qid = $from_qid AND b.qid = $to_qid '
                                       f'MERGE (a)-[r:{relation} '
                                       '{ relation:$relation, sentence:$sentence, relation_url:$relation_url }]->(b)'
                                       'RETURN type(r), r.relation',
                                       from_qid=from_qid, to_qid=to_qid, relation=relation, sentence=sentence,
                                       relation_url=relation_url)

    def test_that_clean_gdb_runs_correct_query(self):
        tx = mock.MagicMock()

        self.gdb._clean_gdb(tx)

        tx.run.assert_called_once_with('MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n, r')
