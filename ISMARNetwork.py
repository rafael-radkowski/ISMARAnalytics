
from collections import deque


class ISMARNetwork:


    author_db = None
    paper_db = None

    connections = dict()

    weighted_graph = dict()


    Billinghurst_penalty = 20



    def __init__(self, author_db_, paper_db_):
        self.author_db = author_db_
        self.paper_db = paper_db_

        self.__init_network()


    def CalculateBillinghurstDistance(self, last_name, first_name):

        mb = self.__getAuthor( "M.", "Billinghurst")
        author = self.__getAuthor(first_name, last_name)


        return self.__shortest_distance(author.id, mb.id)





    def __init_network(self):

        # Go through all authors and look for all co-authors in a particular year.
        # connections[i][j]    connection from to. id and j are author ids


        for authors in self.author_db.values():

            for author in authors:

                for paper_id in author.paper_list:

                    paper = self.paper_db.db[paper_id]

                    author_id = author.id

                    if author_id not in self.connections:
                        self.connections[author_id] = list()

                    for coauthor in paper.authors:


                        co_id = self.__getAuthorId(coauthor.last_name, coauthor.first_name)
                        if co_id == author_id:
                            continue



                        self.connections[author_id].append(co_id)


        # create a weighted graph


        num_nodes = 0

        for node in self.connections.keys():

            for edge in self.connections[node]:

                if node not in self.weighted_graph:
                    self.weighted_graph[node] = dict()

                if edge not in self.weighted_graph[node]:
                    self.weighted_graph[node][edge] = 0

                self.weighted_graph[node][edge] = self.weighted_graph[node][edge] + 1


    def __getAuthorById(self, id):

        # exhaustive search. That can go better

        for authors in self.author_db.values():

            for author in authors:

                if author.id == id:
                    return author


    def __getAuthorId(self, last_name, first_name):
        if last_name not in self.author_db:
            print("Author " + last_name + " not in db")
            return -1

        authors = self.author_db[last_name]

        for aa in authors:
            if aa.first_name == first_name:
                return aa.id


    def __getAuthor(self, first_name, last_name):

        matches = self.author_db[last_name]

        for a in matches:
            if a.first_name == first_name:
                return a

        return None



    def __shortest_distance(self, from_id, to_id):


        if from_id == to_id:
            return 0, [from_id]


        # Search for connected components / topological search

        visited = list()
        num_groups = 0
        path = list()

        distance = 0

        queue = deque()


        # for all nodes
        queue.append((from_id, 0 ))



        if from_id not in self.weighted_graph:
            return self.Billinghurst_penalty, [] # author is not in graph, means the author has no connections

        num_hops = 0 # the graph can be considered as unweighted. Thus, find the number of dfs hops.

        # breath first search
        while len(queue) > 0:

            current_node = queue.popleft()
            visited.append(current_node[0])

            path.append(current_node[0])

            if current_node[0] == to_id:
                distance = current_node[1] + 1
                break

            childs =self.weighted_graph[current_node[0]]

            for child in self.weighted_graph[current_node[0]].keys():

                if child in visited or child in queue:
                    continue

                queue.append((child, current_node[1] + 1))


        walked_path = []

        if distance == 0:
            return self.Billinghurst_penalty, walked_path

        stack = []
        stack.append(from_id)


        visited2 = []


        depth = 0
        depth_stack = []

        depth_stack.append(list())
        depth_stack[depth].append(from_id)



        self.__depth_first_search(from_id, 0, distance, to_id, walked_path)

        if distance > self.Billinghurst_penalty:
            distance = self.Billinghurst_penalty

        return distance, walked_path



        visited2 = []


        while len(stack) > 0:

            current_node = stack.pop()
            walked_path.append(current_node)

            visited2.append(current_node)

            if current_node == to_id:
                break

            childs =  self.weighted_graph[current_node].keys()

            childs_added = False

            if len(walked_path) < distance:
                for c in childs:
                    if c in visited2 or c in stack:
                        continue

                    if c in visited:
                        stack.append(c)
                        childs_added = True

            if childs_added == False:
                walked_path.pop()


        return distance, walked_path


    def __depth_first_search(self, node, depth, depth_limit, target, walked_path):


        walked_path.append(node)

        if node == target:
            return True

        if depth >= depth_limit-1:
            walked_path.pop()
            return False



        childs = self.weighted_graph[node].keys()

        for c in childs:
            if c not in walked_path:
                ret = self.__depth_first_search(c, depth + 1, depth_limit, target, walked_path)
                if ret == True:
                    return True

        walked_path.pop()

        return False


