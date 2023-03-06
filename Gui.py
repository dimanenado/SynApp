import customtkinter
import requests

class SynApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # main window size, title and size limits
        self.geometry('600x420')
        self.title('SynApp')
        self.minsize(500, 300)

        # default appearance
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('blue')

        # creating grid
        self.grid_rowconfigure((1, 2), weight=1)
        self.grid_columnconfigure((1, 2, 3), weight=1)

        # adding left side labels for logo + text
        self.leftlabel1 = customtkinter.CTkLabel(master=self, text='   SynApp', font=('Roboto', 26), anchor='n')
        self.leftlabel1.grid(row=0, column=0, columnspan=1, padx=0, pady=(27, 0), sticky="nws")

        self.leftlabel2 = customtkinter.CTkLabel(master=self, text='_________ \n    simple\n    synonym\n    search',
                                                 font=('Roboto', 18), anchor='n', justify='left')
        self.leftlabel2.grid(row=1, column=0, columnspan=1, padx=0, pady=(0, 0), sticky="nws")

        # add search bar and bind enter to self.search()
        self.searchbar = customtkinter.CTkEntry(master=self, height=50, font=('Roboto', 22), border_width=0,
                                                corner_radius=5)
        self.searchbar.grid(row=0, column=1, columnspan=3, padx=(20, 0), pady=(20, 0), sticky='new')
        self.searchbar.bind('<Return>', lambda event: self.search())

        # add search button
        self.button = customtkinter.CTkButton(master=self, text='Search', font=('Roboto', 16), width=90, height=50,
                                              command=self.search)
        self.button.grid(row=0, column=4, padx=(5, 20), pady=(20, 0), sticky='ewn')

        # add label for output
        self.outputlabel = customtkinter.CTkLabel(master=self, text='', anchor='n', corner_radius=5,
                                                  font=('Roboto', 18), justify='left')
        self.outputlabel.grid(row=1, column=1, columnspan=4, rowspan=3, padx=(20, 20), pady=(20, 20), sticky="nswe")

    def search(self):
            word = self.searchbar.get().strip()
            self.outputlabel.configure(anchor='nw', text=f'input is: {word}')

if __name__ == "__main__":
    app = SynApp()
    app.mainloop()



