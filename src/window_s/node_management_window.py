from typing import List, Optional, Dict
from copy import deepcopy

import dearpygui.dearpygui as dpg
from src.window_s.node_editor_window import NodeWindow
from src.runner.node_runner import NodeRunner
from src.nodes.node_list import node_file, node_class
from src.utils.utils import help

def create_call_back(node_file, node_name, func, node_editor_tag):
    node_file = deepcopy(node_file)
    node_name = deepcopy(node_name)
    func = func
    node_editor_tag = node_editor_tag

    def call():
        func(node_file, node_name, parent=node_editor_tag)

    return call

class NodeManagementWindow():
    def __init__(self, window_width: int, 
                 window_height: int, 
                 window_pos: List[int],
                 node_editor_tag: str|int, 
                 node_window:NodeWindow,
                 node_runner_config: Dict) -> None:
        self.window_width = window_width
        self.window_height = window_height
        self.window_pos = window_pos
        self.node_editor_tag = node_editor_tag

        self.node_window = node_window
        self.node_runner_config = node_runner_config
    
    def run_node(self):
        adjacency_list, adjacency_list_reverse = self.node_window.convert_to_adjacency_list()
        print(self.node_window.edge_dict)
        node_runner = NodeRunner(self.node_window.node_list, 
                                      adjacency_list, 
                                      adjacency_list_reverse, 
                                      self.node_runner_config)
        node_runner.run()
        print("finished running")

    def reset_run_state(self):
        for node in self.node_window.node_list:
            node.run_state = False

    def finish_all_node(self):
        for node in self.node_window.node_list:
            node.run_state = True

    def set_node_management(self, label="node_management") -> str:
        node_management_window_tag = dpg.add_window(label=label, width=self.window_width, height=self.window_height, pos=self.window_pos, no_close=True)

        node_create_group = dpg.add_child_window(label="node create", parent=node_management_window_tag, height=300)
        node_select_data = {}
        for node_f, node_name_list in zip(node_file, node_class):
            split_node_file = node_f.split(".")
            if len(split_node_file) > 1:
                base_name = "/".join(split_node_file[:-1])
                if base_name not in node_select_data:
                    node_select_data[base_name] = [[node_f, node_name_list]]
                else:
                    node_select_data[base_name].append([node_f, node_name_list])
            else:
                if "norm" not in node_select_data:
                    node_select_data["norm"] = [[node_f, node_name_list]]
                else:
                    node_select_data["norm"].append([node_f, node_name_list])

        create_button_list = []
        tab_bar_tag = dpg.add_tab_bar(parent=node_create_group)
        for tree_bar_name in node_select_data.keys():
            bar_tag = dpg.add_tab(label=tree_bar_name, parent=tab_bar_tag)
            tree_node_tag = dpg.add_tree_node(label=tree_bar_name, parent=bar_tag)
            for group_node_name in node_select_data[tree_bar_name]:
                for node_name in group_node_name[1]:
                    create_button_list.append(dpg.add_button(label=f"Create {node_name}", parent=tree_node_tag, 
                                callback=create_call_back(group_node_name[0], node_name, self.node_window.set_node, self.node_editor_tag)))

        # promptNode_create_button = dpg.add_button(label="Create Prompt Node", parent=node_create_group, 
        #                                           callback=lambda: self.node_window.set_node("PromptNode", parent=self.node_editor_tag))
        # chat_model_create_button = dpg.add_button(label="Create OpenAI Chat Node", parent=node_create_group, 
        #                                           callback=lambda: self.node_window.set_node("OpenAI_chat_Node", parent=self.node_editor_tag))
        # start_node_button = dpg.add_button(label="Create Start Node", parent=node_create_group, 
        #                                    callback=lambda:self.node_window.set_node("StartNode", parent=self.node_editor_tag))
        # print_node_button = dpg.add_button(label="Create Print Node", parent=node_create_group, 
        #                                    callback=lambda:self.node_window.set_node("PrintNode", parent=self.node_editor_tag))
        
        node_run_group = dpg.add_child_window(label="node run", parent=node_management_window_tag, height=150)
        run_button = dpg.add_button(label="Run", parent=node_run_group, callback=self.run_node)
        reset_button = dpg.add_button(label="Reset", parent=node_run_group, callback=self.reset_run_state)
        help("Rest all node run flags", node_run_group)
        finish_button = dpg.add_button(label="Finish All", parent=node_run_group, callback=self.finish_all_node)
        help("Sets all run flags to force an end to the process", node_run_group)

        
        
            