import os
import sys
from unittest import TestCase
from unittest.mock import MagicMock, patch

from neo4j import exceptions

sys.path.append(os.path.abspath('..'))
from neo4j_handler import Neo4j_handler


class Test_neo4j_handler(TestCase):

    @patch('neo4j_handler.GraphDatabase.driver')
    def setUp(self, mock_driver):
        self.gdb = Neo4j_handler('', '', '')

    @patch.object(Neo4j_handler, 'connect_to_database_with_retry')
    def test_that_init_calls_connect_to_database_with_retry_with_correct_args(self, mock_connect):
        uri = 'foo.com'
        user = 'foo'
        password = 'bar'

        Neo4j_handler(uri, user, password)

        mock_connect.assert_called_once_with(uri, user, password, max_retry_count=5)

    @patch('neo4j_handler.GraphDatabase.driver')
    def test_that_connect_to_database_with_retry_returns_gdb_driver(self, mock_driver):
        uri = 'foo.com'
        user = 'foo'
        password = 'bar'
        driver = 'fake driver'
        mock_driver.return_value = driver

        actual = self.gdb.connect_to_database_with_retry(uri, user, password)

        mock_driver.assert_called_once_with(uri, auth=(user, password))
        self.assertEqual(driver, actual)

    @patch('neo4j_handler.time.sleep')
    @patch('neo4j_handler.GraphDatabase.driver')
    def test_that_connect_to_database_with_retry_returns_None_after_retry_count(self, mock_driver, mock_sleep):
        max_retry_count = 3
        mock_driver.side_effect = exceptions.ServiceUnavailable

        actual = self.gdb.connect_to_database_with_retry('', '', '', max_retry_count=max_retry_count)

        self.assertEqual(mock_driver.call_count, max_retry_count)
        self.assertEqual(None, actual)

    def test_that_close_calls_driver_close_once(self):
        self.gdb.close()

        self.gdb.driver.close.assert_called_once()

    def test_that_create_node_runs_correct_query(self):
        tx = MagicMock()
        qid = 'foo'
        name = 'bar'
        url = 'baz'

        self.gdb._create_node(tx, qid, name, url)

        tx.run.assert_called_once_with('MERGE (a:Node {qid:$qid}) SET a.name = $name SET a.url = $url',
                                       qid=qid, name=name, url=url)

    def test_that_create_directed_edge_runs_correct_query(self):
        tx = MagicMock()
        from_qid = 'foo'
        to_qid = 'bar'
        relation = 'baz'
        sentence = 'foobar'
        relation_url = 'foo.com'

        self.gdb._create_directed_edge(tx, from_qid, to_qid, relation, sentence, relation_url)

        tx.run.assert_called_once_with('MATCH (a:Node),(b:Node) WHERE a.qid = $from_qid AND b.qid = $to_qid '
                                       f'MERGE (a)-[r:{relation} '
                                       '{ relation:$relation, sentence:$sentence, relation_url:$relation_url }]->(b)'
                                       'RETURN type(r), r.relation',
                                       from_qid=from_qid, to_qid=to_qid, relation=relation, sentence=sentence,
                                       relation_url=relation_url)

    def test_that_clean_gdb_runs_correct_query(self):
        tx = MagicMock()

        self.gdb._clean_gdb(tx)

        tx.run.assert_called_once_with('MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n, r')
