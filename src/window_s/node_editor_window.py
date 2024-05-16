import dearpygui.dearpygui as dpg
from typing import Optional, List
import importlib
import sys
sys.path.append("../../")
from src.nodes.base_node import BaseNode

class NodeWindow():
    def __init__(self, window_width: int, window_height: int, window_pos: List[int], label="node_editor", node_base_module = "nodes.") -> None:
        self.window_width = window_width
        self.window_height = window_height
        self.window_pos = window_pos
        self.node_base_module = node_base_module

        self.edge_dict = {}
        self.node_list: List[BaseNode] = []

    def show_node_list(self):
        for node in self.node_list:
            print(node.node)
            print(node.node_name)
            print(node.input_attrs, node.output_attrs)
        print("==================")

    def convert_to_adjacency_list(self):
        adjacency_list = {}
        adjacency_list_reverse = {}
        for edge in self.edge_dict.values():
            if dpg.get_item_configuration(edge[0])["attribute_type"] == dpg.mvNode_Attr_Output:
                output_item = edge[0]
                input_item = edge[1]
            elif dpg.get_item_configuration(edge[0])["attribute_type"] == dpg.mvNode_Attr_Input:
                input_item = edge[0]
                output_item = edge[1]
            else:
                continue
            if output_item in adjacency_list:
                adjacency_list[output_item].append(input_item)
            else:
                adjacency_list[output_item] = [input_item]

            if input_item in adjacency_list_reverse:
                adjacency_list_reverse[input_item].append(output_item)
            else:
                adjacency_list_reverse[input_item] = [output_item]

        return adjacency_list, adjacency_list_reverse

    # callback runs when user attempts to connect attributes
    def link_callback(self, sender, app_data):
        # app_data -> (link_id1, link_id2)
        edge_tag = dpg.add_node_link(app_data[0], app_data[1], parent=sender)
        self.edge_dict[edge_tag] = app_data



    # callback runs when user attempts to disconnect attributes
    def delink_callback(self, sender, app_data):
        # app_data -> link_id
        self.edge_dict.pop(app_data)
        dpg.delete_item(app_data)

    def set_node(self, 
                 node_file: str,
                 node_name: str, 
                 parent: Optional[str|int] = None, 
                 node_tag: Optional[str|int] = None, **kwargs) -> None:
        if not hasattr(importlib.import_module(self.node_base_module+node_file), node_name):
            raise ValueError("node name not exist")
        else:
            node_cls = getattr(importlib.import_module(self.node_base_module+node_file), node_name)
            node = node_cls(parent, node_name, node_tag, **kwargs)
            self.node_list.append(node)
            return node.node

    def set_node_editor(self, label="node_editor") -> str:
        self.node_window_tag = dpg.add_window(label=label, width=self.window_width, height=self.window_height, pos=self.window_pos, no_move=False, no_close=True)
        node_editor_tag = dpg.add_node_editor(label="node_editor", 
                        callback=self.link_callback, 
                        delink_callback=self.delink_callback, 
                        parent=self.node_window_tag,
                        minimap=True,
                        minimap_location=dpg.mvNodeMiniMap_Location_BottomRight)
        
        return node_editor_tag
            