# -*- coding: utf-8 -*-
"""
Sankey Diagram
"""
import copy
import json
import os
import random
from os.path import abspath

from backend import action_list


LINK_BOLD = 20


def gen_path(action_list):
    result = []
    for path_len in xrange(1, len(action_list)):
        actions_copy = copy.deepcopy(action_list)
        path = []
        for i in xrange(path_len):
            seed = random.randrange(path_len - i)
            node = actions_copy.pop(seed)
            path.append(node)
        result.append(path)
    return result


def gen_path1(action_list):
    result = []
    actions_copy = copy.deepcopy(action_list)
    while actions_copy:
        node_count = random.randrange(start=1, stop=len(actions_copy), step=1) if len(actions_copy) > 1 else 1
        path = []
        for i in xrange(node_count):
            seed = random.randrange(len(actions_copy) - 1) if len(actions_copy) > 1 else 0
            path.append(actions_copy.pop(seed))
        result.append(path)
    print result
    return result


def gen_path_value(path_list):
    path_value_list = []
    for path in path_list:
        single_path = []
        for i in xrange(len(path) - 1):
            seed = random.randrange(LINK_BOLD)
            single_path.append(seed)
        path_value_list.append(single_path)
    return path_value_list


def gen_json_file(path_list, path_value_list):
    nodes = []
    for action in action_list.action:
        node = {"name": action}
        nodes.append(node)

    links = []
    for index, path in enumerate(path_list):
        for i in xrange(len(path) - 1):
            source = action_list.action.index(path[i])
            target = action_list.action.index(path[i+1])
            link = {"source": source, "target": target, "value": path_value_list[index][i]}
            links.append(link)
    temp = {"nodes": nodes,
            "links": links}

    root = os.path.dirname(os.path.dirname(abspath(__file__)))
    with open(os.path.join(root, 'mock_data.json'), 'w') as fp:
        fp.write(json.dumps(temp))


def simulate():
    path_list = gen_path1(action_list.action)
    path_value_list = gen_path_value(path_list)
    gen_json_file(path_list, path_value_list)


if __name__ == "__main__":
    simulate()
