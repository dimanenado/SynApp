import customtkinter
import requests
import logging

logging.basicConfig(filename='SynApp.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

class SynApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # main window size, title and size limits
        self.geometry('620x460')
        self.title('SynApp')
        self.minsize(620, 300)

        # default appearance
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('blue')

        # creating grid
        self.grid_rowconfigure((1, 2), weight=1)
        self.grid_columnconfigure((1, 2, 3), weight=1)

        # adding left side labels for logo + text
        self.leftlabel1 = customtkinter.CTkLabel(master=self, text='SynApp', font=('Roboto', 26, 'bold'), anchor='n')
        self.leftlabel1.grid(row=0, column=0, columnspan=1, padx=24, pady=(24, 0), sticky="w")

        self.leftlabel2 = customtkinter.CTkLabel(master=self, text='_________\nSimple\nSynonym\nSearch',
                                                 font=('Roboto', 18), anchor='n', justify='left')
        self.leftlabel2.grid(row=1, column=0, columnspan=1, padx=24, pady=(16, 0), sticky="nw")

        # add search bar and bind enter to self.search()
        self.searchbar = customtkinter.CTkEntry(master=self, height=48, font=('Roboto', 22), border_width=0,
                                                corner_radius=12)
        self.searchbar.grid(row=0, column=1, columnspan=3, padx=0, pady=(24, 0), sticky='new')
        self.searchbar.bind('<Return>', lambda event: self.search())

        # add search button
        self.button = customtkinter.CTkButton(master=self, text='Search', font=('Roboto', 18),  width=90, height=48, corner_radius=12, hover_color='#0078d7', command=self.search)
        self.button.grid(row=0, column=4, padx=(12, 24), pady=(24, 0), sticky='ewn')

        # add label for output
        welcome_text = 'Welcome to our synonym finder!\n\nTo get started:\n-- type a word or phrase into the search bar\n-- click the "Search" button\n\n\nHappy synonym hunting!'
        self.outputlabel = customtkinter.CTkTextbox(master=self, corner_radius=5,font=('Roboto', 18),border_spacing=12,
                                                    fg_color='#242424'
                                                    )
        self.outputlabel.grid(row=1, column=1, columnspan=4, rowspan=3, padx=(0, 12), pady=(24, 24), sticky="nswe")
        self.outputlabel.insert('0.0', welcome_text)

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
                           'max': 10,
                           'md': 'f'}
            #[Optional]if space in input change params to ml - 'means like' for better output
        if ' ' in word:
            datamuse_params = {'ml': word,
                               'max': 10}
            response = requests.get(datamuse_url, params=datamuse_params)
            logging.info(f'Datamuse request URL:{response.url}')
            # sanity check
            if response.status_code == 200:
                synonyms = [result['word'] for result in response.json()]
                note = '\n\n**Found with Datamuse API'
                logging.info(f'Datamuse sorted output is: {synonyms}')
                return synonyms, note
        response = requests.get(datamuse_url, params = datamuse_params)
        logging.info(f'Datamuse request URL:{response.url}')
        # sanity check
        if response.status_code == 200:
            logging.info(f'Datamuse response: {response}')
            results = sorted(response.json(), key=lambda x: float(x['tags'][0].split(':')[1]), reverse=True)
            synonyms = []
            for item in results:
                synonyms.append(item['word'])
            note = '\n\n**Found with Datamuse API'
            logging.info(f'Datamuse sorted output is: {synonyms}')
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
            logging.info(f'Merriam-Webster request URL:{merriam_webster_response.url}')
            merriam_webster_results = merriam_webster_response.json()
            note = '\n\n**Displaying list combined from multiple sources'
            for entry in merriam_webster_results:
                if 'meta' in entry and 'syns' in entry['meta']:
                    for syn_list in entry['meta']['syns']:
                        synonyms.extend(syn_list)
                        if len(synonyms) >= 10:
                            break
                    if len(synonyms) >= 10:
                        break
            logging.info(f'Result output is: {synonyms}')
            return synonyms[:10], note
        else:
            raise requests.exceptions.HTTPError('Bad request Merriam Webster :(')

    def search(self):
        word = self.searchbar.get().strip()
        logging.info('_____________STARTING NEW SEARCH_____________')
        logging.info(f'user input is:{word}')
        self.searchbar.delete('0', '100')

        try:
            if not self.is_valid_input(word):
                raise ValueError(f'Oops, {word} looks like invalid input: \n\nlets try something different')
            synonyms, note = self.generate_syn(word)
            if len(synonyms) < 3:
                synonyms, note = self.generate_more(word, synonyms)
                logging.warning(f'less than three synonyms found with Datamuse')
            if synonyms:
                nld = '\n-- '  # both are workarounds for fstring backslash
                nl = '\n'
                self.outputlabel.delete('0.0','20.0')
                self.outputlabel.insert(('0.0'), f'Synonyms found for {word}:{nl}{nld}{nld.join(synonyms)}{note}')

            else:
                logging.info(f'no synonyms found for {word}')
                self.outputlabel.delete('0.0', '20.0')
                self.outputlabel.insert(('0.0'), f'Oops, nothing found for {word} :(\n\nPlease try something else')

        except Exception as e:
            logging.error(f'exception caught: {e}')
            self.outputlabel.delete('0.0', '20.0')
            self.outputlabel.insert(('0.0'), f'{e}')



#create instance and start mainevent

if __name__ == "__main__":
    app = SynApp()
    app.mainloop()



