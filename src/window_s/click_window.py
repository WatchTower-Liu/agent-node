import dearpygui.dearpygui as dpg
from src.window_s.node_editor_window import NodeWindow

from src.nodes.base_node import BaseNode

class NodeRightClickWindow():
    def __init__(self, window_width: int, window_height: int, node_window: NodeWindow) -> None:
        self.window_width = window_width
        self.window_height = window_height

        self.node_window = node_window
        self.right_click_window = -1

        with dpg.handler_registry():
            dpg.add_mouse_click_handler(callback=self.click_item)

    def click_item(self, sender, app_data):
        for node in self.node_window.node_list:
            if dpg.is_item_right_clicked(node.node):
                self.set_node_right_click_window(node)

    def set_node_right_click_window(self, node: BaseNode):
        if self.right_click_window != -1:
            dpg.delete_item(self.right_click_window)
        self.right_click_window = dpg.add_window(width=self.window_width, height=self.window_height, 
                                                pos=dpg.get_item_state(node.node)["rect_min"])

        dpg.add_button(label="Delete", parent=self.right_click_window, 
                       callback=lambda: self.delete_node(node, self.right_click_window))

    def delete_node(self, node: BaseNode, right_click_window: str|int):
        all_children = dpg.get_item_children(node.node)
        for child in all_children.values():
            for child_item in child:
                dpg.delete_item(child_item)

        dpg.delete_item(node.node)
        self.node_window.node_list.remove(node)
        for input_attr in node.input_attrs.keys():
            edge_keys = list(self.node_window.edge_dict.keys())
            for edge_key in edge_keys:
                if input_attr in self.node_window.edge_dict[edge_key]:
                    self.node_window.edge_dict.pop(edge_key)
                    dpg.delete_item(edge_key)

        for output_attr in node.output_attrs.keys():
            edge_keys = list(self.node_window.edge_dict.keys())
            for edge_key in edge_keys:
                if output_attr in self.node_window.edge_dict[edge_key]:
                    self.node_window.edge_dict.pop(edge_key)
                    dpg.delete_item(edge_key)

        del node
        dpg.delete_item(right_click_window)
        self.right_click_window = -1

from src.nodes.node_list import node_file, node_class
from copy import deepcopy


class NodeEditorWindowRightClickWindow():
    def __init__(self, window_width: int, window_height: int, node_editor_tag: str|int, node_window: NodeWindow) -> None:
        self.window_width = window_width
        self.window_height = window_height

        self.node_editor_tag = node_editor_tag
        self.node_window = node_window
        self.right_click_window = -1

        with dpg.handler_registry():
            dpg.add_mouse_click_handler(callback=self.click_item)
 

    def click_item(self, sender, app_data):
        for node in self.node_window.node_list:
            if dpg.is_item_right_clicked(node.node):
                return 
            
        if dpg.is_item_hovered(self.node_editor_tag) and app_data==dpg.mvMouseButton_Right:
            
            self.set_right_click_window()
                
    def create_call_back(self, node_file, node_name, func, node_editor_tag):
        node_file = deepcopy(node_file)
        node_name = deepcopy(node_name)
        func = func
        node_editor_tag = node_editor_tag

        def call():
            node_tag = func(node_file, node_name, parent=node_editor_tag)
            dpg.delete_item(self.right_click_window)
            self.right_click_window = -1

        return call
    
    def node_create_tree(self, bar_tag):
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
        for tree_bar_name in node_select_data.keys():
            # tab_bar_tag = dpg.add_tab_bar(parent=self.right_click_window)
            # bar_tag = dpg.add_tab(label=tree_bar_name, parent=tab_bar_tag)
            tree_node_tag = dpg.add_tree_node(label=tree_bar_name, parent=bar_tag)
            for group_node_name in node_select_data[tree_bar_name]:
                for node_name in group_node_name[1]:
                    create_button_list.append(dpg.add_button(label=f"Create {node_name}", parent=tree_node_tag, 
                                callback=self.create_call_back(group_node_name[0], node_name, self.node_window.set_node, self.node_editor_tag)))

    def set_right_click_window(self):
        if self.right_click_window != -1:
            dpg.delete_item(self.right_click_window)

        self.right_click_window = dpg.add_window(popup=True, label="node_editor_right_click_window", width=self.window_width, height=self.window_height)
        tab_bar_tag = dpg.add_tab_bar(parent=self.right_click_window)
        bar_tag = dpg.add_tab(label="node management",parent=tab_bar_tag)
        tree_node_tag = dpg.add_tree_node(label="create node", parent=bar_tag)
        self.node_create_tree(tree_node_tag)
                
        

