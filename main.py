from tkinter import *
from tkinter import messagebox
import requests
import json
from newspaper import Article
import nltk

# download nltk packages for tokenization
nltk.download('punkt')


type = 'sports'
apiKey = 'YOUR_API_KEY_HERE'
BASE_URL = "https://github.com/sherelene"


class NewsApp:
    global apiKey, type

    def __init__(self, root):
        self.root = root
        self.root.geometry('1250x600+0+0')
        self.root.title("Web Organizer")

        # ====variables========#
        self.newsCatButton = []
        self.newsCat = ["general", "information",
                        "description", "article text", "video(s)", "images(s)"]



        # ========title frame===========#
        bg_color = "#323a45"
        text_area_bg = "#e1f3f8"
        basic_font_color = "#ffffff" #"#ccc4c4"
        title = Label(self.root, text="Web Organizer", font=("times new roman", 30, "bold"),
                      pady=2, bd=12, relief=GROOVE, bg=bg_color, fg=basic_font_color).pack(fill=X)

        F1 = LabelFrame(self.root, text="Category", font=(
            "times new roman", 20, "bold"), bg=bg_color, fg=basic_font_color, bd=10, relief=GROOVE)
        F1.place(x=0, y=80, width=300, relheight=0.88)


        b = Button(F1, text=self.newsCat[0].upper(
        ), width=20, bd=7, font="arial 15 bold")
        b.grid(row=0, column=0, padx=10, pady=5)
        b.bind('<Button-1>', self.Newsarea)
        self.newsCatButton.append(b)

        b2 = Button(F1, text=self.newsCat[1].upper(
        ), width=20, bd=7, font="arial 15 bold")
        b2.grid(row=1, column=0, padx=10, pady=5)
        b2.bind('<Button-1>', self.Newsarea)
        self.newsCatButton.append(b2)

        # =======news frame=======#
        font_color = "#212121"
        F2 = Frame(self.root, bd=7, relief=GROOVE)
        F2.place(x=320, y=80, relwidth=0.7, relheight=0.8)
        news_title = Label(F2, text="Content", font=(
            "arial", 20, "bold"), bd=7, relief=GROOVE).pack(fill=X)
        scroll_y = Scrollbar(F2, orient=VERTICAL)
        self.txtarea = Text(F2, yscrollcommand=scroll_y.set, font=(
            "arial", 15, "bold"), bg=text_area_bg, fg=font_color)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.txtarea.yview)
        self.txtarea.insert(
            END,
            "Enter web url here")
        self.txtarea.pack(fill=BOTH, expand=1)

    def Newsarea(self, event):
        url = "https://www.opensourceforu.com/2016/02/ionic-a-ui-framework-to-simplify-hybrid-mobile-app-development/"

        article = Article(url)

        # 1 . Download the article
        article.download()

        # 2. Parse the article
        article.parse()


        type = event.widget.cget('text').lower()
        BASE_URL = "https://github.com/sherelene"
        self.txtarea.delete("1.0", END)
        self.txtarea.insert(END, f"\n {article.authors}\n")
        self.txtarea.insert(
            END, "--------------------------------------------------------------------\n")

    def info(self, url):
        article = Article(url)

        # 1 . Download the article
        article.download()

        # 2. Parse the article
        article.parse()

        # 3. Fetch Author Name(s)
        self.article.authors

        # 4. Fetch Publication Date
        print('Article Publication Date:')
        print(article.publish_date)
        # 5. The URL of the Major Image
        print('Major Image in the article:')
        print(article.top_image)

        # 6. Natural Language Processing on Article to fetch Keywords
        article.nlp()
        print('Keywords in the article')
        print(article.keywords)

        # 7. Generate Summary of the article
        print('Article Summary')
        print(article.summary)


root = Tk()
obj = NewsApp(root)
root.mainloop()

