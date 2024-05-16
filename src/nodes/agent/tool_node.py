from typing import List, Optional, Dict, Any, Union
import dearpygui.dearpygui as dpg
import sys
sys.path.append("../../")

from src.nodes.base_node import BaseNode


class ToolNode(BaseNode):
    def __init__(self, parent: str|int, node_name: Optional[str|int] = None, node_tag: Optional[str|int] = None, **kwargs) -> None:
        super().__init__(parent, node_name, node_tag, **kwargs)

        self.create_node()

    def create_node(self) -> None:
        self.prompt_tag = self.add_attribute(label="tool_attr", attribute_type=dpg.mvNode_Attr_Output)
        self.add_attr_value(label="tool_name", parent=self.prompt_tag, width=300)
        self.add_attr_value(label="call_func/url", parent=self.prompt_tag, width=300)
        self.add_attr_value(label="tool_description", parent=self.prompt_tag, width=300)
        self.add_attr_value(label="tool_parameter", parent=self.prompt_tag, width=300)


    def add_attr_value(self, label: str, parent: Optional[str|int], width) -> None:
        dpg.add_input_text(label=label, parent=parent, width=width, multiline = False)

    def call_node(self, pre_node_attr_dict: Dict[int|str, list[int|str]], 
                  pre_node_list: List[BaseNode], 
                  other_paras: Optional[Dict] = None):
        if len(pre_node_attr_dict) !=0 or len(pre_node_list) != 0:
            print("ToolNode has no precursor node")
            return
        
        self.run_state = True