import dearpygui.dearpygui as dpg

def set_UI_font(font_path="../../font/simhei.ttf", font_size = 16):
    with dpg.font_registry():
        with dpg.font(font_path, font_size) as font1:  # 增加中文编码范围，防止问号
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
        dpg.bind_font(font1)


def help(message, parent):
    last_item = dpg.last_item()
    group = dpg.add_group(parent = parent, horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("(?)", color=[0, 255, 0])
    tip_tag = dpg.add_tooltip(t)
    dpg.add_text(message, parent=tip_tag)