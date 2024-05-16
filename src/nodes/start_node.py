from typing import List, Dict, Any, Optional, Union
import sys
sys.path.append("../../")
from src.nodes.base_node import BaseNode
import dearpygui.dearpygui as dpg

class StartNode(BaseNode):
    def __init__(self, parent: str|int, node_name: Optional[str|int] = None, node_tag: Optional[str|int] = None, **kwargs) -> None:
        super().__init__(parent, node_name, node_tag, **kwargs)

        self.create_node()

    def create_node(self) -> None:
        self.prompt_tag = self.add_attribute(label="start_attr", attribute_type=dpg.mvNode_Attr_Output)
        self.add_attr_value("run from here", label="start", parent=self.prompt_tag)

    def add_attr_value(self, default_value, label: str, parent: Optional[str|int]) -> None:
        dpg.add_text(default_value, label=label, parent=parent)

    def call_node(self, pre_node_attr_dict: Dict[int|str, list[int|str]], 
                  pre_node_list: List[BaseNode], 
                  other_paras: Optional[Dict] = None):
        if len(pre_node_attr_dict) !=0 or len(pre_node_list) != 0:
            print("StartNode has no precursor node")
            return
        
        self.run_state = True


def main():
    pass

if __name__ == "__main__":
    main()

