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
        self.leftlabel1 = customtkinter.CTkLabel(master=self, text='SynApp', font=('Roboto', 26, 'bold'), anchor='n')
        self.leftlabel1.grid(row=0, column=0, columnspan=1, padx=20, pady=(27, 0), sticky="nws")

        self.leftlabel2 = customtkinter.CTkLabel(master=self, text='_________\nsimple\nsynonym\nsearch',
                                                 font=('Roboto', 18), anchor='n', justify='left')
        self.leftlabel2.grid(row=1, column=0, columnspan=1, padx=20, pady=(0, 0), sticky="nws")

        # add search bar and bind enter to self.search()
        self.searchbar = customtkinter.CTkEntry(master=self, height=50, font=('Roboto', 22), border_width=0,
                                                corner_radius=5)
        self.searchbar.grid(row=0, column=1, columnspan=3, padx=0, pady=(20, 0), sticky='new')
        self.searchbar.bind('<Return>', lambda event: self.search())

        # add search button
        self.button = customtkinter.CTkButton(master=self, text='Search', font=('Roboto', 18), width=90, height=50,
                                              command=self.search)
        self.button.grid(row=0, column=4, padx=(10, 20), pady=(20, 0), sticky='ewn')

        # add label for output
        welcome_text = 'Welcome to our synonym finder!\n\nTo get started:\n-- type a word or phrase into the search bar\n-- click the "Search" button\n\n\nHappy synonym hunting!'
        self.outputlabel = customtkinter.CTkLabel(master=self, text=welcome_text, anchor='nw', corner_radius=5,
                                                  font=('Roboto', 18), justify='left')
        self.outputlabel.grid(row=1, column=1, columnspan=4, rowspan=3, padx=(20, 20), pady=(22, 20), sticky="nswe")

    # input check
    def is_valid_input(self, word):
        allowed_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '-"
        if not word:
            return False
        return all(char in allowed_characters for char in word)

    # datamuse API request
    def generate_syn(self, word):
        datamuse_url = 'https://api.datamuse.com/words'
        datamuse_params = {'rel_syn': word,
                           'max': 10}
        # if space in input change params to ml - means like for better output
        if ' ' in word:
            datamuse_params = {'ml': word,
                             'max': 10}
        response = requests.get(datamuse_url, params = datamuse_params)
        # sanity check
        if response.status_code == 200:
            results = response.json()
            synonyms = [result['word'] for result in results]
            note = '\n\n**Found with Datamuse API'
            return synonyms, note   # return synonyms and a note str

        else:
            raise requests.exceptions.HTTPError('Bad request Datamuse :(')

    #Merriam-Webster request if generate_syn founds less than 3 synonyms
    def generate_more(self, word, synonyms):
        merriam_webster_url = f'https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}'
        merriam_webster_params = {'key': '49b6cc9c-f1e8-40c8-bce9-a4c28d2b334a'}
        merriam_webster_response = requests.get(merriam_webster_url, params=merriam_webster_params)
        #sanity check
        if merriam_webster_response.status_code == 200:
            merriam_webster_results = merriam_webster_response.json()
            note = '\n\n**Displaying list combined from multiple sources'
            for entry in merriam_webster_results:
                if 'meta' in entry and 'syns' in entry['meta']:
                    for syn_list in entry['meta']['syns']:
                        synonyms.extend(syn_list)
                        if len(synonyms) >= 10:
                            break
                    if len(synonyms) >=10:
                        break
            return synonyms[:10], note
        else:
            raise requests.exceptions.HTTPError('Bad request Merriam Webster :(')

    def search(self):
        word = self.searchbar.get().strip()

        try:
            if not self.is_valid_input(word):
                raise ValueError(f'Oops,{word} looks like invalid input: \n\nlets try something different')
            synonyms, note = self.generate_syn(word)
            if len(synonyms) < 3:
                synonyms, note = self.generate_more(word, synonyms)
            if synonyms:
                nld = '\n-- '  # both are workarounds for fstring backslash
                nl = '\n'
                self.outputlabel.configure(anchor='nw', text=f'Synonyms found for {word}:{nl}{nld}{nld.join(synonyms)}{note}', justify='left')
                self.searchbar.delete('0', '100')
            else:
                self.outputlabel.configure(anchor='nw', text='Oops, nothing found :(\n\nPlease try something else', justify='left')
                self.searchbar.delete('0', '100')
        except Exception as e:
            self.outputlabel.configure(anchor='nw', text=e)
            self.searchbar.delete('0', '100')

if __name__ == "__main__":
    app = SynApp()
    app.mainloop()



