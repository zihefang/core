"""
The actions taken when each menubar option is clicked
"""

import logging
import webbrowser
from tkinter import filedialog, messagebox

from core.api.grpc import core_pb2
from coretk.setwallpaper import CanvasWallpaper
from coretk.sizeandscale import SizeAndScale

SAVEDIR = "/home/ncs/Desktop/"


def sub_menu_items():
    logging.debug("Click on sub menu items")


def file_new():
    logging.debug("Click file New")


def file_new_shortcut(event):
    logging.debug("Shortcut for file new shortcut")


def file_open():
    logging.debug("Click file Open")


def file_open_shortcut(event):
    logging.debug("Shortcut for file open")


def file_reload():
    logging.debug("Click file Reload")


def file_save():
    logging.debug("Click file save")


def file_save_shortcut(event):
    logging.debug("Shortcut for file save")


def file_export_python_script():
    logging.debug("Click file export python script")


def file_execute_xml_or_python_script():
    logging.debug("Execute XML or Python script")


def file_execute_python_script_with_options():
    logging.debug("Click execute Python script with options")


def file_open_current_file_in_editor():
    logging.debug("Click file open current in editor")


def file_print():
    logging.debug("Click file Print")


def file_save_screenshot():
    logging.debug("Click file save screenshot")


def edit_undo():
    logging.debug("Click edit undo")


def edit_undo_shortcut(event):
    logging.debug("Shortcut for edit undo")


def edit_redo():
    logging.debug("Click edit redo")


def edit_redo_shortcut(event):
    logging.debug("Shortcut for edit redo")


def edit_cut():
    logging.debug("Click edit cut")


def edit_cut_shortcut(event):
    logging.debug("Shortcut for edit cut")


def edit_copy():
    logging.debug("Click edit copy")


def edit_copy_shortcut(event):
    logging.debug("Shortcut for edit copy")


def edit_paste():
    logging.debug("Click edit paste")


def edit_paste_shortcut(event):
    logging.debug("Shortcut for edit paste")


def edit_select_all():
    logging.debug("Click edit select all")


def edit_select_all_shortcut(event):
    logging.debug("Shortcut for edit select all")


def edit_select_adjacent():
    logging.debug("Click edit select adjacent")


def edit_select_adjacent_shortcut(event):
    logging.debug("Shortcut for edit select adjacent")


def edit_find():
    logging.debug("CLick edit find")


def edit_find_shortcut(event):
    logging.debug("Shortcut for edit find")


def edit_clear_marker():
    logging.debug("Click edit clear marker")


def edit_preferences():
    logging.debug("Click preferences")


def canvas_new():
    logging.debug("Click canvas new")


def canvas_manage():
    logging.debug("Click canvas manage")


def canvas_delete():
    logging.debug("Click canvas delete")


def canvas_size_scale():
    logging.debug("Click canvas size/scale")
    SizeAndScale()


def canvas_wallpaper():
    logging.debug("CLick canvas wallpaper")


def canvas_previous():
    logging.debug("Click canvas previous")


def canvas_previous_shortcut(event):
    logging.debug("Shortcut for canvas previous")


def canvas_next():
    logging.debug("Click canvas next")


def canvas_next_shortcut(event):
    logging.debug("Shortcut for canvas next")


def canvas_first():
    logging.debug("CLick canvas first")


def canvas_first_shortcut(event):
    logging.debug("Shortcut for canvas first")


def canvas_last():
    logging.debug("CLick canvas last")


def canvas_last_shortcut(event):
    logging.debug("Shortcut canvas last")


def view_show():
    logging.debug("Click view show")


def view_show_hidden_nodes():
    logging.debug("Click view show hidden nodes")


def view_locked():
    logging.debug("Click view locked")


def view_3d_gui():
    logging.debug("CLick view 3D GUI")


def view_zoom_in():
    logging.debug("Click view zoom in")


def view_zoom_in_shortcut(event):
    logging.debug("Shortcut view zoom in")


def view_zoom_out():
    logging.debug("Click view zoom out")


def view_zoom_out_shortcut(event):
    logging.debug("Shortcut view zoom out")


def tools_auto_rearrange_all():
    logging.debug("Click tools, auto rearrange all")


def tools_auto_rearrange_selected():
    logging.debug("CLick tools auto rearrange selected")


def tools_align_to_grid():
    logging.debug("Click tools align to grid")


def tools_traffic():
    logging.debug("Click tools traffic")


def tools_ip_addresses():
    logging.debug("Click tools ip addresses")


def tools_mac_addresses():
    logging.debug("Click tools mac addresses")


def tools_build_hosts_file():
    logging.debug("Click tools build hosts file")


def tools_renumber_nodes():
    logging.debug("Click tools renumber nodes")


def tools_experimental():
    logging.debug("Click tools experimental")


def tools_topology_generator():
    logging.debug("Click tools topology generator")


def tools_debugger():
    logging.debug("Click tools debugger")


def widgets_observer_widgets():
    logging.debug("Click widgets observer widgets")


def widgets_adjacency():
    logging.debug("Click widgets adjacency")


def widgets_throughput():
    logging.debug("Click widgets throughput")


def widgets_configure_adjacency():
    logging.debug("Click widgets configure adjacency")


def widgets_configure_throughput():
    logging.debug("Click widgets configure throughput")


def session_change_sessions():
    logging.debug("Click session change sessions")


def session_node_types():
    logging.debug("Click session node types")


def session_comments():
    logging.debug("Click session comments")


def session_hooks():
    logging.debug("Click session hooks")


def session_reset_node_positions():
    logging.debug("Click session reset node positions")


def session_emulation_servers():
    logging.debug("Click session emulation servers")


def session_options():
    logging.debug("Click session options")


def help_about():
    logging.debug("Click help About")


class MenuAction:
    """
    Actions performed when choosing menu items
    """

    def __init__(self, application, master):
        self.master = master
        self.application = application
        self.core_grpc = application.core_grpc

    def clean_nodes_links_and_set_configuarations(self):
        """
        Prompt use to stop running session before application is closed

        :return: nothing
        """
        logging.info(
            "menuaction.py: clean_nodes_links_and_set_configuration() Exiting the program"
        )
        grpc = self.application.core_grpc
        state = grpc.get_session_state()

        if (
            state == core_pb2.SessionState.SHUTDOWN
            or state == core_pb2.SessionState.DEFINITION
        ):
            grpc.delete_session()
            grpc.core.close()
            # self.application.quit()
        else:
            msgbox = messagebox.askyesnocancel("stop", "Stop the running session?")

            if msgbox or msgbox is False:
                if msgbox:
                    grpc.set_session_state("datacollect")
                    grpc.delete_links()
                    grpc.delete_nodes()
                    grpc.delete_session()
                # else:
                #     grpc.set_session_state("definition")
                grpc.core.close()
                # self.application.quit()

    def on_quit(self):
        """
        Prompt user whether so save running session, and then close the application

        :return: nothing
        """
        self.clean_nodes_links_and_set_configuarations()
        # self.application.core_grpc.close()
        self.application.quit()

    def file_save_as_xml(self):
        logging.info("menuaction.py file_save_as_xml()")
        grpc = self.application.core_grpc
        file_path = filedialog.asksaveasfilename(
            initialdir=SAVEDIR,
            title="Save As",
            filetypes=(("EmulationScript XML files", "*.xml"), ("All files", "*")),
            defaultextension=".xml",
        )
        # with open("prev_saved_xml.txt", "a") as file:
        #     file.write(file_path + "\n")
        grpc.save_xml(file_path)

    def file_open_xml(self):
        logging.info("menuaction.py file_open_xml()")
        file_path = filedialog.askopenfilename(
            initialdir=SAVEDIR,
            title="Open",
            filetypes=(("EmulationScript XML File", "*.xml"), ("All Files", "*")),
        )
        # clean up before opening a new session
        self.clean_nodes_links_and_set_configuarations()
        # grpc = CoreGrpc(self.application.master)
        # grpc.core.connect()
        core_grpc = self.application.core_grpc
        core_grpc.core.connect()
        # session_id = core_grpc.open_xml(file_path)
        # core_grpc.session_id = session_id

        core_grpc.open_xml(file_path)
        # print("Print session state")
        # print(grpc.get_session_state())
        self.application.canvas.canvas_reset_and_redraw(core_grpc)

        # Todo might not need
        self.application.core_grpc = core_grpc

        self.application.core_editbar.destroy_children_widgets()
        self.application.core_editbar.create_runtime_toolbar()
        # self.application.canvas.draw_existing_component()
        # t1 = time.clock()
        # print(t1 - t0)

    def canvas_size_and_scale(self):
        SizeAndScale(self.application)

    def canvas_set_wallpaper(self):
        CanvasWallpaper(self.application)

    def help_core_github(self):
        webbrowser.open_new("https://github.com/coreemu/core")

    def help_core_documentation(self):
        webbrowser.open_new("http://coreemu.github.io/core/")
