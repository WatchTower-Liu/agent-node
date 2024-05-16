from typing import List, Dict, Any, Optional, Union
import time
from openai import OpenAI
import sys
sys.path.append("../../")
from src.nodes.base_node import BaseNode
import dearpygui.dearpygui as dpg

class KIMI_chat_Node(BaseNode):
    def __init__(self, parent: str|int, node_name: Optional[str|int]  = None, node_tag: Optional[str|int] = None, **kwargs) -> None:
        super().__init__(parent, node_name, node_tag, **kwargs)

        self.create_node()

    def create_node(self) -> None:
        self.result_tag = self.add_attribute(label="result_attr", attribute_type=dpg.mvNode_Attr_Output)
        self.set_pin_name("result", self.result_tag, 240)
        self.result_value_tag = dpg.add_text(label="result", parent=self.result_tag, show=False)
        self.prompt_tag = self.add_attribute(label="prompt_attr", attribute_type=dpg.mvNode_Attr_Input)
        self.set_pin_name("prompt", self.prompt_tag)
        self.chat_attr_tag = self.add_attribute(label="chat", attribute_type=dpg.mvNode_Attr_Static)
        self.add_attr_value(label="api_key", parent=self.chat_attr_tag, width=200)
        self.add_attr_value(label="model_name", parent=self.chat_attr_tag, width=200)
        self.add_attr_value(label="system", parent=self.chat_attr_tag, width=200, multi_line=True, default_value="You are a helpful assistant.")
        self.sample_para_tag = self.add_attribute(label="sample_para_attr", attribute_type=dpg.mvNode_Attr_Input)
        self.set_pin_name("sample_para", self.sample_para_tag)
    
    def add_attr_value(self, label: str, parent: Optional[str|int], width, multi_line: bool = False, default_value:str="") -> None:
        dpg.add_input_text(label=label, parent=parent, width=width, multiline=multi_line, default_value=default_value)

    def process_prompt(self, all_input_data: Dict):
        finall_prompt = ""
        if "prompt" in all_input_data:
            finall_prompt = "\n".join(all_input_data["prompt"])
            return {"prompt":finall_prompt}
        return {"prompt":"Error!! Prompt not found"}

    def wait_pre_node_finish(self, pre_node_list: List[BaseNode]):
        for pre_node in pre_node_list:
            while not pre_node.down_state:
                time.sleep(0.01)

    def call_node(self, pre_node_attr_dict: Dict[int|str, list[int|str]], 
                  pre_node_list: List[BaseNode], 
                  other_paras: Optional[Dict] = None):
        self.wait_pre_node_finish(pre_node_list)
        ### All precursor nodes have been processed  ###
        input_dict = {}
        if self.sample_para_tag in pre_node_attr_dict:
            sample_para = self.get_prenode_value(pre_node_attr_dict[self.sample_para_tag])
            input_dict.update(sample_para)
        if self.prompt_tag in pre_node_attr_dict:
            prompt_data = self.get_prenode_value(pre_node_attr_dict[self.prompt_tag])
            input_dict.update(self.process_prompt(prompt_data))
        else:
            self.run_state = True
            return
        ### All input data have been collected ###

        result= self.chat(**input_dict)

        # dpg.delete_item(self.result_value_tag)
        # self.result_value_tag = dpg.add_text(default_value=result, parent=self.result_tag, label="result", tag=self.result_value_tag, show=False)
        dpg.set_value(self.result_value_tag, result)
        self.run_state = True

    def chat(self, **kwargs):
        chat_attr_child = dpg.get_item_children(self.chat_attr_tag)
        chat_attr_dict = {}
        for child in chat_attr_child.keys():
            for child_node in chat_attr_child[child]:
                chat_attr_dict[dpg.get_item_label(child_node)] = dpg.get_value(child_node)

        print(chat_attr_dict)
        print(kwargs)
        message = []
        message.append({"role": "system", "content": chat_attr_dict["system"]})
        message.append({"role": "user", "content": kwargs["prompt"]})
        result = self.get_response(api_key=chat_attr_dict["api_key"], 
                                   message=message, 
                                   temperature=kwargs["temperature"] if "temperature" in kwargs else 1,
                                   top_p=kwargs["top_p"] if "top_p" in kwargs else 1,
                                   model_name=chat_attr_dict["model_name"] if len(chat_attr_dict["model_name"]) > 0 else "moonshot-v1-32k")

        return result
        
    def get_response(self, api_key: str, message: List[Dict], temperature = 1, top_p = 1, model_name: str = "moonshot-v1-32k") -> str:
        try:
            client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")
            response = client.chat.completions.create(
                model=model_name,
                messages=message,
                temperature=temperature,
                top_p=top_p,
                # max_tokens=4096*4
            )
        except Exception as e:
            print(e)
            return "Error: " + str(e)
        return response.choices[0].message.content

