import sys
from neo4j import GraphDatabase
import time

class DBCLI:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.driver.verify_connectivity()

    def close(self):
        self.driver.close()

    def find_children(self, node_name):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Category {name: $node_name})-[:IS_PARENT_OF]->(child:Category) RETURN child.name AS child",
                node_name=node_name
            )
            return [record["child"] for record in result]

    def count_children(self, node_name):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Category {name: $node_name})-[:IS_PARENT_OF]->(child:Category) RETURN count(child) AS count",
                node_name=node_name
            )
            return result.single()["count"]

    def find_grandchildren(self, node_name):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (p:Category {name: $node_name})-[:IS_PARENT_OF]->(c:Category)-[:IS_PARENT_OF]->(gc:Category) RETURN gc.name AS grandchild",
                node_name=node_name
            )
            return [record["grandchild"] for record in result]

    def find_parents(self, node_name):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Category {name: $node_name})<-[:IS_PARENT_OF]-(parent:Category) RETURN parent.name AS parent",
                node_name=node_name
            )
            return [record["parent"] for record in result]

    def count_parents(self, node_name):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Category {name: $node_name})<-[:IS_PARENT_OF]-(parent:Category) RETURN count(parent) AS count",
                node_name=node_name
            )
            return result.single()["count"]
        
    def find_grandparents(self, node_name):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (gp:Category)-[:IS_PARENT_OF]->(p:Category)-[:IS_PARENT_OF]->(c:Category {name: $node_name}) RETURN gp.name AS grandparent",
                node_name=node_name
            )
            return [record["grandparent"] for record in result]

    def count_unique_nodes(self):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n:Category) RETURN count(DISTINCT n.name) AS count"
            )
            return result.single()["count"]

    def find_root_node(self):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Category) WHERE NOT (c)<-[:IS_PARENT_OF]-() RETURN c.name AS root_node"
            )
            return result.single()["root_node"]

    def find_nodes_with_most_children(self):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (p:Category)-[:IS_PARENT_OF]->(c:Category) "
                "WITH p, count(c) AS child_count "
                "RETURN p.name AS node, max(child_count) AS max_children "
                "ORDER BY max_children DESC"
            )
            if result.peek() is not None:
                max_children = result.peek()["max_children"]
                return [record["node"] for record in result if record["max_children"] == max_children]
            else:
                return []

    def find_nodes_with_least_children(self):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (p:Category)-[:IS_PARENT_OF]->(c:Category) "
                "WITH p, count(c) AS child_count "
                "RETURN p.name AS node, min(child_count) AS min_children "
                "ORDER BY min_children"
            )
            if result.peek() is not None:
                min_children = result.peek()["min_children"]
                return [record["node"] for record in result if record["min_children"] == min_children]
            else:
                return []

    def rename_node(self, old_name, new_name):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n:Category {name: $old_name}) SET n.name = $new_name RETURN n.name AS new_name",
                old_name=old_name,
                new_name=new_name
            )
            return result.single()["new_name"]
        
    def find_paths_between_nodes(self, start_node, end_node):
        with self.driver.session() as session:
            result = session.run(
                "MATCH path = (start:Category {name: $start_node})-[:IS_PARENT_OF*]->(end:Category {name: $end_node}) "
                "RETURN path",
                start_node=start_node,
                end_node=end_node
            )
            paths = [record["path"] for record in result]
            return paths



    def run_command(self, goal_number, node_name=None, another_node_name=None):
        start_time = time.time()
        if goal_number == "1":
            children = self.find_children(node_name)
            print("Children of node", node_name, ":", children)
        elif goal_number == "2":
            child_count = self.count_children(node_name)
            print("Number of children of node", node_name, ":", child_count)
        elif goal_number == "3":
            grandchildren = self.find_grandchildren(node_name)
            print("Grandchildren of node", node_name, ":", grandchildren)
        elif goal_number == "4":
            parents = self.find_parents(node_name)
            print("Parents of node", node_name, ":", parents)
        elif goal_number == "5":
            parent_count = self.count_parents(node_name)
            print("Number of parents of node", node_name, ":", parent_count)
        elif goal_number == "6":
            grandparents = self.find_grandparents(node_name)
            print("Grandparents of node", node_name, ":", grandparents)
        elif goal_number == "7":
            uniquely_named_node_count = self.count_unique_nodes()
            print("Number of uniquely named nodes:", uniquely_named_node_count)
        elif goal_number == "8":
            root_node = self.find_root_node()
            print("Root node:", root_node)
        elif goal_number == "9":
            nodes_with_most_children = self.find_nodes_with_most_children()
            print("Nodes with the most children:", nodes_with_most_children)
        elif goal_number == "10":
            nodes_with_least_children = self.find_nodes_with_least_children()
            print("Nodes with the least children:", nodes_with_least_children)
        elif goal_number == "11":
            renamed_node = self.rename_node(node_name, another_node_name)
            print("Node renamed. New name:", renamed_node)
        elif goal_number == "12":
            paths = self.find_paths_between_nodes(node_name, another_node_name)
            print("Paths between", node_name, "and", another_node_name, ":", paths)
        else:
            print("Invalid goal number.")

        end_time = time.time()
        print("Time taken for the query:", end_time - start_time, "seconds")


    def start(self):
        if len(sys.argv) < 2:
            print("Usage: dbcli <goal_number> [optional_node_name]")
            return

        goal_number = sys.argv[1]
        if len(sys.argv) == 3:
            node_name = sys.argv[2]
            another_node_name = None
        elif len(sys.argv) == 4:
            node_name = sys.argv[2]
            another_node_name = sys.argv[3]
        else:
            node_name = None
            another_node_name = None

        self.run_command(goal_number, node_name, another_node_name)


if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "password"

    dbcli = DBCLI(uri, user, password)
    dbcli.start()
    dbcli.close()
