import networkx as nx # type: ignore
import matplotlib.pyplot as plt
import numpy as np
from networkx.algorithms import community



G = nx.DiGraph()

file_path = "sx-stackoverflow.txt"

with open(file_path, "r") as f:
    for i, line in enumerate(f):
        if i > 100000:  # on limite pour éviter surcharge
            break
        
        u, v, t = line.split()
        G.add_edge(int(u), int(v), timestamp=int(t))

print("Nombre de noeuds :", G.number_of_nodes())
print("Nombre de liens :", G.number_of_edges())



#1. Analyse de la distribution des degrés



# degrés des nœuds
degrees = [d for n, d in G.degree()]

# statistiques simples
print("Degré moyen :", np.mean(degrees))
print("Degré max :", np.max(degrees))
print("Degré min :", np.min(degrees))

plt.hist(degrees, bins=50)
plt.title("Distribution des degrés")
plt.xlabel("Degré")
plt.ylabel("Nombre de nœuds")
plt.show()


#2. Analyse des composantes connectées 

# composantes fortement connectées (graphe dirigé)
scc = list(nx.strongly_connected_components(G))
print("Nombre de composantes fortement connectées :", len(scc))

# plus grande composante
largest_scc = max(scc, key=len)
print("Taille de la plus grande composante :", len(largest_scc))





#3. Analyse des chemins


# diamètre (peut être lourd sur grand graphe → on utilise sous-graphe)
G_sub = G.subgraph(list(G.nodes())[:5000])

if nx.is_connected(G_sub.to_undirected()):
    print("Diamètre :", nx.diameter(G_sub.to_undirected()))
    print("Distance moyenne :", nx.average_shortest_path_length(G_sub.to_undirected()))
else:
    print("Le sous-graphe n'est pas connexe")



# 4. Clustering + densité

# clustering moyen
clustering = nx.average_clustering(G.to_undirected())
print("Clustering moyen :", clustering)

# densité
density = nx.density(G)
print("Densité du réseau :", density)



#5. Analyse de centralité


deg_cent = nx.degree_centrality(G)
top_deg = sorted(deg_cent.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top degré centralité :", top_deg)

pagerank = nx.pagerank(G)
top_pr = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top PageRank :", top_pr)


# top 10 degree centrality
deg_cent = nx.degree_centrality(G)
top_deg = sorted(deg_cent.items(), key=lambda x: x[1], reverse=True)[:10]

nodes = [str(n) for n, _ in top_deg]
values = [v for _, v in top_deg]

plt.figure(figsize=(10,6))
plt.bar(nodes, values)
plt.title("Top 10 des nœuds par Degree Centrality")
plt.xlabel("Nœuds")
plt.ylabel("Centralité")
plt.show()




#communities



G_sub = G.subgraph(list(G.nodes())[:5000]).copy() 
communities = community.louvain_communities(G_sub, seed=42) 
print("Nombre de communautés (Louvain):", len(communities))



#. Label Propagation


G_undirected = G_sub.to_undirected()

# Louvain
communities = community.louvain_communities(G_undirected, seed=42)






#graph

import networkx as nx
import matplotlib.pyplot as plt

# utiliser ton sous-graphe
G_vis = G_sub.to_undirected()


G_vis = G_vis.subgraph(list(G_vis.nodes())[:1000]).copy()
# Louvain communities
communities = list(nx.community.louvain_communities(G_vis, seed=42))

# créer un dictionnaire node -> communauté
node_color = {}
for i, comm in enumerate(communities):
    for node in comm:
        node_color[node] = i

# liste des couleurs pour chaque nœud
colors = [node_color.get(node, -1) for node in G_vis.nodes()]

# layout (important pour lisibilité)
pos = nx.spring_layout(G_vis, seed=42)

plt.figure(figsize=(12, 8))
nx.draw_networkx_nodes(G_vis, pos,
                       node_color=colors,
                       cmap=plt.cm.tab20,
                       node_size=20)

nx.draw_networkx_edges(G_vis, pos, alpha=0.1)

plt.title("Communautés détectées (Louvain)")
plt.axis("off")
plt.show()




# Label Propagation
lp_communities = list(community.label_propagation_communities(G_undirected))
print("Nombre de communautés (Label Propagation):", len(lp_communities))



G_lp = G_vis.copy()

lp_communities = list(nx.community.label_propagation_communities(G_lp))

node_color = {}
for i, comm in enumerate(lp_communities):
    for node in comm:
        node_color[node] = i

colors = [node_color.get(n, -1) for n in G_lp.nodes()]

pos = nx.spring_layout(G_lp, seed=42)

plt.figure(figsize=(10,7))
nx.draw_networkx_nodes(G_lp, pos, node_color=colors, cmap=plt.cm.tab20, node_size=20)
nx.draw_networkx_edges(G_lp, pos, alpha=0.1)

plt.title("Communautés - Label Propagation (44)")
plt.axis("off")
plt.show()




# K-Clique
kclique_communities = list(community.k_clique_communities(G_undirected, 4))
print("Nombre de communautés (K-Clique):", len(list(kclique_communities)))

G_k = G_vis.copy()

kc_communities = list(nx.community.k_clique_communities(G_k, 4))

node_color = {}
for i, comm in enumerate(kc_communities):
    for node in comm:
        node_color[node] = i

colors = [node_color.get(n, -1) for n in G_k.nodes()]

pos = nx.spring_layout(G_k, seed=42)

plt.figure(figsize=(10,7))
nx.draw_networkx_nodes(G_k, pos, node_color=colors, cmap=plt.cm.tab20, node_size=20)
nx.draw_networkx_edges(G_k, pos, alpha=0.1)

plt.title("Communautés - K-Clique (147)")
plt.axis("off")
plt.show()






