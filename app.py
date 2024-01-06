# -*- coding: utf-8 -*-
"""
Page Mage Panel App

"""

import panel as pn
import pandas as pd
import pymongo
import hvplot.pandas



"""
FUNCTIONS
"""
def create_client():
    client_str = "mongodb+srv://PageMageApp:3vc4u328TOrRBhmN@pagemage0.kwyg3z7.mongodb.net/"
    client = pymongo.mongo_client.MongoClient(client_str, server_api=pymongo.server_api.ServerApi('1'))
    return client

def get_user_list (): 
    cursor = collection_user.find()
    users = pd.DataFrame(list(cursor))
    out = [i for i in users['username']]
    out.append("")
    return out

def select_attribute (attribute):
    cursor = collection_shelf.find({},{attribute: 1})
    books = pd.DataFrame(list(cursor))
    out = [str(i) for i in books[attribute].unique()]
    out.append("")
    return out

def get_book_scores (book): 
    cursor = collection_shelf.find()
    df = pd.DataFrame(list(cursor))
    df = df.loc[df['Unique ID'] == book, ].copy()
    scores = df[['User', 'CharacterDevelopment', 'Setting', 'Plot', 'Prose', 'MagicNovelty', 'RatingOverall', 'UnweightedRating']]
    scores = scores.set_index('User')
    scores = scores.T
    scores['Balrog'] = scores.mean(axis=1)
    scores = scores.T
    return scores

def make_book_plot(book):
    cursor = collection_shelf.find()
    df = pd.DataFrame(list(cursor))
    df = df.loc[df['Unique ID'] == book, ].copy()
    scores = df[['User', 'CharacterDevelopment', 'Setting', 'Plot', 'Prose', 'MagicNovelty', 'RatingOverall', 'UnweightedRating']]
    scores = scores.set_index('User')
    scores = scores.T
    scores['Balrog'] = scores.mean(axis=1)
    return scores.hvplot(kind='bar')

def get_book_mtr (book): 
    cursor = collection_shelf.find()
    df = pd.DataFrame(list(cursor))
    df = df.loc[df['Unique ID'] == book, ].copy()
    mtr = df[['User', 'MtR1', 'MtR2', 'MtR3', 'MtR4']]
    mtr = mtr.set_index('User')
    return mtr

def get_user_book (user, book): 
    cursor = collection_shelf.find()
    df = pd.DataFrame(list(cursor))
    df = df.loc[(df['Unique ID'] == book) & (df['User'] == user), ]
    return df

def get_value(df, attribute, dtype):
    if len(df) > 0 : 
        value = df[attribute].iat[0]
    else: 
        value = None
    if value == None: 
        dtypes = {str: '', 
                  float: 0, 
                  }
        value = dtypes[dtype] #add appropriate filler for dtype
    elif dtype == float: 
        value = float(value)
    return value

def check_book_exists(user, edit_title, edit_author):
    book_id = "{}_{}".format(edit_title, edit_author)
    df = get_user_book(user, book_id)
    if len(df) > 0:
        return True
    else: 
        return False

def calc_overall_rating (chardev, setting, plot, prose, magnov):
    out = 0.26 * chardev + 0.26 * setting + 0.26 * plot + 0.11 * prose + 0.11 * magnov
    return out

def calc_progress (CurrentPage, PageLength):
    if PageLength == 0: 
        out = 0
    else: 
        out = CurrentPage / PageLength
    return out


def update_DB(user, edit_title, edit_author, edit_series, edit_genre, edit_subgenre, edit_interest, edit_status,
               edit_synopsis, edit_mtr1, edit_mtr2, edit_mtr3, edit_mtr4, 
               edit_currentpage, edit_pagelength, edit_yearpublished, edit_priority, edit_chardev, edit_setting, edit_plot,
               edit_prose, edit_magnov, edit_unwtrate, event):
           
        #update book
    collection_shelf.update_one(
   { 
      "Unique ID": f"{edit_title}_{edit_author}",
      "User": user
   },
   {
      "$set": {
         "Title": edit_title,
         "Author": edit_author,
         "Series": edit_series,
         "Genre": edit_genre,
         "SubGenre": edit_subgenre,
         "Synopsis": edit_synopsis,
         "CurrentPage": edit_currentpage,
         "PageLength": edit_pagelength,
         "Progress": calc_progress(edit_currentpage, edit_pagelength),
         "YearPublished": edit_yearpublished,
         "Status": edit_status,
         "Interest": edit_interest,
         "Priority": edit_priority,
         "CharacterDevelopment": edit_chardev,
         "Setting": edit_setting,
         "Plot": edit_plot,
         "Prose": edit_prose,
         "MagicNovelty": edit_magnov,
         "RatingOverall": calc_overall_rating(edit_chardev, edit_setting, edit_plot, edit_prose, edit_magnov),
         "UnweightedRating": edit_unwtrate,
         "MtR1": edit_mtr1,
         "MtR2": edit_mtr2,
         "MtR3": edit_mtr3,
         "MtR4": edit_mtr4
             }
          }
       );

    mark_sql.object = "Database Updated!"
    return None

def insert_DB(user_add, add_title, add_author, add_series, add_genre, add_subgenre, add_interest, add_status,
               add_synopsis, add_mtr1, add_mtr2, add_mtr3, add_mtr4, 
               add_currentpage, add_pagelength, add_yearpublished, add_priority, add_chardev, add_setting, add_plot,
               add_prose, add_magnov, add_unwtrate, event):
           
        #update book
    collection_shelf.insert_one(
   {
         "Title": add_title,
         "Author": add_author,
         "Series": add_series,
         "Genre": add_genre,
         "SubGenre": add_subgenre,
         "Synopsis": add_synopsis,
         "CurrentPage": add_currentpage,
         "PageLength": add_pagelength,
         "Progress": calc_progress(add_currentpage, add_pagelength),
         "YearPublished": add_yearpublished,
         "Status": add_status,
         "Interest": add_interest,
         "Priority": add_priority,
         "CharacterDevelopment": add_chardev,
         "Setting": add_setting,
         "Plot": add_plot,
         "Prose": add_prose,
         "MagicNovelty": add_magnov,
         "RatingOverall": calc_overall_rating(add_chardev, add_setting, add_plot, add_prose, add_magnov),
         "UnweightedRating": add_unwtrate,
         "MtR1": add_mtr1,
         "MtR2": add_mtr2,
         "MtR3": add_mtr3,
         "MtR4": add_mtr4, 
         "User": user_add,
         "Unique ID": f"{add_title}_{add_author}"
             }
       );

    mark_sql_add.object = "Database Updated!"
    return None

"""
ESTABLISH DB CONNECTIONS
"""
client = create_client()
db = client['pagemage']
collection_user = db['users']
collection_shelf = db['shelf']


"""
PANEL APP
"""

#CURRENT BOOK

select_book = pn.widgets.AutocompleteInput(name='Select Book', options=select_attribute( "Unique ID"), placeholder='Title_Author Key', restrict=True)

bind_scores = pn.bind(get_book_scores, book = select_book)
disp_scores = pn.pane.DataFrame(bind_scores)

bind_mtr = pn.bind(get_book_mtr, select_book)
disp_mtr = pn.pane.DataFrame(bind_mtr)

bind_plot = pn.bind(make_book_plot, select_book)
disp_plot = pn.panel(bind_plot, sizing_mode='stretch_width')


#EDIT BOOK
user = pn.widgets.AutocompleteInput(name='Select User', options = get_user_list(), placeholder="", restrict=True)
user_book = pn.widgets.AutocompleteInput(name='Select Book', options=select_attribute( "Unique ID"), placeholder='Title_Author Key', restrict=True)

bind_user_book = pn.bind(get_user_book, user=user, book=user_book)

disp_user_book = pn.pane.DataFrame(bind_user_book, index=False)



#Inputs with Value = selected book
edit_title = pn.widgets.AutocompleteInput(name='Edit Title', options=select_attribute( "Title"), value = pn.bind(get_value, df = bind_user_book, attribute="Title", dtype = str))
edit_author = pn.widgets.AutocompleteInput(name='Edit Author (Last, First)', options=select_attribute( "Author"), value = pn.bind(get_value, df = bind_user_book, attribute="Author", dtype = str))
edit_series = pn.widgets.AutocompleteInput(name='Edit Series', options=select_attribute( "Series"), value = pn.bind(get_value, df = bind_user_book, attribute="Series", dtype = str))
edit_genre = pn.widgets.AutocompleteInput(name='Edit Genre', options=select_attribute( "Genre"), value = pn.bind(get_value, df = bind_user_book, attribute="Genre", dtype = str))
edit_subgenre = pn.widgets.AutocompleteInput(name='Edit SubGenre', options=select_attribute( "SubGenre"), value = pn.bind(get_value, df = bind_user_book, attribute="SubGenre", dtype = str))
edit_interest = pn.widgets.AutocompleteInput(name='Edit Interest', options=select_attribute( "Interest"), value = pn.bind(get_value, df = bind_user_book, attribute="Interest", dtype = str))
edit_status = pn.widgets.AutocompleteInput(name='Edit Status', options=select_attribute( "Status"), value = pn.bind(get_value, df = bind_user_book, attribute="Status", dtype = str))


edit_synopsis = pn.widgets.TextInput(name='Edit Synopsis', value = pn.bind(get_value, df = bind_user_book, attribute="Synopsis", dtype = str))
edit_mtr1 = pn.widgets.TextInput(name='Edit Mount Rushmore 1', value = pn.bind(get_value, df = bind_user_book, attribute="MtR1", dtype = str))
edit_mtr2 = pn.widgets.TextInput(name='Edit Mount Rushmore 2', value = pn.bind(get_value, df = bind_user_book, attribute="MtR2", dtype = str))
edit_mtr3 = pn.widgets.TextInput(name='Edit Mount Rushmore 3', value = pn.bind(get_value, df = bind_user_book, attribute="MtR3", dtype = str))
edit_mtr4 = pn.widgets.TextInput(name='Edit Mount Rushmore 4', value = pn.bind(get_value, df = bind_user_book, attribute="MtR4", dtype = str))


edit_currentpage = pn.widgets.FloatInput(name='Edit Current Page', value = pn.bind(get_value, df = bind_user_book, attribute="CurrentPage", dtype = float))
edit_pagelength = pn.widgets.FloatInput(name='Edit Page Length', value = pn.bind(get_value, df = bind_user_book, attribute="PageLength", dtype = float))
edit_yearpublished = pn.widgets.FloatInput(name='Edit Year Published', value = pn.bind(get_value, df = bind_user_book, attribute="YearPublished", dtype = float))
edit_priority = pn.widgets.FloatInput(name='Edit Priority (1=low to 5=high)', value = pn.bind(get_value, df = bind_user_book, attribute="Priority", dtype = float), start=1, end=5)
edit_chardev = pn.widgets.FloatInput(name='Edit Character Development (1=low to 10=high)', value = pn.bind(get_value, df = bind_user_book, attribute="CharacterDevelopment", dtype = float), start=1, end=10)
edit_setting = pn.widgets.FloatInput(name='Edit Setting (1=low to 10=high)', value = pn.bind(get_value, df = bind_user_book, attribute="Setting", dtype = float), start=1, end=10)
edit_plot = pn.widgets.FloatInput(name='Edit Plot (1=low to 10=high)', value = pn.bind(get_value, df = bind_user_book, attribute="Plot", dtype = float), start=1, end=10)
edit_prose = pn.widgets.FloatInput(name='Edit Prose (1=low to 10=high)', value = pn.bind(get_value, df = bind_user_book, attribute="Prose", dtype = float), start=1, end=10)
edit_magnov = pn.widgets.FloatInput(name='Edit Magiv / Novelty (1=low to 10=high)', value = pn.bind(get_value, df = bind_user_book, attribute="MagicNovelty", dtype = float), start=1, end=10)
edit_unwtrate = pn.widgets.FloatInput(name='Edit Unweighted Rating (1=low to 10=high)', value = pn.bind(get_value, df = bind_user_book, attribute="UnweightedRating", dtype = float), start=1, end=10)


bind_edit_book = pn.bind(update_DB, user, edit_title, edit_author, edit_series, edit_genre, edit_subgenre, edit_interest, edit_status,
               edit_synopsis, edit_mtr1, edit_mtr2, edit_mtr3, edit_mtr4, 
               edit_currentpage, edit_pagelength, edit_yearpublished, edit_priority, edit_chardev, edit_setting, edit_plot,
               edit_prose, edit_magnov, edit_unwtrate) 

button_sql = pn.widgets.Button(name="Update Book", button_type = "primary")
mark_sql = pn.pane.Markdown(object = "")
button_sql.on_click(bind_edit_book)

#ADD A NEW BOOK
user_add = pn.widgets.AutocompleteInput(name='Select User', options = get_user_list(), placeholder="", restrict=True)

#Inputs 
add_title = pn.widgets.AutocompleteInput(name='Edit Title', options=select_attribute( "Title"), restrict=False)
add_author = pn.widgets.AutocompleteInput(name='Edit Author (Last, First)', options=select_attribute( "Author"), restrict=False)
add_series = pn.widgets.AutocompleteInput(name='Edit Series', options=select_attribute( "Series"), restrict=False)
add_genre = pn.widgets.AutocompleteInput(name='Edit Genre', options=select_attribute( "Genre"), restrict=False)
add_subgenre = pn.widgets.AutocompleteInput(name='Edit SubGenre', options=select_attribute( "SubGenre"), restrict=False)
add_interest = pn.widgets.AutocompleteInput(name='Edit Interest', options=select_attribute( "Interest"), restrict=False)
add_status = pn.widgets.AutocompleteInput(name='Edit Status', options=select_attribute( "Status"), restrict=False)


add_synopsis = pn.widgets.TextInput(name='Edit Synopsis')
add_mtr1 = pn.widgets.TextInput(name='Edit Mount Rushmore 1')
add_mtr2 = pn.widgets.TextInput(name='Edit Mount Rushmore 2')
add_mtr3 = pn.widgets.TextInput(name='Edit Mount Rushmore 3')
add_mtr4 = pn.widgets.TextInput(name='Edit Mount Rushmore 4')


add_currentpage = pn.widgets.FloatInput(name='Edit Current Page')
add_pagelength = pn.widgets.FloatInput(name='Edit Page Length')
add_yearpublished = pn.widgets.FloatInput(name='Edit Year Published')
add_priority = pn.widgets.FloatInput(name='Edit Priority (1=low to 5=high)', start=1, end=5)
add_chardev = pn.widgets.FloatInput(name='Edit Character Development (1=low to 10=high)', start=1, end=10)
add_setting = pn.widgets.FloatInput(name='Edit Setting (1=low to 10=high)', start=1, end=10)
add_plot = pn.widgets.FloatInput(name='Edit Plot (1=low to 10=high)', start=1, end=10)
add_prose = pn.widgets.FloatInput(name='Edit Prose (1=low to 10=high)', start=1, end=10)
add_magnov = pn.widgets.FloatInput(name='Edit Magiv / Novelty (1=low to 10=high)', start=1, end=10)
add_unwtrate = pn.widgets.FloatInput(name='Edit Unweighted Rating (1=low to 10=high)', start=1, end=10)


bind_add_book = pn.bind(insert_DB, user_add, add_title, add_author, add_series, add_genre, add_subgenre, add_interest, add_status,
               add_synopsis, add_mtr1, add_mtr2, add_mtr3, add_mtr4, 
               add_currentpage, add_pagelength, add_yearpublished, add_priority, add_chardev, add_setting, add_plot,
               add_prose, add_magnov, add_unwtrate) 

button_sql_add = pn.widgets.Button(name="Add Book", button_type = "primary")
mark_sql_add = pn.pane.Markdown(object = "")
button_sql_add.on_click(bind_add_book)


#ORGANIZE OUTPUT INTO TABS
tabs = pn.Tabs(("Current Book", pn.Column(select_book, disp_scores, disp_mtr, disp_plot)), 
               ("Edit Book", pn.Column(
                                   pn.Row(user, user_book), 
                                   pn.Row(disp_user_book ,),
                                   pn.Row(edit_title, edit_author, edit_series, edit_genre, edit_subgenre,), 
                                   pn.Row(edit_synopsis,), 
                                   pn.Row(edit_currentpage, edit_pagelength, edit_yearpublished, edit_status, edit_interest, edit_priority,),
                                   pn.Row(edit_chardev, edit_setting, edit_plot, edit_prose, edit_magnov, edit_unwtrate, ),
                                   pn.Row(edit_mtr1, edit_mtr2, edit_mtr3, edit_mtr4,),
                                   pn.Row(button_sql, mark_sql),
                                   )),
               ("Add Book", pn.Column(
                                   pn.Row(user_add), 
                                   pn.Row(add_title, add_author, add_series, add_genre, add_subgenre,), 
                                   pn.Row(add_synopsis,), 
                                   pn.Row(add_currentpage, add_pagelength, add_yearpublished, add_status, add_interest, add_priority,),
                                   pn.Row(add_chardev, add_setting, add_plot, add_prose, add_magnov, add_unwtrate, ),
                                   pn.Row(add_mtr1, add_mtr2, add_mtr3, add_mtr4,),
                                   pn.Row(button_sql_add, mark_sql_add),
                                   )),
                                   ).servable()






