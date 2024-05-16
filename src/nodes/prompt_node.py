from typing import List, Dict, Any, Optional, Union
import sys
sys.path.append("../../")
from src.nodes.base_node import BaseNode
import dearpygui.dearpygui as dpg

class PromptNode(BaseNode):
    def __init__(self, parent: str|int, node_name: Optional[str|int] = None, node_tag: Optional[str|int] = None, **kwargs) -> None:
        super().__init__(parent, node_name, node_tag, **kwargs)

        self.create_node()

    def create_node(self) -> None:
        self.tital_tag = self.add_attribute(label="tital_attr", attribute_type=dpg.mvNode_Attr_Static)
        self.set_pin_name("", self.tital_tag, 300)
        self.prompt_tag = self.add_attribute(label="prompt_attr", attribute_type=dpg.mvNode_Attr_Output)
        self.add_attr_value(label="prompt", parent=self.prompt_tag, width=240)
        
    def add_attr_value(self, label: str, parent: Optional[str|int], width) -> None:
        dpg.add_input_text(label = label, parent=parent, width=width, multiline = True)

    def call_node(self, pre_node_attr_dict: Dict[int|str, list[int|str]], 
                  pre_node_list: List[BaseNode], 
                  other_paras: Optional[Dict] = None):
        if len(pre_node_attr_dict) !=0 or len(pre_node_list) != 0:
            print("PromptNode has no precursor node")
            return
        
        self.run_state = True


def main():
    pass

if __name__ == "__main__":
    main()

