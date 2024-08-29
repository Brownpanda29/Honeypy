import pandas as pd
import matplotlib.pyplot as plt
import requests
from ipaddress import ip_address
from user_agents import parse

# Load honeypot logs
logs = pd.read_csv('honeypot_logs.csv')

# Initial analysis
ip_addresses = logs['ip_address']
user_agents = logs['user_agent']

# Graph-based analysis
graph = nx.Graph()
for index, row in logs.iterrows():
    graph.add_node(row['command'], type='command')
    graph.add_node(row['ip_address'], type='ip_address')
    graph.add_edge(row['command'], row['ip_address'])

# Community detection
communities = nx.algorithms.community.greedy_modularity_communities(graph)
community_labels = {node: community for community, nodes in enumerate(communities) for node in nodes}

# Centrality measures
centrality = nx.algorithms.centrality.degree_centrality(graph)

# Threat intelligence feed integration
misp_api = 'https://misp.example.com/api/v2/events'
response = requests.get(misp_api, headers={'Authorization': 'Bearer YOUR_API_KEY'})
misp_data = response.json()

# Correlate with honeypot logs
matches = []
for event in misp_data['events']:
    for attribute in event['attributes']:
        if attribute['type'] == 'ip-src' and attribute['value'] in ip_addresses:
            matches.append((attribute['value'], event['info']))

# Visualization and reporting
plt.figure(figsize=(10, 6))
nx.draw(graph, pos=nx.spring_layout(graph), node_color='lightblue', node_size=5000, with_labels=True)
plt.title('Hacker Behavior Graph')
plt.show()

print('Matches with threat intelligence feeds:')
for match in matches:
    print(f'IP address: {match[0]}, Event info: {match[1]}')
