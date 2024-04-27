from neo4j import GraphDatabase

class Neo4jUtility:
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        self.driver.verify_connectivity()

    def close(self):
        self.driver.close()
    
    def create_index(self):
        with self.driver.session() as session:
            session.run("CREATE INDEX ON :Category(name)")


    def find_children(self, node_name):
        with self.driver.session() as session:
            result = session.run("MATCH (c:Category {name: $nodeName})-[:SUBCATEGORY]->(s:Category ) RETURN s.name AS child", nodeName=node_name)
            children = [record["child"] for record in result]
            return children

    def count_children(self, node_name):
        with self.driver.session() as session:
            result = session.run("MATCH (c:Category{name: $nodeName})-[:SUBCATEGORY]->(s:Category) RETURN count(s) AS childCount", nodeName=node_name)
            child_count = result.single()["childCount"]
            return child_count


    def find_grandchildren(self, node_name):
        with self.driver.session() as session:
            result = session.run("MATCH (p:Category {name: $nodeName})-[:SUBCATEGORY]->(:Category)-[:SUBCATEGORY]->(gc:Category) RETURN gc.name AS grandchild", nodeName=node_name)
            grandchildren = [record["grandchild"] for record in result]
            return grandchildren


    def find_parents(self, node_name):
        with self.driver.session() as session:
            result = session.run("MATCH (c:Category)-[:SUBCATEGORY]->(p:Category {name: $nodeName}) RETURN c.name AS parent", nodeName=node_name)
            parents = [record["parent"] for record in result]
            return parents


    def count_parents(self, node_name):
        with self.driver.session() as session:
            result = session.run("MATCH (c:Category)-[:SUBCATEGORY]->(p:Category {name: $nodeName}) RETURN count(c) AS parentCount", nodeName=node_name)
            parent_count = result.single()["parentCount"]
            return parent_count


    def find_grandparents(self, node_name):
        with self.driver.session() as session:
            result = session.run("MATCH (c:Category)-[:SUBCATEGORY]->(:Category)-[:SUBCATEGORY]->(gp:Category {name: $nodeName}) RETURN DISTINCT c.name AS grandParent", nodeName=node_name)
            grand_parents = [record["grandParent"] for record in result]
            return grand_parents


    def count_unique_nodes(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n:Category) RETURN COUNT(DISTINCT n.name) AS uniqueCount")
            unique_count = result.single()["uniqueCount"]
            return unique_count
 

    def find_root_node(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n:Category) WHERE NOT (:Category)-[:SUBCATEGORY]->(n) RETURN n.name AS root")
            root_node = result.single()["root"]
            return root_node


    def find_nodes_with_most_children(self):
        with self.driver.session() as session:
            result = session.run("MATCH (c:Category)-[:SUBCATEGORY]->(s:Category) "
                                "RETURN c.name AS node, COUNT(s) AS childCount "
                                "ORDER BY childCount DESC")
            nodes = [record["node"] for record in result]
            return nodes


    def find_nodes_with_least_children(self):
        with self.driver.session() as session:
            result = session.run("MATCH (c:Category)-[:SUBCATEGORY]->(s:Category) "
                                "WITH c.name AS node, COUNT(s) AS childCount "
                                "ORDER BY childCount ASC "
                                "MATCH (n:Category {name: node, childCount: childCount}) "
                                "RETURN n.name AS node")
            nodes = [record["node"] for record in result]
            return nodes

    def rename_node(self, old_name, new_name):
        with self.driver.session() as session:
            result = session.run("MATCH (n:Category {name: $oldName}) "
                                 "SET n.name = $newName "
                                 "RETURN n.name AS newName", oldName=old_name, newName=new_name)
            new_name = result.single()["newName"]
            return new_name
        
    def run_command(self, command):
        if command == "1":
            node_name = input("Enter the node name: ")
            children = self.find_children(node_name)
            print("Children of node", node_name, ":", children)
        elif command == "2":
            node_name = input("Enter the node name: ")
            child_count = self.count_children(node_name)
            print("Number of children of node", node_name, ":", child_count)
        elif command == "3":
            node_name = input("Enter the node name: ")
            grandchildren = self.find_grandchildren(node_name)
            print("Grandchildren of node", node_name, ":", grandchildren)
        elif command == "4":
            node_name = input("Enter the node name: ")
            parents = self.find_parents(node_name)
            print("Parents of node", node_name, ":", parents)
        elif command == "5":
            node_name = input("Enter the node name: ")
            parent_count = self.count_parents(node_name)
            print("Number of parents of node", node_name, ":", parent_count)
        elif command == "6":
            node_name = input("Enter the node name: ")
            grandparents = self.find_grandparents(node_name)
            print("Grandparents of node", node_name, ":", grandparents)
        elif command == "7":
            uniquely_named_node_count = self.count_unique_nodes()
            print("Number of uniquely named nodes:", uniquely_named_node_count)
        elif command == "8":
            root_node = self.find_root_node()
            print("Root node:", root_node)
        elif command == "9":
            nodes_with_most_children = self.find_nodes_with_most_children()
            print("Nodes with the most children:", nodes_with_most_children)
        elif command == "10":
            nodes_with_least_children = self.find_nodes_with_least_children()
            print("Nodes with the least children:", nodes_with_least_children)
        elif command == "11":
            old_name = input("Enter the node's old name: ")
            new_name = input("Enter the node's new name: ")
            renamed_node = self.rename_node(old_name, new_name)
            print("Node renamed. New name:", renamed_node)
        else:
            print("Invalid command.")

    def start(self):
        while True:
            print("COMMANDS:")
            print("1. Finds all children of a given node")
            print("2. Counts all children of a given node")
            print("3. Finds all grandchildren of a given node")
            print("4. Finds all parents of a given node")
            print("5. Counts all parents of a given node")
            print("6. Finds all grandparents of a given node")
            print("7. Counts how many uniquely named nodes there are")
            print("8. Finds a root node, one which is not a subcategory of any other node")
            print("9. Finds nodes with the most children")
            print("10. Finds nodes with the least children")
            print("11. Renames a given node")
            print("0. Exit")

            command = input("Enter command number: ")
            if command == "0":
                print("Exiting...")
                break

            self.run_command(command)

# ------------------------------------------------------------------------
uri = "bolt://localhost:7687"  
username = "neo4j"  
password = "password" 

utility = Neo4jUtility(uri, username, password)
utility.start()
utility.close()
