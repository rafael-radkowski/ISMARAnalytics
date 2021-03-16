import matplotlib.pyplot as plt

import networkx as nx


class DataPlot:




    def __init__(self):

        pass


    @staticmethod
    def plotFrequency( x, y, labels, title, axis, file):


        fig = plt.figure()
        ax1 = fig.add_subplot(111)

        color = ['r', 'g', 'b', 'y', 'c', 'm']
        cidx = 0

        for yy in y:
            ax1.plot(x, yy,  c=color[cidx], linestyle='dashed', marker="o", linewidth=1, label=labels[cidx])
            #ax1.scatter(x, yy, s=10, linewidth=2, c=color[cidx], marker="o", label=labels[cidx])
            cidx = cidx + 1

        #ax1.scatter(x[40:], y[40:], s=10, c='r', marker="o", label='second')

        plt.title(title)
        plt.xlabel(axis[0])
        plt.ylabel(axis[1])
        plt.xticks(rotation=90)
        plt.legend(loc='upper left')

        plt.savefig(file)
        plt.show()


    @staticmethod
    def plotStack(x, y, labels, title, axis, file):



        fig, ax = plt.subplots()
        ax.stackplot(x, y, labels=labels)


        ax.legend(loc='upper left')
        plt.title(title)
        plt.xlabel(axis[0])
        plt.ylabel(axis[1])
        plt.xticks(rotation=90)

        plt.savefig(file)
        plt.show()


    @staticmethod
    def plotStackNormalized(x, y, labels, title, axis, file):

        for i in range(len(x)):

            sum_per_year = 0
            for j in range(len(labels)):
                sum_per_year = sum_per_year + y[j][i]

            for j in range(len(labels)):
                y[j][i] = y[j][i] / sum_per_year




        fig, ax = plt.subplots()
        ax.stackplot(x, y, labels=labels)

        ax.legend(loc='upper left')
        plt.title(title)
        plt.xlabel(axis[0])
        plt.ylabel(axis[1])
        plt.xticks(rotation=90)

        plt.savefig(file)
        plt.show()


    @staticmethod
    def plotGraph( weighted_edges):


        G = nx.Graph()


        for node in weighted_edges.keys():

            for edge in weighted_edges[node].keys():


                value = weighted_edges[node][edge]

                G.add_edge(str(node), str(edge), weight=value)


        elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 1.0]
        esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 1.0]

        pos = nx.spring_layout(G, k=0.1, scale=5, dim=2)  # positions for all nodes

        # nodes
        nx.draw_networkx_nodes(G,  pos, node_size=60)

        # edges

        nx.draw_networkx_edges(G, pos, edgelist=elarge, width=1, edge_color="b")
        nx.draw_networkx_edges(G, pos, edgelist=esmall, width=1, style="dashed")

      #  nx.draw_networkx_edges(G, pos, edgelist=elarge, width=2)
       # nx.draw_networkx_edges(
       #     G, pos, edgelist=esmall, width=2, alpha=0.5, edge_color="b", style="dashed"
       # )

        # labels
        nx.draw_networkx_labels(G, pos, font_size=6, font_family="sans-serif")

        plt.axis("off")
        plt.show()