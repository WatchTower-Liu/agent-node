from typing import List, Dict
from threading import Thread
from multiprocessing import Process
import sys
sys.path.append("../")

from src.nodes.base_node import BaseNode

class NodeRunner():
    def __init__(self, node_list: List[BaseNode], 
                 adjacency_list: Dict[int|str, List[int|str]], 
                 adjacency_list_reverse: Dict[int|str, List[int|str]],
                 running_config: Dict) -> None:
        self.node_list = node_list
        self.adjacency_list = adjacency_list
        self.running_config = running_config
        self.adjacency_list_reverse = adjacency_list_reverse

    def find_start_node(self):
        start_node: List[BaseNode] = []
        for node in self.node_list:
            if len(node.input_attrs) == 0:
                start_node.append(node)

        return start_node 
    
    def run_start_nodes(self, start_node_list: List[BaseNode]):
        run_thread_list = []
        for first_run_node in start_node_list:
            run_thread = Thread(target=first_run_node.call_node, args=([], []))
            run_thread.start()
            run_thread_list.append(run_thread)
        for thread in run_thread_list:
            thread.join()

    def reset_run_state(self):
        for node in self.node_list:
            node.run_state = False

    def check_finish(self):
        not_down_index = []
        for idx, node in enumerate(self.node_list):
            if not node.run_state:
                not_down_index.append(idx)
        return not_down_index
    
    def all_cut(self):
        for node in self.node_list:
            node.run_state = True

    def run(self):
        start_node_list = self.find_start_node()
        self.run_start_nodes(start_node_list)    ## run from start node
        
        self.running_config
        while True:
            not_down_index = self.check_finish()
            if len(not_down_index) == 0:
                break

            print(start_node_list[0].output_attrs)
            print(self.adjacency_list)
            print(self.adjacency_list_reverse)
            process_thred_list = []
            for idx in not_down_index:
                pre_node_attr_dict = {}
                pre_node_list = []
                real_node = self.node_list[idx]
                for input_attr_tag in real_node.input_attrs:
                    if input_attr_tag not in self.adjacency_list_reverse:
                        continue
                    pre_node_attr_dict[input_attr_tag] = self.adjacency_list_reverse[input_attr_tag]
                    for pre_node_tag in self.adjacency_list_reverse[input_attr_tag]:
                        for node in self.node_list:
                            if pre_node_tag in node.output_attrs:
                                pre_node_list.append(node)

                run_thread = Thread(target=real_node.call_node, args=(pre_node_attr_dict, pre_node_list))
                run_thread.start()
                process_thred_list.append(run_thread)
            for thread in process_thred_list:
                thread.join()

        self.reset_run_state()
        
