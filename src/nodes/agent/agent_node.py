from typing import List, Dict, Any, Optional, Union
import time
import json
import sys
sys.path.append("../../")
from src.nodes.base_node import BaseNode
import dearpygui.dearpygui as dpg


class AgentNode(BaseNode):
    tool_names_description = """
### {tool_name}: {tool_description} 输入参数：{tool_parameter} 调用函数：{call_func}
"""
    tools_prompt_ZN = """
    你需要根绝用户的输入，思考用户的需求，然后给出合适的工具。
    你拥有的工具有：
    {tool_names_description}
    你需要选择工具，这些工具必须是{tool_names}之一。
    返回格式：
    {{
        "思考"："思考如何选择tools",
        "result": {{ "tool_name": "你选择的工具", "tool_parameter": "工具的参数", "call_func": "调用函数"}}
    }}
    严格按照这种格式返回，保证可以被json.loads()解析。
    用户输入的内容是：
    {user}
    """
    def __init__(self, parent: str|int, node_name: Optional[str|int]  = None, node_tag: Optional[str|int] = None, **kwargs) -> None:
        super().__init__(parent, node_name, node_tag, **kwargs)

        self.create_node()

    def create_node(self) -> None:
        self.used_tools_tag = self.add_attribute(label="used_tools_attr", attribute_type=dpg.mvNode_Attr_Input)
        self.set_pin_name("tools", self.used_tools_tag)

        self.agent_prompt_tag = self.add_attribute(label="agent_prompt_attr", attribute_type=dpg.mvNode_Attr_Input)
        self.set_pin_name("agent_prompt", self.agent_prompt_tag)

        self.helper_tag = self.add_attribute(label="helper_attr", attribute_type=dpg.mvNode_Attr_Static)

        self.processed_agent_prompt = self.add_attribute(label="processed_agent_prompt_attr", attribute_type=dpg.mvNode_Attr_Output)
        self.set_pin_name("processed_agent_prompt", self.processed_agent_prompt, 100)
        self.result_value_tag = dpg.add_text(label="prompt", parent=self.processed_agent_prompt, show=False)

    def add_attr_value(self, default_value: Optional[Any] = None, label: List[str] = None, parent: Optional[str|int] = None, width: int = 150) -> None:
        dpg.add_text(default_value=default_value[0], label=label[0], parent=parent)


    def wait_pre_node_finish(self, pre_node_list: List[BaseNode]):
        for pre_node in pre_node_list:
            while not pre_node.down_state:
                time.sleep(0.01)

    def process_agent_prompt(self, all_input_data: Dict):
        prompt = all_input_data.get("prompt", "")
        if isinstance(prompt, str):
            prompt = "\n".join(json.loads(prompt))
        elif isinstance(prompt, list):
            prompt = "\n".join(prompt)
        tool_names = all_input_data["tool_name"]
        call_funcs = all_input_data["call_func/url"]
        tool_description = all_input_data["tool_description"]
        tool_parameter = all_input_data["tool_parameter"]

        tool_names_description = ""
        for tool_name, call_func, description, parameter in zip(tool_names, call_funcs, tool_description, tool_parameter):
            tool_names_description += self.tool_names_description.format(tool_name=tool_name, 
                                                                         call_func=call_func, 
                                                                         tool_description=description, 
                                                                         tool_parameter=parameter)
        fprompt = self.tools_prompt_ZN.format(tool_names_description=tool_names_description, tool_names=tool_names, user=prompt)
        return fprompt

    def call_node(self, pre_node_attr_dict: Dict[int|str, list[int|str]], 
                  pre_node_list: List[BaseNode], 
                  other_paras: Optional[Dict] = None):
        
        self.wait_pre_node_finish(pre_node_list)
        ### All precursor nodes have been processed  ###
        use_input_dict = {}
        if self.used_tools_tag in pre_node_attr_dict:
            tools_data = self.get_prenode_value(pre_node_attr_dict[self.used_tools_tag])
            print(tools_data)
            use_input_dict.update(tools_data)
        else:
            self.run_state = True
            dpg.set_value(self.result_value_tag, "error tools not found")
            print("error tools not found")
            return 

        if self.agent_prompt_tag in pre_node_attr_dict:
            prompt_data = self.get_prenode_value(pre_node_attr_dict[self.agent_prompt_tag])
            use_input_dict.update(prompt_data)
        else:
            self.run_state = True
            dpg.set_value(self.result_value_tag, "agent prompt not found")
            print("agent prompt not found")
            return 

        chat_prompt = self.process_agent_prompt(use_input_dict)
        print(chat_prompt)

        # dpg.delete_item(self.result_value_tag)
        # self.result_value_tag = dpg.add_text(default_value=chat_prompt, parent=self.processed_agent_prompt, label="prompt", tag=self.result_value_tag, show=False)
        dpg.set_value(self.result_value_tag, chat_prompt)
        self.run_state = True

