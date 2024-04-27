from neo4j import GraphDatabase
import time

class DBCLI:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.driver.verify_connectivity()

    def close(self):
        self.driver.close()

    def count_nodes(self):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n) RETURN count(n) AS count"
            )
            return result.single()["count"]


    def find_children(self, node_name):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Category {name: $node_name})-[:IS_PARENT_OF]->(child:Subcategory) RETURN child.name",
                node_name=node_name
            )
            return [record["child.name"] for record in result]

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
                "MATCH (c:Category {name: $node_name})-[:IS_PARENT_OF]->(child:Subcategory)-[:IS_PARENT_OF]->(grandchild:Subcategory) RETURN grandchild.name",
                node_name=node_name
            )
            return [record["grandchild.name"] for record in result]

    def find_parents(self, node_name):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Category {name: $node_name})<-[:IS_PARENT_OF]-(parent:Category) RETURN parent.name",
                node_name=node_name
            )
            return [record["parent.name"] for record in result]

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
                "MATCH (c:Category {name: $node_name})<-[:IS_PARENT_OF]-(parent:Category)<-[:IS_PARENT_OF]-(grandparent:Category) RETURN grandparent.name",
                node_name=node_name
            )
            return [record["grandparent.name"] for record in result]

    def count_unique_nodes(self):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Category) RETURN count(DISTINCT c.name) AS count"
            )
            return result.single()["count"]

    def find_root_nodes(self):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Category) WHERE NOT (c)<-[:IS_PARENT_OF]-() RETURN c.name"
            )
            return [record["c.name"] for record in result]

    def find_nodes_with_most_children(self):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Category)-[:IS_PARENT_OF]->(child:Subcategory) WITH c, count(child) AS child_count RETURN c.name, max(child_count) AS max_count"
            )
            max_count = result.single()["max_count"]
            result = session.run(
                "MATCH (c:Category)-[:IS_PARENT_OF]->(child:Subcategory) WITH c, count(child) AS child_count WHERE child_count = $max_count RETURN c.name",
                max_count=max_count
            )
            return [record["c.name"] for record in result]

    def find_nodes_with_least_children(self):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Category)-[:IS_PARENT_OF]->(child:Subcategory) WITH c, count(child) AS child_count WHERE child_count > 0 RETURN c.name, min(child_count) AS min_count"
            )
            min_count = result.single()["min_count"]
            result = session.run(
                "MATCH (c:Category)-[:IS_PARENT_OF]->(child:Subcategory) WITH c, count(child) AS child_count WHERE child_count = $min_count RETURN c.name",
                min_count=min_count
            )
            return [record["c.name"] for record in result]

    def rename_node(self, old_name, new_name):
        with self.driver.session() as session:
            session.run(
                "MATCH (c:Category {name: $old_name}) SET c.name = $new_name",
                old_name=old_name, new_name=new_name
            )

    def find_paths_between_nodes(self, node1, node2):
        with self.driver.session() as session:
            result = session.run(
                "MATCH path = allShortestPaths((c1:Category {name: $node1})-[:IS_PARENT_OF*]->(c2:Category {name: $node2})) RETURN path",
                node1=node1, node2=node2
            )
            return [record["path"] for record in result]
        

        
    def run_command(self, command):
        if command == "1":
            node_name = input("Enter the node name: ")
            start_time = time.time()
            children = self.find_children(node_name)
            end_time = time.time()  
            print("Children of node", node_name, ":", children)
            print("Time taken for the query:", end_time - start_time, "seconds")
        elif command == "2":
            node_name = input("Enter the node name: ")
            start_time = time.time()
            child_count = self.count_children(node_name)
            end_time = time.time()  
            print("Number of children of node", node_name, ":", child_count)
            print("Time taken for the query:", end_time - start_time, "seconds")
            
        elif command == "3":
            node_name = input("Enter the node name: ")
            start_time = time.time()
            grandchildren = self.find_grandchildren(node_name)
            end_time = time.time()
            print("Grandchildren of node", node_name, ":", grandchildren)
            print("Time taken for the query:", end_time - start_time, "seconds")
        elif command == "4":
            node_name = input("Enter the node name: ")
            start_time = time.time()
            parents = self.find_parents(node_name)
            end_time = time.time()  
            print("Parents of node", node_name, ":", parents)
            print("Time taken for the query:", end_time - start_time, "seconds")
        elif command == "5":
            node_name = input("Enter the node name: ")
            start_time = time.time()
            parent_count = self.count_parents(node_name)
            end_time = time.time()  
            print("Number of parents of node", node_name, ":", parent_count)
            print("Time taken for the query:", end_time - start_time, "seconds")
        elif command == "6":
            node_name = input("Enter the node name: ")
            start_time = time.time()
            grandparents = self.find_grandparents(node_name)
            end_time = time.time()  
            print("Grandparents of node", node_name, ":", grandparents)
            print("Time taken for the query:", end_time - start_time, "seconds")
        elif command == "7":
            start_time = time.time()
            uniquely_named_node_count = self.count_unique_nodes()
            end_time = time.time()  
            print("Number of uniquely named nodes:", uniquely_named_node_count)
            print("Time taken for the query:", end_time - start_time, "seconds")
        elif command == "8":
            start_time = time.time()
            root_node = self.find_root_node()
            end_time = time.time()  
            print("Root node:", root_node)
            print("Time taken for the query:", end_time - start_time, "seconds")
        elif command == "9":
            start_time = time.time()
            nodes_with_most_children = self.find_nodes_with_most_children()
            end_time = time.time()  
            print("Nodes with the most children:", nodes_with_most_children)
            print("Time taken for the query:", end_time - start_time, "seconds")
        elif command == "10":
            start_time = time.time()
            nodes_with_least_children = self.find_nodes_with_least_children()
            end_time = time.time()  
            print("Nodes with the least children:", nodes_with_least_children)
            print("Time taken for the query:", end_time - start_time, "seconds")
        elif command == "11":
            start_time = time.time()
            old_name = input("Enter the node's old name: ")
            new_name = input("Enter the node's new name: ")
            renamed_node = self.rename_node(old_name, new_name)
            end_time = time.time()  
            print("Node renamed. New name:", renamed_node)
            print("Time taken for the query:", end_time - start_time, "seconds")
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



if __name__ == "__main__":
    uri = "bolt://localhost:7687/neo4j"
    user = "neo4j"
    password = "password"

    dbcli = DBCLI(uri, user, password)
    # dbcli.start()
    # dbcli.close()












    # # Example usage
    # start_time = time.time()
    # end_time = time.time()
    # print("Time taken for finding children:", end_time - start_time, "seconds")
    # children = dbcli.find_children("1880s_films")
    # print("Children:", children)

    # start_time = time.time()

    # records, summary, keys = dbcli.driver.execute_query(
    #     "MATCH (n) RETURN COUNT(n) AS count",
    #     database_="neo4j",
    # )

    # print(records, summary, keys)   

    count = dbcli.count_nodes()
    print("Count of children:", count)

    # Similarly, test other methods for all goals

    dbcli.close()
