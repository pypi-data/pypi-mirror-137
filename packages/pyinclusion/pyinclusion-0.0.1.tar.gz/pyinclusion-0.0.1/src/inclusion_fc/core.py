from pyflowchart import *
import numpy as np
import pandas as pd
"""
The construction of the flowchart diagram occurs in three steps
1. We will compute the stats of subject remaining and excluded subjects
2. We will construct the nodes
3. The nodes will be connected
4. Post-hoc adjustment

"""

# 1. Compute the stats
# default ordering is not specified
def filter_df(my_df, label_orders=None):
    # all the labels should be part of my_df
    remove_counts = []
    current_counts = [len(my_df)]

    current_columns = my_df.columns.tolist()
    # check PID exists
    assert 'pid' in current_columns

    # check all the specified label exists
    if label_orders is not None:
        for my_label in label_orders:
            assert my_label in current_columns
    else:
        current_columns.remove('pid')
        label_orders = current_columns

    for my_label in label_orders:
        my_count = np.sum(my_df[my_label] == True)
        my_remove = np.sum(my_df[my_label] == False)
        current_counts.append(my_count)
        remove_counts.append(my_remove)
        my_df = my_df[my_df[my_label] == True]
    return my_df, current_counts, remove_counts, label_orders


def get_node_name(node_text, n, node_type='start', exclude_reason=''):
    # node_type = ['start', 'end', 'condition', exclude']
    deafult_str = {
        'start': "All subjects",
        'end': "Subjects included",
        'condition':  "Fulfilled condtions",
        'exclude': "Excluded due to "
    }
    if len(node_text) == 0:
        node_text = deafult_str[node_type] + exclude_reason

    node_text = (node_text + "\n n=%d" % n)
    return node_text


def generate_nodes(current_counts, remove_counts, label_orders, start_node_text="",
                   end_node_text="", condition_text=[], exclusion_text=[]):
    assert len(condition_text) == len(exclusion_text)

    start_node_text = get_node_name(start_node_text, current_counts[0], node_type='start')
    end_node_text = get_node_name(end_node_text, current_counts[-1], node_type='end')

    start_node = StartNode(start_node_text)
    start_node.node_text = start_node_text
    end_node = EndNode(end_node_text)
    end_node.node_text = end_node_text  # to get rid of the default start and end

    # Get condition nodes
    cond_nodes = []
    removed_nodes = []
    for i in range(len(label_orders)):
        to_remove_num = remove_counts[i]
        current_num = current_counts[i]

        my_condition_text = condition_text[i] if len(condition_text) > 0 else ""
        my_exclude_text = exclusion_text[i] if len(condition_text) > 0 else ""

        my_condition_text = get_node_name(my_condition_text, current_num, node_type='condition')
        my_exclude_text = get_node_name(my_exclude_text, to_remove_num,
                                        node_type='exclude', exclude_reason=label_orders[i])

        cond_nodes.append(ConditionNode(my_condition_text))
        removed_nodes.append(OperationNode(my_exclude_text))

    cond_nodes.append(end_node)
    return start_node, cond_nodes, removed_nodes


def connect_nodes(start_node, cond_nodes, removed_nodes):
    start_node.connect(cond_nodes[0])
    for i in range(len(cond_nodes) - 1):
        cond_nodes[i].connect_yes(cond_nodes[i + 1])
        cond_nodes[i].connect_no(removed_nodes[i])

    fc = Flowchart(start_node)
    print(fc.flowchart())
    return fc.flowchart()


def gen_graph(my_df, label_orders=None, **kwargs):
    """
    start_node_text (str)
    end_node_text (str)
    condition_text (str list)
    exclusion_text (str list)
    """
    my_df, current_counts, remove_counts, label_orders = filter_df(my_df, label_orders=label_orders)
    start_node, cond_nodes, removed_nodes = generate_nodes(current_counts, remove_counts, label_orders, **kwargs)
    return connect_nodes(start_node, cond_nodes, removed_nodes)
