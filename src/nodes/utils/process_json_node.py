from typing import List, Dict, Any, Optional, Union
import time
import json
import sys
sys.path.append("../../")
from src.nodes.base_node import BaseNode
import dearpygui.dearpygui as dpg

class ProcessJsonNode(BaseNode):
    def __init__(self, parent: str|int, node_name: Optional[str|int]  = None, node_tag: Optional[str|int] = None, **kwargs) -> None:
        super().__init__(parent, node_name, node_tag, **kwargs)

        self.create_node()

    def create_node(self) -> None:
        self.result_tag = self.add_attribute(label="result_attr", attribute_type=dpg.mvNode_Attr_Output)
        self.set_pin_name("result", self.result_tag, 300)
        self.result_value_tag = dpg.add_text(label="result", parent=self.result_tag, show=False)
        
        self.input_text_tag = self.add_attribute(label="input_text_attr", attribute_type=dpg.mvNode_Attr_Input)
        self.set_pin_name("input_text", self.input_text_tag)

        self.extra_key_tag = self.add_attribute(label="extra_key_attr", attribute_type=dpg.mvNode_Attr_Static)
        self.show_keys = dpg.add_text(parent=self.extra_key_tag, color=[0, 200, 200])
        dpg.add_text("Use '|' to separate different keys and\nignore keys when they don't exist", parent=self.extra_key_tag, color=[200, 200, 0])
        self.key_list_text = dpg.add_input_text(label="key_list_text", multiline=True, parent=self.extra_key_tag, width=240)

    def add_attr_value(self, label: str, parent: Optional[str|int], width, multi_line: bool = False, default_value:str="") -> None:
        dpg.add_input_text(label=label, parent=parent, width=width, multiline=multi_line, default_value=default_value)

    def wait_pre_node_finish(self, pre_node_list: List[BaseNode]):
        for pre_node in pre_node_list:
            while not pre_node.down_state:
                time.sleep(0.01)

    def flatten_json(self, json_obj:Dict, parent_key:str='', sep:str=' '):
        items = {}

        def recurse(obj, parent_key):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    new_key = f"{parent_key}_{k}" if parent_key else k
                    recurse(v, new_key)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    recurse(item, parent_key)
            elif isinstance(obj, str):

                try:
                    convert2obj = json.loads(obj.replace("\'", "\""))
                    recurse(convert2obj, parent_key)
                except:
                    if parent_key in items:
                        items[parent_key] += f"{sep}{obj}"
                    else:
                        items[parent_key] = str(obj)
            else:
                if parent_key in items:
                    items[parent_key] += f"{sep}{obj}"
                else:
                    items[parent_key] = str(obj)
        
        for all_key in json_obj.keys():
            if isinstance(json_obj[all_key], (dict, list)):
                recurse(json_obj[all_key], all_key)
            elif isinstance(json_obj[all_key], str):
                try:
                    recurse(json.loads(json_obj[all_key].replace("\'", "\"")), all_key)
                except Exception as e:
                    print(e)
            else:
                continue
        return items

    def process_json(self, input_text:Dict, key_list_text:str):
        processed_text = ""
        try:
            input_text_json_obj = self.flatten_json(input_text)
            key_list = list(input_text_json_obj.keys())
            dpg.set_value(self.show_keys, "\n".join([",".join(key_list[sk_idx:sk_idx+2]) for sk_idx in range(0, len(key_list), 2)]))

            key_list_text_split = key_list_text.split("|")
  
            for key in key_list_text_split:
                if key in input_text_json_obj:
                    processed_text+= key + "\n" + input_text_json_obj[key] + "\n"

            return processed_text
        except Exception as e:
            return e

    def call_node(self, pre_node_attr_dict: Dict[int|str, list[int|str]], 
                  pre_node_list: List[BaseNode], 
                  other_paras: Optional[Dict] = None):
        self.wait_pre_node_finish(pre_node_list)
        ### All precursor nodes have been processed  ###
        if self.input_text_tag in pre_node_attr_dict:
            input_text = self.get_prenode_value(pre_node_attr_dict[self.input_text_tag])
        else:
            self.run_state = True
        key_list_text = self.get_prenode_value([self.extra_key_tag])['key_list_text'][0]
        
        result = self.process_json(input_text, key_list_text)
        print(result)
        dpg.set_value(self.result_value_tag, result)
        self.run_state = True