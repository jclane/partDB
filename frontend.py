"""Displays the GUI for SubHunt."""

import tkinter as tk
from tkinter import messagebox, filedialog

from backend import (remove_table, part_in_db, add_part, remove_part,
                     convert_to_dict, update_part, list_subs,
                     is_valid_sub, import_from_csv)


def clear_widgets(frame):
    """Removes all widgets from frame."""
    for widget in frame.winfo_children():
        widget.destroy()


class Main(tk.Tk):
    """Displays initial state of GUI."""

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.menu = tk.Menu(self)

        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.file_menu.add_command(label="Import", command=self.import_list)
        self.file_menu.add_command(label="Purge Records",
                                   command=lambda:
                                   self.show_frame("PurgePage"))
        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.edit = tk.Menu(self.menu, tearoff=False)
        self.edit.add_command(label="Add",
                              command=lambda: self.show_frame("AddPartPage"))
        self.edit.add_command(label="Remove",
                              command=lambda:
                              self.show_frame("RemovePartPage"))
        self.edit.add_command(label="Edit",
                              command=lambda: self.show_frame("EditPartPage"))
        self.menu.add_cascade(label="Edit", menu=self.edit)

        self.search_menu = tk.Menu(self.menu, tearoff=False)
        self.search_menu.add_command(label="Part Info",
                                     command=lambda:
                                     self.show_frame("SearchPage"))
        self.search_menu.add_command(label="Verify Sub",
                                     command=lambda:
                                     self.show_frame("VerifySubsPage"))
        self.search_menu.add_command(label="List Subs",
                                     command=lambda:
                                     self.show_frame("FindSubsPage"))
        self.menu.add_cascade(label="Search", menu=self.search_menu)

        self.help_menu = tk.Menu(self.menu, tearoff=False)
        self.help_menu.add_command(label="Help [coming soon]")
        self.help_menu.add_command(label="About partDB [coming soon]")
        self.menu.add_cascade(label="?", menu=self.help_menu)

        self.config(menu=self.menu)
        self.geometry("860x525")

        self.container = tk.Frame(self)
        self.container.grid(column=0, row=0, sticky="EW")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for frame_name in (MainPage, PurgePage, AddPartPage, RemovePartPage,
                           EditPartPage, SearchPage, VerifySubsPage,
                           FindSubsPage):
            page_name = frame_name.__name__
            frame = frame_name(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()

    def import_list(self):
        """Opens a dialog window to pick file for import"""
        file = filedialog.askopenfilename(title="Import",
                                          filetypes=[("CSV files", "*.csv")])

        if file != "":
            import_from_csv(file)


class MainPage(tk.Frame):
    """Initial page.  Is blank."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


class PurgePage(tk.Frame):
    """Displays GUI for user to remove tables from database."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.db_label = tk.Label(self, text="Database to purge: ")
        self.db_label.grid(column=0, row=0, sticky="EW")

        self.db_var = tk.StringVar()
        self.db_var.set("CPU")
        self.databases = ("CPU", "HDD", "MEM")

        self.db_drop = tk.OptionMenu(self, self.db_var, *self.databases)
        self.db_drop.grid(column=1, row=0, sticky="EW")

        self.purge_button = tk.Button(
            self,
            text="Purge",
            command=self.purge_table
            )
        self.purge_button.grid(column=1, row=1, sticky="EW")

    def purge_table(self):
        """Calls remove_table to remove table from the database."""
        if remove_table(self.db_var.get().lower()):
            messagebox.showinfo("Purge Complete",
                                self.db_var.get() + " table purged.")
        else:
            messagebox.showerror("Error!")


class AddPartPage(tk.Frame):
    """Displays GUI for users to add parts to the database."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.container = tk.Frame(self)
        self.container.grid(column=0, row=0, sticky="EW")

        self.sub_frame = tk.Frame(self)
        self.sub_frame.grid(column=0, row=1, padx=5, pady=5)

        self.part_type_label = tk.Label(self.container,
                                        text="Select part type: ")
        self.part_type_label.grid(column=0, row=0, sticky="W")
        self.part_types = ["HDD", "SSD", "SSHD", "MEM", "CPU"]
        self.part_types_var = tk.StringVar()
        self.part_types_var.set("HDD")
        self.part_type_drop = tk.OptionMenu(self.container,
                                            self.part_types_var,
                                            *self.part_types)
        self.part_type_drop.grid(column=1, row=0, sticky="EW")

        self.part_types_var.trace('w', self.change_dropdown)

    def add_hdd(self):
        """
        Displays GUI for the user to add a record to the "hdd"
        table.
        """

        self.part_num_label = tk.Label(self.sub_frame, text="Part Number: ")
        self.part_num_label.grid(column=0, row=1)
        self.part_num_box = tk.Entry(self.sub_frame)
        self.part_num_box.grid(column=1, row=1, sticky="EW")

        self.brand_label = tk.Label(self.sub_frame, text="Brand: ")
        self.brand_label.grid(column=0, row=2)
        self.brand_var = tk.StringVar()
        self.brand_var.set("Acer")
        self.brands = ("Acer", "Asus", "CVO", "Dell", "Hewlett Packard",
                       "Lenovo", "Samsung", "Sony", "Toshiba")
        self.brand_drop = tk.OptionMenu(self.sub_frame,
                                        self.brand_var,
                                        *self.brands)
        self.brand_drop.grid(column=1, row=2, sticky="EW")

        self.description_label = tk.Label(self.sub_frame,
                                          text="Description: ")
        self.description_label.grid(column=0, row=3)
        self.description_box = tk.Entry(self.sub_frame)
        self.description_box.grid(column=1, row=3)

        self.connector_label = tk.Label(self.sub_frame, text="Connector: ")
        self.connector_label.grid(column=0, row=4)
        self.connector_var = tk.StringVar()
        self.connector_var.set("SATA")
        if self.part_types_var.get() in ["HDD", "SSHD"]:
            self.connectors = ("SATA", "IDE", "proprietary")
        elif self.part_types_var.get() == "SSD":
            self.connectors = ("SATA", "m.2", "eMMC", "mSATA", "proprietary")
        self.connector_drop = tk.OptionMenu(self.sub_frame,
                                            self.connector_var,
                                            *self.connectors)
        self.connector_drop.grid(column=1, row=4)

        self.hdd_capacity_box = tk.Entry(self.sub_frame)
        self.ssd_capacity_box = tk.Entry(self.sub_frame)
        if self.part_types_var.get() in ["HDD", "SSHD"]:
            self.hdd_capacity_label = tk.Label(
                self.sub_frame, text="HDD Capacity (GB): "
                )
            self.hdd_capacity_label.grid(column=0, row=5)
            self.hdd_capacity_box.grid(column=1, row=5)
        else:
            self.hdd_capacity_box.insert(0, "")

        if self.part_types_var.get() in ["SSHD", "SSD"]:
            self.ssd_capacity_label = tk.Label(self.sub_frame,
                                               text="SSD Capacity (GB): ")
            self.ssd_capacity_label.grid(column=0, row=6)
            self.ssd_capacity_box.grid(column=1, row=6)
        else:
            self.ssd_capacity_box.insert(0, "")

        self.speed_box = tk.Entry(self.sub_frame)
        if self.part_types_var.get() in ["HDD", "SSHD"]:
            self.speed_label = tk.Label(self.sub_frame, text="Speed: ")
            self.speed_label.grid(column=0, row=7)
            self.speed_box.grid(column=1, row=7)
        else:
            self.speed_box.insert(0, "")

        self.physical_size_label = tk.Label(self.sub_frame,
                                            text="Physical Size: ")
        self.physical_size_label.grid(column=0, row=8)
        self.physical_size_var = tk.StringVar()
        self.physical_size_var.set("2.5")
        if self.part_types_var.get() == "SSD":
            self.physical_sizes = ("2.5", "2280", "2260", "2242", "2230")
        elif self.part_types_var.get() in ["HDD", "SSHD"]:
            self.physical_sizes = ("2.5", "3.5")
        self.physical_size_drop = tk.OptionMenu(self.sub_frame,
                                                self.physical_size_var,
                                                *self.physical_sizes)
        self.physical_size_drop.grid(column=1, row=8)

        self.height_var = tk.StringVar()
        self.height_var.set("")

        self.height_label = tk.Label(self.sub_frame, text="Height: ")
        self.height_label.grid(column=0, row=9)
        self.heights = ("5", "7", "9.5")
        self.height_drop = tk.OptionMenu(self.sub_frame,
                                         self.height_var,
                                         *self.heights)
        self.height_drop.grid(column=1, row=9)

        self.interface_label = tk.Label(self.sub_frame, text="Interface: ")
        self.interface_label.grid(column=0, row=10)
        self.interface_var = tk.StringVar()
        self.interface_var.set("SATA III")
        if self.part_types_var.get() == "SSD":
            self.interface_var.set("SATA")
            self.interfaces = ("SATA", "PCIe")
        elif self.part_types_var.get() in ["HDD", "SSHD"]:
            self.interfaces = ("SATA III", "SATA II", "SATA I",
                               "SATA", "PATA")
        self.interfaces_drop = tk.OptionMenu(self.sub_frame,
                                             self.interface_var,
                                             *self.interfaces)
        self.interfaces_drop.grid(column=1, row=10)

        self.do_not_sub_var = tk.BooleanVar()
        self.do_not_sub_var.set(False)
        self.do_not_sub_check = tk.Checkbutton(self.sub_frame,
                                               text="Do Not Sub? ",
                                               variable=self.do_not_sub_var,
                                               anchor="w")
        self.do_not_sub_check.grid(column=1, row=11, sticky="EW")

        self.subbed_var = tk.BooleanVar()
        self.subbed_var.set(False)
        self.subbed_check = tk.Checkbutton(self.sub_frame, text="Subbed? ",
                                           variable=self.subbed_var,
                                           anchor="w")
        self.subbed_check.grid(column=1, row=12, sticky="EW")

        def add_it():
            self.part_info = (self.part_num_box.get().strip(),
                              self.brand_var.get(), self.connector_var.get(),
                              self.hdd_capacity_box.get(),
                              self.ssd_capacity_box.get(),
                              self.speed_box.get(),
                              self.part_types_var.get(),
                              self.physical_size_var.get(),
                              self.height_var.get(), self.interface_var.get(),
                              self.description_box.get(),
                              str(bool(self.do_not_sub_var.get())).upper(),
                              str(bool(self.subbed_var.get())).upper())
            if add_part("hdd", self.part_info) == "Done":
                messagebox.showinfo("Part Added",
                                    self.part_num_box.get().strip() +
                                    " has been added to the database.")

        self.add_button = tk.Button(self.sub_frame, text="Add",
                                    command=add_it)
        self.add_button.grid(column=1, row=13, sticky="EW")

    def add_mem(self):
        """
        Displays GUI for the user to add a record to the "mem"
        table.
        """

        self.part_num_label = tk.Label(self.sub_frame, text="Part Number: ")
        self.part_num_label.grid(column=0, row=1)

        self.part_num_box = tk.Entry(self.sub_frame)
        self.part_num_box.grid(column=1, row=1, sticky="EW")

        self.brand_label = tk.Label(self.sub_frame, text="Brand: ")
        self.brand_label.grid(column=0, row=2)

        self.brand_var = tk.StringVar()
        self.brand_var.set("Acer")
        self.brands = ("Acer", "Asus", "CVO", "Dell", "Hewlett Packard",
                       "Lenovo", "Samsung", "Sony", "Toshiba")

        self.brand_drop = tk.OptionMenu(self.sub_frame,
                                        self.brand_var,
                                        *self.brands)
        self.brand_drop.grid(column=1, row=2, sticky="EW")

        self.description_label = tk.Label(self.sub_frame,
                                          text="Description: ")
        self.description_label.grid(column=0, row=3)

        self.description_box = tk.Entry(self.sub_frame)
        self.description_box.grid(column=1, row=3)

        self.speed_label = tk.Label(self.sub_frame, text="Speed: ")
        self.speed_label.grid(column=0, row=4)

        self.speed_box = tk.Entry(self.sub_frame)
        self.speed_box.grid(column=1, row=4)

        self.connector_label = tk.Label(self.sub_frame, text="Connector: ")
        self.connector_label.grid(column=0, row=5)

        self.connector_var = tk.StringVar()
        self.connector_var.set("SO-DIMM")
        self.connectors = ("SO-DIMM", "UDIMM")

        self.connector_drop = tk.OptionMenu(self.sub_frame,
                                            self.connector_var,
                                            *self.connectors)
        self.connector_drop.grid(column=1, row=5)

        self.capacity_label = tk.Label(self.sub_frame, text="Capacity (GB): ")
        self.capacity_label.grid(column=0, row=6)

        self.capacity_box = tk.Entry(self.sub_frame)
        self.capacity_box.grid(column=1, row=6)

        self.do_not_sub_var = tk.BooleanVar()
        self.do_not_sub_var.set(False)

        self.do_not_sub_check = tk.Checkbutton(self.sub_frame,
                                               text="Do Not Sub? ",
                                               variable=self.do_not_sub_var,
                                               offvalue=False, onvalue=True,
                                               anchor="w")
        self.do_not_sub_check.grid(column=1, row=7, sticky="EW")

        self.subbed_var = tk.BooleanVar()
        self.subbed_var.set(False)

        self.subbed_check = tk.Checkbutton(self.sub_frame, text="Subbed? ",
                                           variable=self.subbed_var,
                                           offvalue=False,
                                           onvalue=True, anchor="w")
        self.subbed_check.grid(column=1, row=8, sticky="EW")

        def add_it():
            self.part_info = (self.part_num_box.get(), self.speed_box.get(),
                              self.brand_var.get(), self.connector_var.get(),
                              self.capacity_box.get(),
                              self.description_box.get(),
                              str(bool(self.do_not_sub_var.get())).upper(),
                              str(bool(self.subbed_var.get())).upper())
            if add_part("mem", self.part_info) == "Done":
                messagebox.showinfo("Part Added",
                                    self.part_num_box.get().strip() +
                                    " has been added to the database.")

        self.add_button = tk.Button(self.sub_frame, text="Add",
                                    command=add_it)
        self.add_button.grid(column=1, row=9, sticky="EW")

    def add_cpu(self):
        """
        Displays GUI for the user to add a record to the "cpu" table.
        """

        self.part_num_label = tk.Label(self.sub_frame, text="Part Number: ")
        self.part_num_label.grid(column=0, row=1)

        self.part_num_box = tk.Entry(self.sub_frame)
        self.part_num_box.grid(column=1, row=1, sticky="EW")

        self.brand_label = tk.Label(self.sub_frame, text="Brand: ")
        self.brand_label.grid(column=0, row=2)

        self.brand_var = tk.StringVar()
        self.brand_var.set("Acer")
        self.brands = ("Acer", "Asus", "CVO", "Dell", "Hewlett Packard",
                       "Lenovo", "Samsung", "Sony", "Toshiba")

        self.brand_drop = tk.OptionMenu(self.sub_frame, self.brand_var,
                                        *self.brands)
        self.brand_drop.grid(column=1, row=2, sticky="EW")

        self.description_label = tk.Label(self.sub_frame,
                                          text="Description: ")
        self.description_label.grid(column=0, row=3)

        self.description_box = tk.Entry(self.sub_frame)
        self.description_box.grid(column=1, row=3)

        self.oem_label = tk.Label(self.sub_frame, text="OEM Part Number: ")
        self.oem_label.grid(column=0, row=3)

        self.oem_box = tk.Entry(self.sub_frame)
        self.oem_box.grid(column=1, row=3)

        self.do_not_sub_var = tk.BooleanVar()
        self.do_not_sub_var.set(False)

        self.do_not_sub_check = tk.Checkbutton(self.sub_frame,
                                               text="Do Not Sub? ",
                                               variable=self.do_not_sub_var,
                                               offvalue=False, onvalue=True,
                                               anchor="w")
        self.do_not_sub_check.grid(column=1, row=7, sticky="EW")

        self.subbed_var = tk.BooleanVar()
        self.subbed_var.set(False)

        self.subbed_check = tk.Checkbutton(self.sub_frame, text="Subbed? ",
                                           variable=self.subbed_var,
                                           offvalue=False, onvalue=True,
                                           anchor="w")
        self.subbed_check.grid(column=1, row=8, sticky="EW")

        def add_it():
            self.part_info = (self.part_num_box.get(), self.brand_var.get(),
                              self.description_box.get(), self.oem_box.get(),
                              str(bool(self.do_not_sub_var.get())).upper(),
                              str(bool(self.subbed_var.get())).upper())
            if add_part("cpu", self.part_info) == "Done":
                messagebox.showinfo("Part Added",
                                    self.part_num_box.get().strip() +
                                    " has been added to the database.")

        self.add_button = tk.Button(self.sub_frame, text="Add",
                                    command=add_it)
        self.add_button.grid(column=1, row=9, sticky="EW")

    def change_dropdown(self, *args):
        """
        When a part type/table is selected from the dropdown
        all widgets are removed from sub_frame and appropriate
        method is called.
        """
        clear_widgets(self.sub_frame)
        if drop_down_var.get() in ["HDD", "SSD", "SSHD"]:
            clear_widgets(self.sub_frame)
            self.add_hdd()
        elif drop_down_var.get() == "MEM":
            clear_widgets(self.sub_frame)
            self.add_mem()
        elif drop_down_var.get() == "CPU":
            clear_widgets(self.sub_frame)
            self.add_cpu()


class RemovePartPage(tk.Frame):
    """
    Displays the GUI allowing users to remove parts from the
    database.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.title = "SubHunt | Remove Part"

        self.part_num_label = tk.Label(self, text="Enter Part Number: ")
        self.part_num_label.grid(column=0, row=0)

        self.part_num_box = tk.Entry(self)
        self.part_num_box.grid(column=1, row=0)

        self.part_type_var = tk.StringVar()
        self.part_type_var.set("HDD")
        self.part_types = ["HDD", "MEM", "CPU"]

        self.part_type_drop = tk.OptionMenu(self, self.part_type_var,
                                            *self.part_types)
        self.part_type_drop.grid(column=3, row=0)

        self.remove_button = tk.Button(self, text="Remove",
                                       command=self.remove_it)
        self.remove_button.grid(column=4, row=0)

    def remove_it(self):
        """
        Retreives table and part_num field data and uses it
        to call remove_part.
        """
        self.part_num = self.part_num_box.get().strip()
        self.table = self.part_type_var.get()
        if (self.part_num != "" and part_in_db(self.table, self.part_num) and
                remove_part(self.table, self.part_num) == "Done"):
            messagebox.showinfo("Part Removed", self.part_num +
                                " removed successfuly.")
        elif self.part_num == "":
            messagebox.showerror("Invalid Entry",
                                 "Please enter a part number.")
        elif not part_in_db(self.table, self.part_num):
            messagebox.showerror("Invalid Entry",
                                 self.part_num +
                                 " does not exist in the database.")


class EditPartPage(tk.Frame):
    """
    Displays GUI allowing the user to edit details of a record
    already in the database.
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.container = tk.Frame(self)
        self.container.grid(column=0, row=0, sticky="EW")
        self.sub_frame = tk.Frame(self)
        self.sub_frame.grid(column=0, row=1, sticky="EW")
        self.updated_part_dict = {}

        self.info_search_label = tk.Label(self.container,
                                          text="Enter Part Number: ")
        self.info_search_label.grid(column=0, row=0, sticky="EW")
        self.info_search_box = tk.Entry(self.container, text="")
        self.info_search_box.grid(column=1, row=0, sticky="EW")

        self.info_type_var = tk.StringVar()
        self.info_type_var.set("HDD")
        self.info_types = ("HDD", "MEM", "CPU")
        self.info_type_drop = tk.OptionMenu(self.container,
                                            self.info_type_var,
                                            *self.info_types)
        self.info_type_drop.grid(column=2, row=0, sticky="EW")

        self.info_search_button = tk.Button(self.container, text="Search",
                                            command=lambda:
                                            self.show_part_info(
                                                self.info_search_box.get()
                                                .strip()
                                                ))
        self.info_search_button.grid(column=3, row=0, sticky="EW")

        self.save_button = tk.Button(self.container, text="Save",
                                     command=lambda:
                                     self.save_it(self.updated_part_dict))
        self.save_button.grid(column=4, row=0, sticky="EW")

    def save_it(self, updated_info):
        """
        Creates of tuple of the dictionary passed to then uses that
        data to call update_part.

        :param updated_info: Dictionary with desired changes
        """
        self.part_info = tuple(value.get() for key, value
                               in updated_info.items())
        if update_part(self.info_type_var.get().lower(),
                       self.part_info) == "Done":
            messagebox.showinfo("Part Update",
                                self.info_search_box.get().strip() +
                                " has been updated.")

    def show_part_info(self, part_num):
        """
        Displays the part info in the GUI in a visually appealing
        way.  Will display an error message if the part passed to
        it is not in the database.
        """
        clear_widgets(self.sub_frame)
        self.table = self.info_type_var.get().lower()
        if part_num != "" and part_in_db(self.table, part_num):
            self.part_info = convert_to_dict(self.table, part_num)
            for row_num, key in enumerate(self.part_info):
                if key in ["do_not_sub", "subbed"]:
                    self.part_info[key] = str(self.part_info[key]).upper()

                if key == "part_num":
                    _ = tk.Entry(self.sub_frame)
                    _.grid(column=1, row=row_num, sticky="W")
                    _.insert(0, self.part_info[key])
                    _.config(state="disabled")
                    self.updated_part_dict["part_num"] = _
                elif key == "brand":
                    self.brand_var = tk.StringVar()
                    self.brand_var.set(self.part_info[key])
                    self.brands = ("Acer", "Asus", "CVO", "Dell",
                                   "Hewlett Packard", "Lenovo", "Samsung",
                                   "Sony", "Toshiba")
                    tk.OptionMenu(self.sub_frame, self.brand_var,
                                  *self.brands).grid(column=1, row=row_num,
                                                     sticky="W")
                    self.updated_part_dict["brand"] = self.brand_var
                elif key == "connector":
                    connector_var = tk.StringVar()
                    connector_var.set(self.part_info[key])
                    connectors = ("SATA", "m.2", "eMMC", "mSATA",
                                  "IDE", "proprietary")
                    tk.OptionMenu(self.sub_frame, connector_var,
                                  *connectors).grid(column=1, row=row_num,
                                                    sticky="W")
                    self.updated_part_dict["connector"] = connector_var
                elif key == "type":
                    self.type_var = tk.StringVar()
                    self.type_var.set(self.part_info[key])
                    self.types = ("HDD", "SSD", "SSHD")
                    tk.OptionMenu(self.sub_frame, self.type_var,
                                  *self.types).grid(column=1, row=row_num,
                                                    sticky="W")
                    self.updated_part_dict["type"] = self.type_var
                else:
                    _ = tk.Entry(self.sub_frame)
                    _.grid(column=1, row=row_num, sticky="W")
                    _.insert(0, self.part_info[key])
                    self.updated_part_dict[key] = _

                tk.Label(self.sub_frame, text=key).grid(column=0, row=row_num,
                                                        sticky="W")
        elif part_num == "":
            messagebox.showerror("Invalid Entry",
                                 "Please enter a part number.")
        elif not part_in_db(self.table, part_num):
            messagebox.showerror("Invalid Entry",
                                 part_num +
                                 " does not exist in the database.")


class SearchPage(tk.Frame):
    """
    Displays a GUI allowing users to search the database for a given
    record and display data for that record.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.title = "SubHunt | Find Part Info"

        self.container = tk.Frame(self)
        self.container.grid(column=0, row=0, sticky="EW")

        self.sub_frame = tk.Frame(self)
        self.sub_frame.grid(column=0, row=1, sticky="EW")

        self.info_search_label = tk.Label(self.container,
                                          text="Enter Part Number: ")
        self.info_search_label.grid(column=0, row=0, sticky="EW")

        self.info_search_box = tk.Entry(self.container, text="")
        self.info_search_box.grid(column=1, row=0, sticky="EW")

        self.info_type_var = tk.StringVar()
        self.info_type_var.set("HDD")
        self.info_types = ("HDD", "MEM", "CPU")

        self.info_type_drop = tk.OptionMenu(self.container,
                                            self.info_type_var,
                                            *self.info_types)
        self.info_type_drop.grid(column=2, row=0, sticky="EW")

        self.info_search_button = tk.Button(self.container, text="Search",
                                                command=lambda:
                                                self.show_part_info(
                                                self.info_search_box.get()
                                                .strip())
                                            )
        self.info_search_button.grid(column=3, row=0, sticky="EW")

    def show_part_info(self, part_num):
        """
        Displays data for part_num on the frame.  Will return an
        error message if part is not in the database.

        :param part_num: Part number to search for
        """
        clear_widgets(self.sub_frame)
        self.table = self.info_type_var.get().lower()
        if part_num != "" and part_in_db(self.table, part_num):
            self.part_dict = convert_to_dict(self.table, part_num)
            self.part_info = {
                key: value for key, value in self.part_dict.items()
                if value != ""
                }
            for row_num, key in enumerate(self.part_info):
                if key in ["do_not_sub", "subbed"]:
                    self.part_info[key] = str(self.part_info[key]).upper()
                tk.Label(self.sub_frame, text=key).grid(column=0, row=row_num,
                                                        sticky="W")
                tk.Label(self.sub_frame,
                         text=self.part_info[key]).grid(column=1, row=row_num,
                                                        sticky="W")
        elif part_num == "":
            messagebox.showerror("Invalid Entry",
                                 "Please enter a part number.")
        elif not part_in_db(self.table, part_num):
            messagebox.showerror("Invalid Entry", part_num +
                                 " does not exist in the database.")


class VerifySubsPage(tk.Frame):
    """Displays if two entered part numbers are valid subs."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.title = "SubHunt | Verify Subs"

        self.search_frame = tk.Frame(self)
        self.search_frame.grid(column=0, row=0, sticky="EW")

        self.part_num_label = tk.Label(self.search_frame,
                                       text="Enter Part Number")
        self.part_num_label.grid(column=0, row=0)

        self.part_num_box = tk.Entry(self.search_frame, text="")
        self.part_num_box.grid(column=1, row=0)

        self.other_part_label = tk.Label(self.search_frame,
                                         text="Enter Second Part")
        self.other_part_label.grid(column=0, row=1)

        self.other_part_box = tk.Entry(self.search_frame, text="")
        self.other_part_box.grid(column=1, row=1)

        self.subs_type_var = tk.StringVar()
        self.subs_type_var.set("HDD")
        self.subs_types = ("HDD", "MEM", "CPU")

        self.subs_type_drop = tk.OptionMenu(self.search_frame,
                                            self.subs_type_var,
                                            *self.subs_types)
        self.subs_type_drop.grid(column=0, row=2)

        self.subs_search_button = tk.Button(
            self.search_frame,
            text="Verify",
            command=lambda:
            self.verify_sub(
            self.subs_type_var.get().lower(),
            self.part_num_box.get().strip(),
            self.other_part_box.get()
            .strip())
            )
        self.subs_search_button.grid(column=1, row=2)

    def show_result(self, result):
        """
        Displays True or False depending on result.

        :param result: Boolean
        """
        if result:
            bg_color = "green"
        if not result:
            bg_color = "red"
        self.result_label = tk.Label(self.search_frame, text=str(result),
                                     bg=bg_color, font=24)
        self.result_label.grid(column=0, row=3, columnspan=2, sticky="NSEW")

    def verify_sub(self, table, part_num, other_part_num):
        """
        Calls is_valid_sub using table, part_num, and
        other_part_num and calls show_result with the result.

        :param table: Table in database
        :param part_num: Part number
        :param other_part_num: Part number to compare
        """
        if part_num and other_part_num:
            self.show_result(is_valid_sub(table, part_num, other_part_num))
        else:
            messagebox.showerror("All fields required",
                                 "Please enter data in both part number \
                                 fields.")


class FindSubsPage(tk.Frame):
    """
    Displays the matching subs for a given part number in the GUI.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.title = "SubHunt | Find Subs"

        self.search_frame = tk.Frame(self)
        self.search_frame.grid(column=0, row=0, sticky="EW")

        self.results = tk.Frame(self)
        self.results.grid(column=0, row=1, padx=20, pady=10, sticky="EW")

        self.subs_search_label = tk.Label(self.search_frame,
                                          text="Enter Part Number")
        self.subs_search_label.grid(column=0, row=0)

        self.subs_search_box = tk.Entry(self.search_frame, text="")
        self.subs_search_box.grid(column=1, row=0)

        self.subs_type_var = tk.StringVar()
        self.subs_type_var.set("HDD")
        self.subs_types = ("HDD", "MEM", "CPU")

        self.subs_type_drop = tk.OptionMenu(self.search_frame,
                                            self.subs_type_var,
                                            *self.subs_types)
        self.subs_type_drop.grid(column=2, row=0)

        self.subs_search_button = tk.Button(self.search_frame, text="Search",
                                                command=lambda:
                                                self.find_subs(self.subs_search_box.get()
                                                .strip())
                                            )
        self.subs_search_button.grid(column=3, row=0)

    def make_table(self, table, subs):
        """
        Displays list of a subs in a spreadsheet
        like manner.

        :param table: Name of database table
        :param part_num: Part number
        :param subs: List of parts matching specs
            of part_num
        """
        clear_widgets(self.results)
        if table == "hdd":
            headers = ["Brand", "Part Number", "Type", "Deminsions",
                       "Height", "Connector", "HDD (GB)", "SSD (GB)",
                       "Speed", "Subbed?"]
        elif table == "mem":
            headers = ["Brand", "Part Number", "Connector", "Capacity",
                       "Speed", "Subbed?"]
        elif table == "cpu":
            headers = ["Brand", "Part Number", "OEM", "Description",
                       "Subbed?"]

        self.widths = {}
        for col_num in enumerate(subs[0]):
            columns = []
            for sub in subs:
                columns.append(sub[col_num[0]])
                self.widths[col_num[0]] = max(len(element) for element in columns)
            self.label_width = max(self.widths[col_num[0]], len(headers[col_num[0]]))
            if self.widths[col_num[0]] < self.label_width:
                self.widths[col_num[0]] = self.label_width + 2

        for col, header in enumerate(headers):
            tk.Label(self.results, text=header,
                     width=self.widths[col],
                     justify="center").grid(column=col, row=0)

        for row, sub in enumerate(subs):
            if row % 2 == 0:
                bg_color = "snow3"
            else:
                bg_color = "snow2"

            if sub[-1] == "TRUE":
                fg_color = "green4"
            else:
                fg_color = "Red2"

            if sub[0] == "CVO":
                fg_color = "steelblue"

            for col, info in enumerate(sub):
                info_var = tk.StringVar()
                info_var.set(info)
                tk.Entry(self.results, width=self.widths[col] + 2,
                         textvariable=info_var,
                         readonlybackground=bg_color,
                         foreground=fg_color,
                         relief="flat", justify="center",
                         state="readonly").grid(column=col, row=row + 1,
                                                sticky="EW")

    def find_subs(self, part_num):
        """
        Finds subs for part_num in the database.
        Then calls make_table to display them.

        :param part_num: Part number to find subs for
        """
        self.table = self.subs_type_var.get().lower()
        if part_num != "" and part_in_db(self.table, part_num):
            subs = list_subs(self.table, part_num)
            if subs:
                self.make_table(self.table, subs)
        elif not part_in_db(self.table, part_num):
            messagebox.showerror("Invalid Entry",
                                 part_num +
                                 " does not exist in the database.")
