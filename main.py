from tkinter import *
from goose3 import Goose


def info():
    article = Goose().extract(e1.get())
    title.set(article.title)
    meta.set(article.meta_description)
    string = article.cleaned_text[:150]
    art_dec.set(string.split("\n"))


if __name__ == '__main__':
    # var for URL
    url = "https://github.com/sherelene/web_scraper"

    # initialization with
    article = Goose().extract(url)

    print("Title of the article :\n", article.title)
    print("Meta information :\n", article.meta_description)
    print("Article Text :\n", article.cleaned_text[:300])


    # object of tkinter
    # and background set to grey
    master = Tk()
    master.configure(bg='LightBlue1')

    # Variable Classes in tkinter
    title = StringVar();
    meta = StringVar();
    art_dec = StringVar();

    # Creating label for each information
    # name using widget Label
    Label(master, text="Website URL : ",
          bg="LightBlue1", font=('Arial', 12)).grid(row=0, sticky=W)
    Label(master, text="Title :",
          bg="LightBlue1", font=('Arial', 12)).grid(row=3, sticky=W)
    Label(master, text="Meta information :",
          bg="LightBlue1", font=('Arial', 12)).grid(row=4, sticky=W)
    Label(master, text="Article description :",
          bg="LightBlue1", font=('Arial', 12)).grid(row=5, sticky=W)

    # Creating label for class variable
    # name using widget Entry
    Label(master, text="", textvariable=title,
          bg="LightBlue1", font=('Arial', 11)).grid(row=3, column=1, sticky=W)
    Label(master, text="", textvariable=meta,
          bg="LightBlue1", font=('Arial', 11)).grid(row=4, column=1, sticky=W)
    Label(master, text="", textvariable=art_dec,
          bg="LightBlue1", font=('Arial', 11)).grid(row=5, column=1, sticky=W)

    e1 = Entry(master, width=100)
    e1.grid(row=0, column=1)

    # creating a button using the widget
    # to call the submit function
    b = Button(master, text="Show", command=info, bg="light gray")
    b.grid(row=0, column=2, columnspan=1, rowspan=1, padx=4, pady=4, )

    mainloop()