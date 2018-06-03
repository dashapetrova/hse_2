import sys
import gensim, logging
import networkx as nx
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

m = 'ruscorpora_upos_skipgram_300_10_2017.bin.gz'
model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
model.init_sims(replace=True)

words = ['кошка_NOUN','собака_NOUN','тигр_NOUN','хищник_NOUN','волк_NOUN','динго_NOUN','мышь_NOUN','млекопитающее_NOUN','животное_NOUN']

G = nx.Graph()
  
for i in words:
    G.add_node(i[:-5])
    for j in words:
        if model.similarity(i,j)>0.5:
            G.add_edge(i[:-5], j[:-5]) 

pos=nx.spring_layout(G)

nx.draw_networkx_nodes(G, pos, node_color='green', node_size=50)
nx.draw_networkx_edges(G, pos, edge_color='yellow')
nx.draw_networkx_labels(G, pos, font_size=15, font_family='Arial')
plt.axis('off') 
plt.show()

mc = []
deg = nx.degree_centrality(G)
for nodeid in sorted(deg, key=deg.get, reverse=True):
    mc.append(nodeid)
s = mc[0] + ', ' + mc[1] + ', ' + mc[2]
print("Три самых центральных слова:",s)
print("Радиус графа = ",nx.radius(G))
print("Коэффициент кластеризации = ",nx.average_clustering(G))
