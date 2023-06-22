# CTkTable Widget by Akascape
# License: MIT
# Author: Akash Bora

import customtkinter

class CTkTable(customtkinter.CTkFrame):
    """ CTkTable Widget """
    
    def __init__(
        self,
        master: any,
        row: int = None,
        column: int = None,
        padx: int = 1, 
        pady: int = 0,
        values: list = [[None]],
        colors: list = [None, None],
        color_phase: str = "horizontal",
        header_color: str = None,
        corner_radius: int = 25,
        hover_color: str = None,
        write: str = False,
        command = None,
        **kwargs):
        
        super().__init__(master, fg_color="transparent")

        self.master = master # parent widget
        self.rows = row if row else len(values) # number of default rows
        self.columns = column if column else len(values[0])# number of default columns
        self.padx = padx # internal padding between the rows/columns
        self.pady = pady
        self.command = command
        self.values = values # the default values of the table
        self.colors = colors # colors of the table if required
        self.header_color = header_color # specify the topmost row color
        self.phase = color_phase
        self.corner = corner_radius
        self.hover_color = hover_color
        self.write = write
        # if colors are None then use the default frame colors:
        self.data = {}
        self.fg_color = customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"] if not self.colors[0] else self.colors[0]
        self.fg_color2 = customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"] if not self.colors[1] else self.colors[1]

        if self.colors[0] is None and self.colors[1] is None:
            if self.fg_color==self.master.cget("fg_color"):
                self.fg_color = customtkinter.ThemeManager.theme["CTk"]["fg_color"]
            if self.fg_color2==self.master.cget("fg_color"):
                self.fg_color2 = customtkinter.ThemeManager.theme["CTk"]["fg_color"]
            
        self.frame = {}
        self.draw_table(**kwargs)
        
    def draw_table(self, **kwargs):

        """ draw the table """
        for i in range(self.rows):
            for j in range(self.columns):
                if self.phase=="horizontal":
                    if i%2==0:
                        fg = self.fg_color
                    else:
                        fg = self.fg_color2
                else:
                    if j%2==0:
                        fg = self.fg_color
                    else:
                        fg = self.fg_color2
                        
                if self.header_color:
                    if i==0:
                        fg = self.header_color
                        
                if not self.hover_color:
                    hover_color = fg
                    hover = False
                else:
                    hover_color = self.hover_color
                    hover = True
                    
                corner_radius = self.corner    
                if i==0 and j==0:
                    corners = ["", fg, fg, fg]
                elif i==self.rows-1 and j==self.columns-1:
                    corners = [fg ,fg, "", fg]
                elif i==self.rows-1 and j==0:
                    corners = [fg ,fg, fg, ""]
                elif i==0 and j==self.columns-1:
                    corners = [fg , "", fg, fg]
                else:
                    corners = [fg, fg, fg, fg]
                    corner_radius = 0
                    
                if self.values:
                    try:
                        value = self.values[i][j]
                    except IndexError: value = " "
                else:
                    value = " "

                if (i,j) in self.data.keys():
                    if self.data[i,j]["args"]: 
                        args = self.data[i,j]["args"]
                    else:
                        args = kwargs
                else:
                    args = kwargs
                    
                self.data[i,j] = {"row": i, "column" : j, "value" : value, "args": args }
              
                args = self.data[i,j]["args"]
                
                if self.write:
                    if self.padx==1: self.padx=0
                    self.frame[i,j] = customtkinter.CTkEntry(self,
                                                             corner_radius=0,
                                                             fg_color=fg, **args)
                    self.frame[i,j].insert("0", value)
                    self.frame[i,j].bind("<Key>", lambda e, row=i, column=j, data=self.data: self.after(100, lambda: self.manipulate_data(row, column)))
                    self.frame[i,j].grid(column=j, row=i, padx=self.padx, pady=self.pady, sticky="nsew")
                    if self.header_color:
                        if i==0:
                            self.frame[i,j].configure(state="readonly")
    
                else:
                    self.frame[i,j] = customtkinter.CTkButton(self, background_corner_colors=corners,
                                                              corner_radius=corner_radius, hover=hover,
                                                              fg_color=fg, hover_color=hover_color, text=value,
                                                              command=(lambda e=self.data[i,j]: self.command(e)) if self.command else None, **args)
                    self.frame[i,j].grid(column=j, row=i, padx=self.padx, pady=self.pady, sticky="nsew")
                
                self.rowconfigure(i, weight=1)
                self.columnconfigure(j, weight=1)
                
    def manipulate_data(self, row, column):
        """ entry callback """
        self.update_data()
        data = self.data[row,column]
        if self.command: self.command(data)
        
    def update_data(self):
        """ update the data when values are changes """
        for i in self.frame:
            if self.write:
                self.data[i]["value"]=self.frame[i].get()
            else:
                self.data[i]["value"]=self.frame[i].cget("text")

        self.values = []
        for i in range(self.rows):
            row_data = []
            for j in range(self.columns):
                row_data.append(self.data[i,j]["value"])
            self.values.append(row_data)
            
    def edit_row(self, row, **kwargs):
        """ edit all parameters of a single row """
        for i in range(self.columns):
            self.frame[row, i].configure(**kwargs)
            self.data[row, i]["args"] = kwargs
        self.update_data()
        
    def edit_column(self, column, **kwargs):
        """ edit all parameters of a single column """
        for i in range(self.rows):
            self.frame[i, column].configure(**kwargs)
            self.data[i, column]["args"] = kwargs
        self.update_data()
        
    def update_values(self, values, **kwargs):
        """ update all values at once """
        for i in self.frame.values():
            i.destroy()
        self.frame = {}
        self.values = values
        self.draw_table(**kwargs)
        self.update_data()
        
    def add_row(self, values, index=None, **kwargs):
        """ add a new row """
        for i in self.frame.values():
            i.destroy()
        self.frame = {}
        if index is None:
            index = len(self.values)      
        try:
            self.values.insert(index, values)
            self.rows+=1
        except IndexError: pass
    
        self.draw_table(**kwargs)
        self.update_data()
        
    def add_column(self, values, index=None, **kwargs):
        """ add a new column """
        for i in self.frame.values():
            i.destroy()
        self.frame = {}
        if index is None:
            index = len(self.values[0])
        x = 0
        for i in self.values:
            try:
                i.insert(index, values[x])
                x+=1
            except IndexError: pass
        self.columns+=1
        self.draw_table(**kwargs)
        self.update_data()
        
    def delete_row(self, index=None):
        """ delete a particular row """
        if index is None or index>=len(self.values):
            index = len(self.values)-1
        self.values.pop(index)
        for i in self.frame.values():
            i.destroy()
        self.rows-=1
        self.frame = {}
        self.draw_table()
        self.update_data()
        
    def delete_column(self, index=None):
        """ delete a particular column """
        if index is None or index>=len(self.values[0]):
            index = len(self.values)-1
        for i in self.values:
            i.pop(index)
        for i in self.frame.values():
            i.destroy()
        self.columns-=1
        self.frame = {}
        self.draw_table()
        self.update_data()
        
    def insert(self, row, column, value, **kwargs):
        """ insert value in a specific block [row, column] """
        if self.write:
            self.frame[row,column].delete(0, customtkinter.END)
            self.frame[row,column].insert(0, value)
            self.frame[row,column].configure(**kwargs)
        else:        
            self.frame[row,column].configure(text=value, **kwargs)
        if kwargs: self.data[row,column]["args"] = kwargs
        self.update_data()
        
    def delete(self, row, column, **kwargs):
        """ delete a value from a specific block [row, column] """
        if self.write:
            self.frame[row,column].delete(0, customtkinter.END)
            self.frame[row,column].configure(**kwargs)
        else:     
            self.frame[row,column].configure(text="", **kwargs)
        if kwargs: self.data[row,column]["args"] = kwargs
        self.update_data()
        
    def get(self, row=None, column=None):
        if row and column:
            return self.data[row,column]["values"]
        else:
            return self.values
    
    def configure(self, **kwargs):
        """ configure table widget attributes"""
        
        if "colors" in kwargs:
            self.colors = kwargs.pop("colors")
            self.fg_color = self.colors[0]
            self.fg_color2 = self.colors[1]
        if "header_color" in kwargs:
            self.header_color = kwargs.pop("header_color")
        if "rows" in kwargs:
            self.rows = kwargs.pop("rows")
        if "columns" in kwargs:
            self.columns = kwargs.pop("columns")
        if "values" in kwargs:
            self.values = kwargs.pop("values")
        if "padx" in kwargs:
            self.padx = kwargs.pop("padx")
        if "padx" in kwargs:
            self.pady = kwargs.pop("pady")
        
        self.update_values(self.values, **kwargs)
