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


# on prend un petit sous-graphe pour visualisation
G_vis = G.subgraph(list(G.nodes())[:500]).to_undirected()

# layout
pos = nx.spring_layout(G_vis, seed=42)

plt.figure(figsize=(10,7))
nx.draw_networkx_nodes(G_vis, pos, node_size=20)
nx.draw_networkx_edges(G_vis, pos, alpha=0.1)

plt.title("Visualisation du réseau (sous-graphe)")
plt.axis("off")
plt.show()
#Construction du réseau

#Le réseau est construit à partir d’un fichier contenant des interactions entre utilisateurs.
#Chaque ligne représente une interaction entre deux utilisateurs avec un timestamp.
#Le graphe obtenu est orienté, où chaque nœud correspond à un utilisateur et chaque arête à une interaction.

#  On observe une structure fortement concentrée au centre,
#  où un grand nombre de nœuds sont densément connectés.
#  Cette zone centrale correspond aux utilisateurs les plus actifs et les plus connectés du réseau.

#  Autour de ce noyau, on distingue des nœuds plus isolés avec peu de connexions.
#  Ces nœuds périphériques représentent des utilisateurs ayant peu d’interactions.


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

#Interprétation de la distribution des degrés

#L’analyse de la distribution des degrés permet de comprendre comment les connexions 
#sont réparties entre les utilisateurs du réseau.

#L’écart très important entre le degré minimum et le degré maximum révèle une forte hétérogénéité dans le réseau.
#La majorité des utilisateurs possède peu de connexions, tandis qu’un petit nombre d’utilisateurs est extrêmement connecté.

#L’histogramme confirme cette observation en montrant une distribution asymétrique,
#où la majorité des nœuds se concentre sur de faibles valeurs, avec une longue traîne vers les valeurs élevées.

#le réseau présente une structure non uniforme dominée par quelques nœuds très influents.



#2. Analyse des composantes connectées 

# composantes fortement connectées (graphe dirigé)
scc = list(nx.strongly_connected_components(G))
print("Nombre de composantes fortement connectées :", len(scc))

# plus grande composante
largest_scc = max(scc, key=len)
print("Taille de la plus grande composante :", len(largest_scc))



#la présence d’une grande composante fortement connectée regroupant 5125 nœuds montre qu’une partie importante du réseau forme un noyau où les utilisateurs sont fortement interconnectés.

#Ainsi, le réseau présente une structure mixte composée :
#- d’un noyau principal dense et fortement connecté,
#- de nombreuses petites composantes isolées.



#3. Analyse des chemins


# diamètre (peut être lourd sur grand graphe → on utilise sous-graphe)
G_sub = G.subgraph(list(G.nodes())[:5000])

if nx.is_connected(G_sub.to_undirected()):
    print("Diamètre :", nx.diameter(G_sub.to_undirected()))
    print("Distance moyenne :", nx.average_shortest_path_length(G_sub.to_undirected()))
else:
    print("Le sous-graphe n'est pas connexe")




# L’analyse des chemins vise à étudier les distances entre les nœuds du réseau.
# Cependant, le sous-graphe analysé n’est pas connexe, ce qui signifie qu’il existe
# des nœuds ou des groupes de nœuds qui ne sont pas accessibles entre eux.

# Dans un graphe non connexe, il est impossible de calculer le diamètre global,
# car certaines paires de nœuds n’ont aucun chemin les reliant.





# 4. Clustering + densité

# clustering moyen
clustering = nx.average_clustering(G.to_undirected())
print("Clustering moyen :", clustering)

# densité
density = nx.density(G)
print("Densité du réseau :", density)


# Le coefficient de clustering moyen mesure la tendance des nœuds à former
# des triangles, c’est-à-dire des groupes où les voisins d’un nœud sont eux-mêmes connectés.

# La valeur obtenue (0.0319) est relativement faible, ce qui indique que
# les utilisateurs ne forment pas beaucoup de groupes fortement interconnectés.
# Autrement dit, les voisins d’un utilisateur ne sont pas souvent connectés entre eux.


# La densité du réseau (0.00067) est extrêmement faible, ce qui signifie que
# seule une très petite fraction des connexions possibles est réellement présente.

#5. Analyse de centralité


deg_cent = nx.degree_centrality(G)
top_deg = sorted(deg_cent.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top degré centralité :", top_deg)

pagerank = nx.pagerank(G)
top_pr = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top PageRank :", top_pr)

# Centralité de closeness
closeness = nx.closeness_centrality(G)
top_closeness = sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top Closeness :", top_closeness)

# Centralité de betweenness
#betweenness = nx.betweenness_centrality(G)
#top_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]
#print("Top Betweenness :", top_betweenness)

# Les nœuds avec une forte centralité de degré (ex: 3043, 572) sont les plus actifs et connectés.
# Le PageRank met en évidence les utilisateurs les plus influents, en tenant compte de la qualité des connexions.
# Certains nœuds apparaissent dans les deux classements, indiquant qu’ils sont à la fois actifs et influents.
# Cela confirme une structure où quelques utilisateurs clés dominent les interactions du réseau.

# Les nœuds avec une forte closeness (ex: 572, 1384652, 184) sont les plus proches de tous les autres dans le réseau.






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


#....................................................

# calcul PageRank
pagerank = nx.pagerank(G)

# top 10 PageRank
top_pr = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]

# préparation des données
nodes = [str(n) for n, _ in top_pr]
values = [v for _, v in top_pr]

# plot
plt.figure(figsize=(10,6))
plt.bar(nodes, values)
plt.title("Top 10 des nœuds par PageRank")
plt.xlabel("Nœuds")
plt.ylabel("PageRank")
plt.xticks(rotation=45)
plt.show()



#communities


# Louvain
G_sub = G.subgraph(list(G.nodes())[:5000]).copy() 
communities = community.louvain_communities(G_sub, seed=42) 
print("Nombre de communautés (Louvain):", len(communities))
G_undirected = G_sub.to_undirected()
communities = community.louvain_communities(G_undirected, seed=42)


#graph

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



# L’algorithme de Louvain détecte plusieurs communautés, indiquant que le réseau est structuré en groupes d’utilisateurs.
# Le graphe montre un noyau central dense où plusieurs communautés se chevauchent, traduisant des interactions communes entre sujets.
# Les petits groupes isolés autour représentent des communautés spécifiques ou peu actives.
# Cela confirme que Stack Overflow est organisé en sous-groupes thématiques avec un cœur fortement interconnecté.








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




# L’algorithme Label Propagation détecte un nombre limité de communautés (44), avec une grande communauté dominante.
# Le graphe montre que la majorité des nœuds appartient à un même groupe central très dense.
# Les petites communautés isolées représentent des groupes marginaux ou peu connectés.
# Cela suggère une structure moins fragmentée que Louvain, avec une forte dominance du noyau central.




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





# L’algorithme K-Clique détecte un grand nombre de petites communautés (147), basées sur des sous-groupes très denses.
# Ces communautés représentent des groupes fortement connectés (cliques), donc des interactions très proches.
# Le noyau central contient plusieurs cliques qui peuvent se chevaucher, montrant des relations complexes.
# Cela met en évidence des micro-communautés très soudées au sein du réseau.
