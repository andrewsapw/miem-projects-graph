from pyvis.network import Network
import streamlit.components.v1 as components
import cabinet
import itertools
from collections import defaultdict, Counter
import networkx as nx


def test_graph() -> Network:
    g = Network(height="500px", width="500px", heading="")
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(1, 3)
    return g


def reformat_fullname(fullname: str) -> str:
    fullname = fullname.split()
    name = f"{fullname[0]} {fullname[1][0]}.{fullname[2][0]}"
    return name


def flatten(t):
    return [item for sublist in t for item in sublist]


def make_graph():
    data = cabinet.get_projects()

    project_members = []
    for project in data:
        head = project["head"]
        direction_head = project["directionHead"]
        team = project["team"]
        team = [i.strip() for i in team]

        if len(head.split()) == 3:
            head = reformat_fullname(head)

        if len(direction_head.split()) == 3:
            direction_head = reformat_fullname(direction_head)

        members = team + [head] + [direction_head]
        members = set([i for i in members if i])
        project_members.append(members)

    all_members = flatten(project_members)
    unique_members = set(all_members)

    g = Network(height="1000px", width="1000px", heading="")

    nodes = {}
    nodes_sizes = Counter(all_members)

    edges = {}

    for idx, name in enumerate(unique_members):
        nodes[name] = idx
        size = nodes_sizes[name] * 10
        g.add_node(idx, label=name, value=size)

    for pm in project_members:
        for n1, n2 in itertools.combinations(pm, r=2):
            edge = tuple(sorted([n1, n2]))

            if edge in edges:
                edges[edge] += 10
            else:
                edges[edge] = 1

            value = edges[edge]
            print(value, edge)
            g.add_edge(nodes[n1], nodes[n2], value=value)

    return g


def make_graph_nx():
    data = cabinet.get_projects()

    nx_graph = nx.Graph()
    project_members = []
    for project in data:
        head = project["head"]
        direction_head = project["directionHead"]
        team = project["team"]
        team = [i.strip() for i in team]

        if len(head.split()) == 3:
            head = reformat_fullname(head)

        if len(direction_head.split()) == 3:
            direction_head = reformat_fullname(direction_head)

        members = team + [head] + [direction_head]
        members = set([i for i in members if i])
        project_members.append(members)

    all_members = flatten(project_members)
    unique_members = set(all_members)

    nodes = {}
    nodes_sizes = Counter(all_members)

    edges = {}

    for idx, name in enumerate(unique_members):
        nodes[name] = idx
        size = nodes_sizes[name] * 10

    for p_idx, pm in enumerate(project_members):
        for name in pm:
            nx_graph.add_node(
                nodes[name], size=nodes_sizes[name], label=name, group=p_idx
            )

    for pm in project_members:
        for n1, n2 in itertools.combinations(pm, r=2):
            edge = tuple(sorted([n1, n2]))

            if edge in edges:
                edges[edge] += 10
            else:
                edges[edge] = 1

            value = edges[edge]
            nx_graph.add_edge(nodes[n1], nodes[n2], value=value)

    g = Network(height="1000px", width="1000px", heading="")
    g.from_nx(nx_graph)

    return g


def show_graph(return_streamlit=False) -> components.html:
    g = make_graph_nx()
    h1 = g.height
    h1 = int(h1.replace("px", ""))
    w1 = g.width
    w1 = int(w1.replace("px", ""))

    g.save_graph("index.html")

    if return_streamlit:
        return components.html(g.html, height=h1, width=w1)
    else:
        return g


if __name__ == "__main__":
    # make_graph()
    show_graph()
