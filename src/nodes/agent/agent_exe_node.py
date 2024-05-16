from typing import Optional, List, Dict, Any
import dearpygui.dearpygui as dpg
import time
import re
import json
import requests

import sys
sys.path.append("../../")
from src.nodes.base_node import BaseNode


class AgentExeNode(BaseNode):
    def __init__(self, parent: str|int, node_name: Optional[str|int]  = None, node_tag: Optional[str|int] = None, **kwargs) -> None:
        super().__init__(parent, node_name, node_tag, **kwargs)

        self.create_node()

    def create_node(self) -> None:
        self.used_tools_tag = self.add_attribute(label="used_tools_attr", attribute_type=dpg.mvNode_Attr_Input)
        self.set_pin_name("tools", self.used_tools_tag)

        self.model_result_tag = self.add_attribute(label="model_result_attr", attribute_type=dpg.mvNode_Attr_Input)
        self.set_pin_name("model_result", self.model_result_tag)

        self.helper_tag = self.add_attribute(label="helper_attr", attribute_type=dpg.mvNode_Attr_Static)

        self.execute_result = self.add_attribute(label="execute_result_attr", attribute_type=dpg.mvNode_Attr_Output)
        self.set_pin_name("execute_result", self.execute_result, 100)
        self.result_value_tag = dpg.add_text(label="execute_result", parent=self.execute_result, show=False)

    def add_attr_value(self, default_value: Optional[Any] = None, label: List[str] = None, parent: Optional[str|int] = None, width: int = 150) -> None:
        dpg.add_text(default_value=default_value[0], label=label[0], parent=parent)

    def wait_pre_node_finish(self, pre_node_list: List[BaseNode]):
        for pre_node in pre_node_list:
            while not pre_node.down_state:
                time.sleep(0.01)

    def call_url(self, url: str, data: Dict):

        response = requests.post(url, data=json.dumps(data))
        print(response)
        data = response.json()
        print(type(data))
        print(data)
        if data['status'] == '0':
            raise RuntimeError(data)
        
        return data
    
    def process_model_result(self, result: Dict, tools_data: Dict):
        real_result = result["result"][0]
        try:
            real_result = real_result.replace("“","\"").replace("”","\"").replace("‘","\'").replace("’","\'")
            pattern = re.compile("\{(.|\n)*(\'|\")result(\'|\")(:|：)( )*(.|\n)*\}")
            match_R = re.search(pattern, real_result)
            if match_R is None:
                return "result not match"

            real_result = real_result[match_R.span()[0]:match_R.span()[1]]
            real_result_obj = json.loads(real_result)["result"]
            tool_name = real_result_obj["tool_name"]
            tool_parameter = real_result_obj["tool_parameter"]
            call_func = real_result_obj["call_func"]
            if tool_name not in tools_data["tool_name"]:
                return "tool name not match"

            query_result = self.call_url(call_func, tool_parameter)
        except Exception as e:
            print(e)
            return "error {}".format(e)

        return query_result


    def call_node(self, pre_node_attr_dict: Dict[int|str, list[int|str]], 
                  pre_node_list: List[BaseNode], 
                  other_paras: Optional[Dict] = None):
        
        self.wait_pre_node_finish(pre_node_list)
        if self.used_tools_tag in pre_node_attr_dict:
            tools_data = self.get_prenode_value(pre_node_attr_dict[self.used_tools_tag])
        else:
            self.run_state = True
            return

        if self.model_result_tag in pre_node_attr_dict:
            model_result = self.get_prenode_value(pre_node_attr_dict[self.model_result_tag])
        else:
            self.run_state = True
            return

        result = self.process_model_result(model_result, tools_data)

        dpg.set_value(self.result_value_tag, str(result))
        self.run_state = True
