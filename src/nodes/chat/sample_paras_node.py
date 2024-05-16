from typing import List, Dict, Any, Optional, Union
import sys
sys.path.append("../../")
from src.nodes.base_node import BaseNode
import dearpygui.dearpygui as dpg

class SampleParasNode(BaseNode):
    def __init__(self, parent: str|int, node_name: Optional[str|int] = None, node_tag: Optional[str|int] = None, **kwargs) -> None:
        super().__init__(parent, node_name, node_tag, **kwargs)

        self.create_node()

    def create_node(self) -> None:
        self.prompt_tag = self.add_attribute(label="sample_paras_attr", attribute_type=dpg.mvNode_Attr_Output)
        self.add_attr_value([1, 1000, 1], label=["temperature", "top_k", "top_p"], parent=self.prompt_tag)

    def add_attr_value(self, default_value: Optional[Any] = None, label: List[str] = None, parent: Optional[str|int] = None, width: int = 300) -> None:
        dpg.add_slider_float(label=label[0], parent=parent, default_value=default_value[0], min_value=0, max_value=1, width=width)  # temperature
        dpg.add_slider_int(label=label[1], parent=parent, default_value=default_value[1], min_value=0, max_value=1000, width=width)  # top_k
        dpg.add_slider_float(label=label[2], parent=parent, default_value=default_value[2], min_value=0, max_value=1, width=width)  # top_p
        

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

