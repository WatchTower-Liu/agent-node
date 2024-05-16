from typing import List, Dict, Any, Optional, Union
import time
import sys
sys.path.append("../../")
from src.nodes.base_node import BaseNode
import dearpygui.dearpygui as dpg

class PrintNode(BaseNode):
    def __init__(self, parent: str|int, node_name: Optional[str|int] = None, node_tag: Optional[str|int] = None, **kwargs) -> None:
        super().__init__(parent, node_name, node_tag, **kwargs)

        self.create_node()

    def create_node(self) -> None:
        self.print_tag = self.add_attribute(label="print_attr", attribute_type=dpg.mvNode_Attr_Input)
        self.add_attr_value(label="print", parent=self.print_tag)

    def add_attr_value(self, label: str, parent: Optional[str|int]) -> None:
        self.show_tag = dpg.add_text(label=label, parent=parent)

    def wait_pre_node_finish(self, pre_node_list: List[BaseNode]):
        for pre_node in pre_node_list:
            while not pre_node.down_state:
                time.sleep(0.01)

    def call_node(self, pre_node_attr_dict: Dict[int|str, list[int|str]], 
                  pre_node_list: List[BaseNode], 
                  other_paras: Optional[Dict] = None):
        self.wait_pre_node_finish(pre_node_list)
        show_data = ""
        if self.print_tag in pre_node_attr_dict:
            all_data = self.get_prenode_value(pre_node_attr_dict[self.print_tag])
            for data in all_data.values():
                show_data += str(data) + "\n"

            stride = 30
            show_data = "\n".join([show_data[start:start+stride] for start in range(0, len(show_data), stride)])
            dpg.set_value(self.show_tag, show_data)


        self.run_state = True


def main():
    pass

if __name__ == "__main__":
    main()

