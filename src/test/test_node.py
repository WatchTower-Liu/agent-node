import dearpygui.dearpygui as dpg
import sys
sys.path.append("../")
from utils.utils import set_UI_font

from window_s.node_editor_window import NodeWindow
from window_s.node_management_window import NodeManagementWindow
from window_s.click_window import NodeRightClickWindow, NodeEditorWindowRightClickWindow

dpg.create_context()


set_UI_font()
# with dpg.window(label="node_editor", width=800, height=800):
node_window = NodeWindow(window_width=1200, window_height=800, window_pos=[0, 0])
node_editor_tag = node_window.set_node_editor()

NodeRightClickWindow(80, 80, node_window)
NodeEditorWindowRightClickWindow(200, 300, node_editor_tag, node_window)

node_management_window = NodeManagementWindow(window_width=300, window_height=800, 
                                              window_pos=[1200, 0],
                                              node_editor_tag=node_editor_tag, node_window=node_window, 
                                              node_runner_config={"1": "1"})
node_management_window.set_node_management()

dpg.create_viewport(title='Custom Title', width=1510, height=840)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()