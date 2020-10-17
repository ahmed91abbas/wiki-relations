from neo4j import GraphDatabase


class Neo4j_handler:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, qid, name, url):
        with self.driver.session() as session:
            session.write_transaction(self._create_node, qid, name, url)

    def create_directed_edge(self, from_qid, to_qId, relation, sentence, relation_url):
        with self.driver.session() as session:
            session.write_transaction(self._create_directed_edge, from_qid, to_qId, relation, sentence, relation_url)

    def clean_gdb(self):
        with self.driver.session() as session:
            session.write_transaction(self._clean_gdb)

    @staticmethod
    def _create_node(tx, qid, name, url):
        result = tx.run('MERGE (a:Person {qid:$qid}) '
                        'SET a.name = $name '
                        'SET a.url = $url', qid=qid, name=name, url=url)
        return result

    @staticmethod
    def _create_directed_edge(tx, from_qid, to_qid, relation, sentence, relation_url):
        result = tx.run('MATCH (a:Person),(b:Person) WHERE a.qid = $from_qid AND b.qid = $to_qid '
                        f'MERGE (a)-[r:{relation} '
                        '{ relation:$relation, sentence:$sentence, relation_url:$relation_url }]->(b)'
                        'RETURN type(r), r.relation',
                        from_qid=from_qid, to_qid=to_qid, relation=relation, sentence=sentence,
                        relation_url=relation_url)
        return result

    @staticmethod
    def _clean_gdb(tx):
        result = tx.run('MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n, r')
        return result
