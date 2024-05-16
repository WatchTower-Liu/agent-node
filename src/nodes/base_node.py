from typing import List, Dict, Any, Optional, Union
import dearpygui.dearpygui as dpg

class BaseNode():
    def __init__(self, 
                 parent: str|int,
                 node_name: Optional[str|int] = None,
                 node_tag: Optional[str|int] = None,
                 **kwargs) -> None:
        self.node_name = node_name if node_name is not None else self.__class__.__name__
        self.node_tag = node_tag if node_tag is not None else dpg.generate_uuid()

        print(kwargs)
        self.node = dpg.add_node(label=self.node_name, tag=self.node_tag, parent=parent, **kwargs)

        self.input_attrs = {}
        self.output_attrs = {}
        self.run_state = False
    
    @property
    def down_state(self):
        return self.run_state
    
    def reset_run_state(self):
        self.run_state = False

    def add_attribute(self, *, label: str =None, user_data: Any =None, use_internal_label: bool =True, tag: Union[int, str] =0, indent: int =-1, parent: Union[int, str] =0, before: Union[int, str] =0, show: bool =True, filter_key: str ='', tracked: bool =False, track_offset: float =0.5, attribute_type: int =0, shape: int =1, category: str ='general', **kwargs) -> Union[int, str]:
        real_parent = parent if parent else self.node_tag

        attr_tag = dpg.add_node_attribute(parent=real_parent, label=label, user_data=user_data, use_internal_label=use_internal_label, tag=tag, indent=indent, before=before, show=show, filter_key=filter_key, tracked=tracked, track_offset=track_offset, attribute_type=attribute_type, shape=shape, category=category, **kwargs)

        if attribute_type == dpg.mvNode_Attr_Input:
            self.input_attrs[attr_tag] = attr_tag
        elif attribute_type == dpg.mvNode_Attr_Output:
            self.output_attrs[attr_tag] = attr_tag
        
        return attr_tag
    
    def get_prenode_value(self, pre_paras_tag: List[int|str]):
        sample_para = {}
        for pre_para in pre_paras_tag:
            all_child = dpg.get_item_children(pre_para)
            for child in all_child.keys():
                for child_node in all_child[child]:
                    IL = dpg.get_item_label(child_node)
                    if IL not in sample_para:
                        sample_para[IL] = [dpg.get_value(child_node)]
                    else:
                        sample_para[IL].append(dpg.get_value(child_node))
        return sample_para

    def set_pin_name(self, pin_name: str, parent: str|int, indent = 0, **kwargs):
        dpg.add_text(pin_name, parent=parent, show=True, indent=indent)
        
    
    def add_attr_value(self, *args, **kwargs):
        raise NotImplementedError
    
    def call_node(self, *args, **kwargs):
        raise NotImplementedError
    


def main():
    pass

if __name__ == "__main__":
    main()

