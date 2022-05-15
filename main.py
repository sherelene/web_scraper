# Zewen Lin
import os
from tkinter import *
import tkinter as tk
import urllib
import webbrowser
import nltk
from newspaper import Article
import web_scraper
import price_tracker
import textwrap

from gtts import gTTS
from PIL import Image, ImageTk

HEIGHT = 600
WIDTH = 800
FONT = "Helvetica"


# remove the main page(containing 4 buttons) and the previous frames after clicking the back button
def forget_main_frame(button_1, button_2, button_3, button_4, display_job_frame):
    button_1.grid_forget()
    button_2.grid_forget()
    button_3.grid_forget()
    button_4.grid_forget()
    display_job_frame.grid_forget()



# text to speech function.
# parameters are strings
def text_to_speech(text):
    language = 'en'
    speech = gTTS(text=text, lang=language, slow=False)
    speech.save("text.mp3")
    os.system("start text.mp3")


# -------------------------------------ARTICLE STUFF----------------------------------------------------------#

def download_article(button1, button2, button3, button4, display_job_frame):
    forget_main_frame(button1, button2, button3, button4, display_job_frame)

    default_url = "https://www.cnn.com/2022/04/26/investing/markets-plunge-tech-down/index.html"

    search_box_frame = tk.Frame(root)
    search_box_frame.place(relx=0.5, rely=0.2, relwidth=0.8, relheight=0.5, anchor='n')

    # display website url label
    url_label = tk.Label(search_box_frame, text="ENTER URL:", font=('Helvetica', 22))
    url_label.place(relx=0.1, rely=0.3, relwidth=0.2, relheight=0.2)

    # display website url input box
    url_box = tk.Entry(search_box_frame, font=(FONT, 18))
    url_box.insert(-1, default_url)
    url_box.place(relx=0.3, rely=0.3, relwidth=0.6, relheight=0.4)

    # display search button
    button_search = tk.Button(search_box_frame, text="Search", font=(FONT, 18), bg="#3f3f3f", fg='white',
                              command=lambda: [url_label.place_forget(), url_box.place_forget(),
                                               button_search.place_forget(), search_box_frame.place_forget(),
                                               display_article(url_box.get())])
    button_search.place(relx=0.38, rely=0.75, relheight=0.2, relwidth=0.2)


def display_article(url):
    article = Article(url)

    # Do some NLP
    article.download()  # Downloads the link’s HTML content
    article.parse()  # Parse the article
    nltk.download('punkt')  # 1 time download of the sentence tokenizer
    article.nlp()  # Keyword extraction wrapper

    display_job_frame = tk.Frame(root)
    display_job_frame.place(relx=0.2, rely=0.05, relwidth=0.9, relheight=0.9)

    # information scraped from the article
    authors = ",".join(article.authors)
    date = article.publish_date
    text = article.text
    title = article.title
    # summ = article.summary.replace('\n', ' ').replace(u'\u2019', "\'")
    summ = textwrap.dedent(article.summary).strip()
    meta = article.meta_description
    image = article.top_image
    multi_images = article.images

    # information scarped from the article turned into a text block
    summary_text = "Author(s): " + str(authors) + "\nDate Published: " + str(date) + "\nArticle Name: " + str(title) + \
                   "\nArticle sypnosis: " + str(meta) + "\nArticle summary: " + str(summ)

    S = tk.Scrollbar(display_job_frame, orient=VERTICAL)
    T = tk.Text(display_job_frame, height=40, width=80, yscrollcommand=S.set, font=("Helvetica", 20), wrap=WORD)
    S.pack(side=tk.RIGHT, fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    T.insert(tk.END, "Author(s): \n")
    T.insert(tk.END, authors)
    T.insert(tk.END, "\n\nDate Published: \n")
    T.insert(tk.END, date)
    T.insert(tk.END, "\n\nArticle Name: \n")
    T.insert(tk.END, title)
    T.insert(tk.END, "\n\nArticle sypnosis:\n")
    T.insert(tk.END, meta)
    T.insert(tk.END, "\n\nArticle summary:\n")
    T.insert(tk.END, summ)

    file_path = download_image(image)  # downloads all images found in article

    # ========title frame===========#
    bg_color = "#323a45"
    text_area_bg = "#e1f3f8"
    basic_font_color = "#ffffff"  # "#ccc4c4"

    display_buttons = tk.Frame(root)
    display_buttons.place(relx=0.0, rely=0.05, relwidth=0.2, relheight=0.9)


    F1 = LabelFrame(display_buttons, text="Category", font=(
        "helvetica", 20, "bold"), bg=bg_color, fg=basic_font_color, bd=10, relief=GROOVE)
    F1.place(x=0, y=0, width=380, relheight=1)


    # button to read summary
    text_talk = tk.StringVar()
    text_talk.set("PLAY SUMMARY")
    b1 = tk.Button(F1, textvariable=text_talk, font=('Helvetica', 18), width=17, bd=7,
                           highlightbackground="#20bebe", fg="black", command=lambda: text_to_speech(summ))
    b1.grid(row=1, column=0, padx=10, pady=5)

    # button to read article
    article_talk = tk.StringVar()
    article_talk.set("PLAY ARTICLE")
    b2 = tk.Button(F1, textvariable=article_talk, font=('Helvetica', 18), width=17, bd=7,
                           highlightbackground="#20bebe", fg="black", command=lambda: text_to_speech(text))
    b2.grid(row=2, column=0, padx=10, pady=5)

    # button to show top image
    image_button = tk.StringVar()
    image_button.set("SHOW IMAGE")
    b3 = tk.Button(F1, textvariable=image_button, font=('Helvetica', 18), width=17, bd=7,
                   highlightbackground="#20bebe", fg="black", command=lambda: display_image(file_path))
    b3.grid(row=3, column=0, padx=10, pady=5)

    # button to read summary
    summary_button = tk.StringVar()
    summary_button.set("SUMMARY")
    b0 = tk.Button(F1, textvariable=summary_button, font=('Helvetica', 18), width=17, bd=7,
                   highlightbackground="#20bebe", fg="black", command=lambda: display_summary(authors, date, title,
                                                                                              meta, summ))
    b0.grid(row=0, column=0, padx=10, pady=5)

    # button to return to main page
    back_button = tk.StringVar()
    back_button.set("BACK TO MAIN")
    bb = tk.Button(F1, textvariable=back_button, font=('Helvetica', 18), width=17, bd=7,
                   highlightbackground="#20bebe", fg="black", command=lambda: return_main(root))
    bb.grid(row=6, column=0, padx=10, pady=5)


def display_image(image_file):

    display_job_frame = tk.Frame(root)
    display_job_frame.place(relx=0.2, rely=0.05, relwidth=0.9, relheight=0.9)

    load = Image.open(image_file)
    S = tk.Scrollbar(display_job_frame, orient=VERTICAL)
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render
    img.place(relx=0.2, rely=0.05, relwidth=0.9, relheight=0.9)

def display_summary(authors, date, title, meta, summ):
    display_job_frame = tk.Frame(root)
    display_job_frame.place(relx=0.2, rely=0.05, relwidth=0.9, relheight=0.9)

    S = tk.Scrollbar(display_job_frame, orient=VERTICAL)
    T = tk.Text(display_job_frame, height=40, width=80, yscrollcommand=S.set, font=("Helvetica", 20), wrap=WORD)
    S.pack(side=tk.RIGHT, fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    T.insert(tk.END, "Author(s): \n")
    T.insert(tk.END, authors)
    T.insert(tk.END, "\n\nDate Published: \n")
    T.insert(tk.END, date)
    T.insert(tk.END, "\n\nArticle Name: \n")
    T.insert(tk.END, title)
    T.insert(tk.END, "\n\nArticle sypnosis:\n")
    T.insert(tk.END, meta)
    T.insert(tk.END, "\n\nArticle summary:\n")
    T.insert(tk.END, summ)


def download_image(images):
    # creates new folder for temp use
    newpath = r'C:\Users\shere\OneDrive\Documents\CPP\SP2022\CS2520\projectVersions\temp'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    cnt = 1  # keeps image names unique

    # changes directory to temp folder
    os.chdir(newpath)


    saved_filename = "0000000" + str(cnt) + ".jpg"
    urllib.request.urlretrieve(images, saved_filename)

    return saved_filename

# function to show images on screen
def show_image(path):
    im = Image.open(path)
    im.show()

# function to delete image
def delete_file(file_path):
    # deletes image
    os.remove(file_path)


# ---------------------------------------------------END ARTICLE-----------------------------------------#


# ---------------------------------------------------In Stock Alert-------------- -----------------------#
def instock_alert():
    return True


# ---------------------------------------------------END In Stock Alert----------------------------------#


# ---------------------------------------------------Job Search--------------------------------- --------#
def search_job(button1, button2, button3, button4, display_job_frame):
    forget_main_frame(button1, button2, button3, button4, display_job_frame)

    default_url = "https://www.timesjobs.com/"

    # canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    # canvas.grid(columnspan=4, rowspan=4)
    # canvas.configure(highlightthickness=0)

    for i in range(5):
        # root.columnconfigure(i, weight=1)
        root.rowconfigure(i, weight=1)

    # search_box_frame = tk.Frame(root)
    # search_box_frame.place(relx=0.5, rely=0.2, relwidth=0.8, relheight=0.5, anchor='n')

    # display website url label
    url_label = tk.Label(root, text="URL:  ", font=(FONT, 22), bg="white")
    url_label.grid(row=1, column=1, sticky="NE", pady=5)
    # url_label.place(relx=0.1, rely=0.3, relwidth=0.2, relheight=0.2)

    # display website url input box
    url_box = tk.Entry(root, font=(FONT, 24), width=33, bg="white")
    url_box.insert(-1, default_url)
    url_box.grid(row=1, column=2, sticky="NW")
    # url_box.place(relx=0.3, rely=0.3, relwidth=0.5, relheight=0.2)

    # display category label
    category_label = tk.Label(root, text="Category:  ", font=(FONT, 22), bg="white")
    category_label.grid(row=2, column=1, sticky="NE", pady=5)
    # category_label.place(relx=0.1, rely=0.55, relwidth=0.2, relheight=0.2)

    # display category input box
    category_box = tk.Entry(root, font=(FONT, 24), width=33, bg="white")
    category_box.grid(row=2, column=2, sticky="NW")
    # category_box.place(relx=0.3, rely=0.55, relwidth=0.5, relheight=0.2)

    # display location label
    location_label = tk.Label(root, text="Location:  ", font=(FONT, 22), bg="white")
    location_label.grid(row=3, column=1, sticky="NE", pady=5)
    # category_label.place(relx=0.1, rely=0.55, relwidth=0.2, relheight=0.2)

    # display location input box
    location_box = tk.Entry(root, font=(FONT, 24), width=33, bg="white")
    location_box.grid(row=3, column=2, sticky="NW")

    search_text = tk.StringVar()
    # display search button
    button_search = tk.Button(root, textvariable=search_text, font=(FONT, 22), height=3, width=14,
                              highlightbackground="#20bebe", fg="black",
                              command=lambda: [url_label.grid_forget(), url_box.grid_forget(),
                                               category_label.grid_forget(), category_box.grid_forget(),
                                               button_search.grid_forget(),
                                               display_job(url_box.get(), category_box.get(), location_box.get())])
    search_text.set("Search")
    # button_search.place(relx=0.38, rely=0.75, relheight=0.2, relwidth=0.2)
    button_search.grid(row=4, column=2, sticky="NW")


def callback(url):
    webbrowser.open_new(url)


def display_job(url, category, location):
    ws = web_scraper.WebScraper(url, category, location)
    company_name, skills, job_link, years, locations = ws.run()
    display_job_frame = tk.Frame(root)
    display_job_frame.grid(row=1, column=1)
    # display_job_frame.place(relx=0.1, rely=0.05, relwidth=0.7, relheight=0.9)
    display_link_frame = tk.Frame(root)
    display_link_frame.grid(row=1, column=4)

    S = tk.Scrollbar(display_job_frame)
    T = tk.Text(display_job_frame, height=40, width=80, font=("FONT", 22), bd=0, highlightthickness=0, wrap=WORD)
    S.pack(side=tk.RIGHT, fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)

    # creates horizontal line for separeting job listings
    horizontalLine = '\u2500' * 20

    for i in range(len(company_name)):
        full_text = ""
        full_text += "Company: "
        full_text += company_name[i]
        full_text += "\n"
        full_text += "Skills: "
        full_text += skills[i]
        full_text += "\n"
        full_text += "Experience: "
        full_text += years[i][0]
        full_text += "\n"
        full_text += "Location: "
        full_text += locations[i]
        full_text += "\n"
        full_text += horizontalLine
        full_text += "\n"
        T.insert(tk.END, full_text)
        link_label = tk.Label(display_link_frame, fg="blue", cursor="hand2", text=company_name[i], font=(FONT, 24))
        link_label.pack(pady=6)
        link_label.bind("<Button-1>", lambda e: callback(job_link[i]))

# ---------------------------------------------------END Job Search-----------------------------------------#


# ---------------------------------------------------Price Tracker-----------------------------------------#
def show_price(item_title, index):
    price_track = price_tracker.PriceTracker(item_title)
    bestbuy, ebay = price_track.run()
    bestbuy_text = "BESTBUY: " + bestbuy[0] + ": " + bestbuy[1]
    eaby_text = "\nEABY:        " + ebay[0] + ": " + ebay[1]
    total_text = bestbuy_text + eaby_text

    # right_frame = tk.Frame(root, height=450, width=500)
    # right_frame.grid(row=1, column=4, rowspan=4, columnspan=2)

    bt = tk.Text(root, font=("FONT", 16), bd=0, highlightthickness=0)
    bt.insert(tk.END, total_text)
    if index == 0:
        bt.place(relx=0.3, rely=0.1, relheight=0.15, relwidth=0.7)
    elif index == 1:
        bt.place(relx=0.3, rely=0.25, relheight=0.15, relwidth=0.7)
    elif index == 2:
        bt.place(relx=0.3, rely=0.42, relheight=0.15, relwidth=0.7)
    elif index == 3:
        bt.place(relx=0.3, rely=0.6, relheight=0.15, relwidth=0.7)
    # bt.grid(row=2, column=4, rowspan=4, columnspan=4)


def price_tracker_gui():
    forget_main_frame()

    # canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH + 200)
    # canvas.grid()
    # canvas.configure(highlightthickness=0, bg="black")
    for i in range(10):
        root.columnconfigure(i, weight=1)
        root.rowconfigure(i, weight=1)

    text_1 = tk.StringVar()
    text_1.set("Nikon Z5")
    button_1 = tk.Button(root, textvariable=text_1, font=('FONT', 18), height=3, width=17,
                         highlightbackground="#20bebe",
                         fg="black", command=lambda: show_price(text_1.get(), 0))
    button_1.grid(row=1, column=0)

    text_2 = tk.StringVar()
    text_2.set("Xbox Series S(512GB)")
    button_2 = tk.Button(root, textvariable=text_2, font=('FONT', 18), height=3, width=17,
                         highlightbackground="#20bebe",
                         fg="black", command=lambda: show_price(text_2.get(), 1))
    button_2.grid(row=2, column=0)

    text_3 = tk.StringVar()
    text_3.set("Ipad pro 11-inch")
    button_3 = tk.Button(root, textvariable=text_3, font=('FONT', 18), height=3, width=17,
                         highlightbackground="#20bebe",
                         fg="black", command=lambda: show_price(text_3.get(), 2))
    button_3.grid(row=3, column=0)

    text_4 = tk.StringVar()
    text_4.set("AirPods(3rd gen)")
    button_4 = tk.Button(root, textvariable=text_4, font=('FONT', 18), height=3, width=17,
                         highlightbackground="#20bebe",
                         fg="black", command=lambda: show_price(text_4.get(), 3))
    button_4.grid(row=4, column=0)


# ---------------------------------------------------END Price Tracker-----------------------------------------#

#------------------------------------------ MAIN PAGE AGAIN FOR BACK BUTTON-----------------------------------------#
def return_main(root):
    display_job_frame = tk.Frame(root)
    display_job_frame.place(relx=0, rely=0, relwidth=1, relheight=1)


    # frame = tk.Frame(root)
    # frame.grid()
    # frame.place(relx=0.45, rely=0.25, relwidth=0.75, relheight=0.8, anchor='n')

    fontColor = "white"
    bgColor = "#EBF7E3"
    font = "Helvetica"

    text_1 = tk.StringVar()
    button_1 = tk.Button(root, textvariable=text_1, font=(font, 22, "bold"), height=6, width=20,
                         bg="#155a69",
                         fg=fontColor, command=lambda: download_article(button_1, button_2, button_3, button_4, display_job_frame))
    text_1.set("Article")
    button_1.grid(row=1, column=1)

    # button_1.place(relx=0.15, rely=0, relheight=0.2, relwidth=0.35)
    text_2 = tk.StringVar()
    button_2 = tk.Button(root, textvariable=text_2, font=(font, 22, "bold"), height=6, width=20,
                         bg="#2bb5d3",
                         fg=fontColor, command=lambda: instock_alert())
    text_2.set("In Stock Alert")
    button_2.grid(row=1, column=2)
    # button_2.place(relx=0.6, rely=0, relheight=0.2, relwidth=0.35)

    text_3 = tk.StringVar()
    button_3 = tk.Button(root, textvariable=text_3, font=(font, 22, "bold"), height=6, width=20,
                         bg="#95dae9",
                         fg="black", command=lambda: price_tracker_gui())
    text_3.set("Price Tracker")
    button_3.grid(row=2, column=1)
    # button_3.place(relx=0.15, rely=0.3, relheight=0.2, relwidth=0.35)

    text_4 = tk.StringVar()
    button_4 = tk.Button(root, textvariable=text_4, font=(font, 22, "bold"), height=6, width=20,
                         bg="black",
                         fg=fontColor, command=lambda: search_job(button_1, button_2, button_3, button_4, display_job_frame))
    text_4.set("Search Job")
    button_4.grid(row=2, column=2)
    # button_4.place(relx=0.6, rely=0.3, relheight=0.2, relwidth=0.35)

    root.mainloop()

#---------------------------------- END MAIN PAGE AGAIN FOR BACK BUTTON-----------------------------------------#


#---------------------------------- BEGIN ORIGNAL MAIN PAGE----------------------------------------#


root = tk.Tk()
root.title("Web Scraper Tool Box")
# root.configure()
root.geometry("800x600")
root.configure(bg='white')

# canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
# canvas.grid(columnspan=4, rowspan=4)
# canvas.configure(highlightthickness=0)

for i in range(4):
    root.columnconfigure(i, weight=1)
    root.rowconfigure(i, weight=1)

#
# frame = tk.Frame(root)
# frame.grid()
# frame.place(relx=0.45, rely=0.25, relwidth=0.75, relheight=0.8, anchor='n')

fontColor = "white"
bgColor = "#EBF7E3"
font = "Helvetica"

display_null = tk.Frame(root)

text_1 = tk.StringVar()
button_1 = tk.Button(root, textvariable=text_1, font=(font, 22, "bold"), height=6, width=20,
                     bg="#155a69",
                     fg=fontColor, command=lambda: download_article(button_1, button_2, button_3, button_4, display_null))
text_1.set("Article")
button_1.grid(row=1, column=1)

# button_1.place(relx=0.15, rely=0, relheight=0.2, relwidth=0.35)
text_2 = tk.StringVar()
button_2 = tk.Button(root, textvariable=text_2, font=(font, 22, "bold"), height=6, width=20,
                     bg="#2bb5d3",
                     fg=fontColor, command=lambda: instock_alert())
text_2.set("In Stock Alert")
button_2.grid(row=1, column=2)
# button_2.place(relx=0.6, rely=0, relheight=0.2, relwidth=0.35)

text_3 = tk.StringVar()
button_3 = tk.Button(root, textvariable=text_3, font=(font, 22, "bold"), height=6, width=20,
                     bg="#95dae9",
                     fg="black", command=lambda: price_tracker_gui())
text_3.set("Price Tracker")
button_3.grid(row=2, column=1)
# button_3.place(relx=0.15, rely=0.3, relheight=0.2, relwidth=0.35)

text_4 = tk.StringVar()
button_4 = tk.Button(root, textvariable=text_4, font=(font, 22, "bold"), height=6, width=20,
                     bg="black",
                     fg=fontColor, command=lambda: search_job(button_1, button_2, button_3, button_4, display_null))
text_4.set("Search Job")
button_4.grid(row=2, column=2)
# button_4.place(relx=0.6, rely=0.3, relheight=0.2, relwidth=0.35)

root.mainloop()
