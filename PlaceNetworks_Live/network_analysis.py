import networkx as nx
import csv
import pylab as plt


### LOAD NETWORK FROM FILE ###
nyc_net = nx.read_edgelist(
    'newyork_net.txt', create_using=nx.DiGraph(), nodetype=int)

### READ FOURSQUARE VENUES DATA ###
node_data = {}
with open('venue_data_4sq_newyork_anon.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        latit = float(row['latitude'])
        longit = float(row['longitude'])
        place_title = row['title']
        node_id = int(row['vid'])
        node_data[node_id] = (place_title, latit, longit)


# some simple stats
N, K = nyc_net.order(), nyc_net.size()
avg_deg = float(K) / N

print("Loaded New York City Place network.")
print("Nodes: %d" % N)
print("Edges: %d" % K)
print("Average degree: %f" % avg_deg)

# Get degree distributions (in- and out-)
in_degrees = nyc_net.in_degree()
in_values = sorted(set(in_degrees.values()))
in_hist = [list(in_degrees.values()).count(x) for x in in_values]

out_degrees = nyc_net.out_degree()
out_values = sorted(set(out_degrees.values()))
out_hist = [list(out_degrees.values()).count(x) for x in out_values]


# plot degree distributions
logScale = True  # set this True to plot data in logarithmic scale
plt.figure()
if logScale:
    plt.loglog(in_values, in_hist, 'ro-')  # red color with marker 'o'
    plt.loglog(out_values, out_hist, 'bv-')  # blue color with marker 'v'
else:
    plt.plot(in_values, in_hist, 'ro-')  # red color with marker 'o'
    plt.plot(out_values, out_hist, 'bv-')  # blue color with marker 'v'
plt.legend(['In-degree', 'Out-degree'])
plt.xlabel('Degree')
plt.ylabel('Number of nodes')
plt.title('network of places in new york')
plt.grid(True)
if logScale:
    plt.xlim([0, 2 * 10**2])
    plt.savefig('nyc_net_degree_distribution_loglog.pdf')
else:
    plt.savefig('nyc_net_degree_distribution.pdf')
plt.close()


# draw the graph using information about nodes geographic positions
pos_dict = {}
for node_id, node_info in node_data.items():
    pos_dict[node_id] = (node_info[2], node_info[1])
nx.draw(nyc_net, pos=pos_dict, with_labels=False, node_size=20)
plt.savefig('nyc_net_graph.png')
plt.close()


# Symmetrize the graph for simplcity
nyc_net_ud = nyc_net.to_undirected()

# We are interested in the largest connected component
nyc_net_components = nx.connected_component_subgraphs(nyc_net_ud)
nyc_net_mc = next(nyc_net_components)

# Graph statistics for the main component
N_mc, K_mc = nyc_net_mc.order(), nyc_net_mc.size()
avg_deg_mc = float(2 * K_mc) / N_mc
avg_clust = nx.average_clustering(nyc_net_mc)

print("")
print("New York Place Network graph main component.")
print("Nodes: %d" % N_mc)
print("Edges: %d" % K_mc)

print("Average degree: %f" % avg_deg_mc)
print("Average clustering coefficient: %f" % avg_clust)


# Betweenness centrality
bet_cen = nx.betweenness_centrality(nyc_net_mc)
# Degree centrality
deg_cen = nx.degree_centrality(nyc_net_mc)
# Eigenvector centrality
eig_cen = nx.eigenvector_centrality(nyc_net_mc)


# utility function: get top keys from a python dictionary.
# Input is a dictionary and number specifies the top-K elements to be
# returned. Return value is a list of tuples [(keyA, valueA)....(keyZ,
# valueZ)]
def getTopDictionaryKeys(dictionary, number):
    topList = []
    a = dict(dictionary)
    for i in range(0, number):
        m = max(a, key=a.get)
        topList.append([m, a[m]])
        del a[m]

    return topList


top_bet_cen = getTopDictionaryKeys(bet_cen, 10)

top_deg_cen = getTopDictionaryKeys(deg_cen, 10)

top_eig_cent = getTopDictionaryKeys(eig_cen, 10)


print('Top-10 places for betweenness centrality.')
for [node_id, value] in top_bet_cen:
    title = node_data[node_id][0]
    print(title)
print('------')

print('Top-10 places for degree centrality.')
for [node_id, value] in top_deg_cen:
    title = node_data[node_id][0]
    print(title)
print('------')

print('Top-10 places for eigenvector centrality.')
for [node_id, value] in top_eig_cent:
    title = node_data[node_id][0]
    print(title)
print('------')
