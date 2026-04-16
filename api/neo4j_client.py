import os
from neo4j import GraphDatabase

class Neo4jClient:
    def __init__(self):
        self.driver = None

    def _get_driver(self):
        if self.driver is None:
            uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
            user = os.environ.get("NEO4J_USER", "neo4j")
            password = os.environ.get("NEO4J_PASSWORD", "neo4jpassword")
            try:
                self.driver = GraphDatabase.driver(uri, auth=(user, password))
            except Exception as e:
                print(f"FAILED to initialize Neo4j driver: {e}")
                return None
        return self.driver

    def close(self):
        if self.driver:
            self.driver.close()

    def create_project_node(self, project_id, name):
        driver = self._get_driver()
        if not driver:
            return
        with driver.session() as session:
            session.write_transaction(self._create_and_return_project, project_id, name)

    @staticmethod
    def _create_and_return_project(tx, project_id, name):
        query = (
            "MERGE (p:Project { id: $project_id }) "
            "SET p.name = $name "
            "RETURN p"
        )
        return tx.run(query, project_id=str(project_id), name=name)

# Initialize a singleton connection manager
neo4j_client = Neo4jClient()
