# Zewen Lin
import tkinter as tk

import bs4
import time
import web_scraper
import nltk
from tkinter import *
from newspaper import Article
import tempfile
import urllib.request
from PIL import Image
import os

HEIGHT = 700
WIDTH = 800


# remove the main page(containing 4 buttons)
def forget_main_frame():
    button_1.place_forget()
    button_2.place_forget()
    frame.place_forget()


def website_info():
    forget_main_frame()


#-------------------------------------ARTICLE STUFF----------------------------------------------------------#
def download_article():
    forget_main_frame()

    default_url = "https://www.cnn.com/2022/04/26/investing/markets-plunge-tech-down/index.html"


    search_box_frame = tk.Frame(root)
    search_box_frame.place(relx=0.5, rely=0.2, relwidth=0.8, relheight=0.5, anchor='n')

    # display website url label
    url_label = tk.Label(search_box_frame, text="URL:", font=('Courier', 18))
    url_label.place(relx=0.1, rely=0.3, relwidth=0.2, relheight=0.2)

    # display website url input box
    url_box = tk.Entry(search_box_frame, font=('Courier', 18))
    url_box.insert(-1, default_url)
    url_box.place(relx=0.3, rely=0.3, relwidth=0.5, relheight=0.2)


    # display search button
    button_search = tk.Button(search_box_frame, text="Search", font=('Courier', 18),
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

    authors = ",".join(article.authors)
    date = article.publish_date
    text = article.text
    title = article.title
    summ = article.summary.replace('\n', ' ').replace(u'\u2019',"\'")
    meta = article.meta_description
    image = article.top_image
    multi_images = article.images
    print(multi_images)

    S = tk.Scrollbar(display_job_frame, orient=VERTICAL)
    T = tk.Text(display_job_frame, height=40, width=80, yscrollcommand=S.set, font=("Helvetica", 15))
    S.pack(side=tk.RIGHT, fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    T.insert(tk.END, "Author(s): ")
    T.insert(tk.END, authors)
    T.insert(tk.END, "\nDate Published: \n")
    T.insert(tk.END, date)
    T.insert(tk.END, "\n\nArticle Name: \n")
    T.insert(tk.END, title)
    T.insert(tk.END, "\n\nArticle sypnosis:\n")
    T.insert(tk.END, meta)
    T.insert(tk.END, "\n\nArticle summary:\n")
    T.insert(tk.END, summ)


    download_image(multi_images) #downloads all images found in article



def download_image(images):

    #creates new folder for temp use
    newpath = os.getcwd() + "\\temp"
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    cnt = 1 #keeps image names unique

    #changes directory to temp folder
    os.chdir(newpath)

    #saves all images in temp folder
    for image in images:
        saved_filename = "0000000" + str(cnt) + ".jpg"
        urllib.request.urlretrieve(image, saved_filename)
        cnt = cnt + 1
        show_image(saved_filename)

        # deletes image
        delete_file(saved_filename)



def show_image(path):
    from PIL import Image
    im = Image.open(path)
    im.show()



def delete_file(file_path):
    # deletes image
    os.remove(file_path)

#---------------------------------------------------END ARTICLE-----------------------------------------#


def search_job():
    forget_main_frame()

    default_url = "https://www.timesjobs.com/"

    search_box_frame = tk.Frame(root)
    search_box_frame.place(relx=0.5, rely=0.2, relwidth=0.8, relheight=0.5, anchor='n')

    # display website url label
    url_label = tk.Label(search_box_frame, text="URL:", font=('Courier', 18))
    url_label.place(relx=0.1, rely=0.3, relwidth=0.2, relheight=0.2)

    # display website url input box
    url_box = tk.Entry(search_box_frame, font=('Courier', 18))
    url_box.insert(-1, default_url)
    url_box.place(relx=0.3, rely=0.3, relwidth=0.5, relheight=0.2)

    # display category label
    category_label = tk.Label(search_box_frame, text="Category:", font=('Courier', 18))
    category_label.place(relx=0.1, rely=0.55, relwidth=0.2, relheight=0.2)

    # display category input box
    category_box = tk.Entry(search_box_frame, font=('Courier', 18))
    category_box.place(relx=0.3, rely=0.55, relwidth=0.5, relheight=0.2)

    # display search button
    button_search = tk.Button(search_box_frame, text="Search", font=('Courier', 18),
                              command=lambda: [url_label.place_forget(), url_box.place_forget(),
                                               category_label.place_forget(), category_box.place_forget(),
                                               button_search.place_forget(), search_box_frame.place_forget(),
                                               display_job(url_box.get(), category_box.get())])
    button_search.place(relx=0.38, rely=0.75, relheight=0.2, relwidth=0.2)


def display_job(url, category):
    ws = web_scraper.WebScraper(url, category)
    company_name, skills = ws.run()
    display_job_frame = tk.Frame(root)
    display_job_frame.place(relx=0.2, rely=0.05, relwidth=0.9, relheight=0.9)
    full_text = ""
    for i in range(len(company_name)):
        full_text += "Company Name: "
        full_text += company_name[i]
        full_text += "\n"
        full_text += "Skills: "
        full_text += skills[i]
        full_text += "\n\n"

    S = tk.Scrollbar(display_job_frame)
    T = tk.Text(display_job_frame, height=40, width=80)
    S.pack(side=tk.RIGHT, fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    T.insert(tk.END, full_text)


def in_stock_alert():
    forget_main_frame()


root = tk.Tk()
root.title("Web Scraper")

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = tk.Frame(root)
frame.place(relx=0.45, rely=0.25, relwidth=0.75, relheight=0.8, anchor='n')

title = Label(root, text="Web Scraper", font=('Courier', 17))
title.place(relx=0.5, rely=0.05, anchor=CENTER)
description = Label(root, text="Built to make article-viewing and job-searching more accessible.", font=('Courier', 13))
description.place(relx=0.5, rely=0.1, anchor=CENTER)

button_1 = tk.Button(frame, text="Article Search", font=('Courier', 17), command=lambda: download_article())
button_1.place(relx=0.15, rely=0.25, relheight=0.2, relwidth=0.35)
button_2 = tk.Button(frame, text="Job Search", font=('Courier', 17), command=lambda: search_job())
button_2.place(relx=0.6, rely=0.25, relheight=0.2, relwidth=0.35)


root.mainloop()

