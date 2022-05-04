# Zewen Lin
import tkinter as tk
import webbrowser
import web_scraper
import price_tracker

HEIGHT = 600
WIDTH = 800


# remove the main page(containing 4 buttons)
def forget_main_frame():
    button_1.grid_forget()
    button_2.grid_forget()
    button_3.grid_forget()
    button_4.grid_forget()


def website_info():
    forget_main_frame()


def download_pic():
    forget_main_frame()


# job searching
def search_job():
    forget_main_frame()

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
    url_label = tk.Label(root, text="URL:  ", font=('Railway', 16))
    url_label.grid(row=1, column=1, sticky="NE", pady=5)
    # url_label.place(relx=0.1, rely=0.3, relwidth=0.2, relheight=0.2)

    # display website url input box
    url_box = tk.Entry(root, font=('Railway', 18), width=22)
    url_box.insert(-1, default_url)
    url_box.grid(row=1, column=2, sticky="NW")
    # url_box.place(relx=0.3, rely=0.3, relwidth=0.5, relheight=0.2)

    # display category label
    category_label = tk.Label(root, text="Category:  ", font=('Railway', 16))
    category_label.grid(row=2, column=1, sticky="NE", pady=5)
    # category_label.place(relx=0.1, rely=0.55, relwidth=0.2, relheight=0.2)

    # display category input box
    category_box = tk.Entry(root, font=('Railway', 18), width=22)
    category_box.grid(row=2, column=2, sticky="NW")
    # category_box.place(relx=0.3, rely=0.55, relwidth=0.5, relheight=0.2)

    # display location label
    location_label = tk.Label(root, text="Location:  ", font=('Railway', 16))
    location_label.grid(row=3, column=1, sticky="NE", pady=5)
    # category_label.place(relx=0.1, rely=0.55, relwidth=0.2, relheight=0.2)

    # display location input box
    location_box = tk.Entry(root, font=('Railway', 18), width=22)
    location_box.grid(row=3, column=2, sticky="NW")

    search_text = tk.StringVar()
    # display search button
    button_search = tk.Button(root, textvariable=search_text, font=('Railway', 16), height=3, width=14,
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
    #display_job_frame.place(relx=0.1, rely=0.05, relwidth=0.7, relheight=0.9)
    display_link_frame = tk.Frame(root)
    display_link_frame.grid(row=1, column=4)

    S = tk.Scrollbar(display_job_frame)
    T = tk.Text(display_job_frame, height=40, width=80, font=("Railway", 16), bd=0, highlightthickness=0)
    S.pack(side=tk.RIGHT, fill=tk.Y)
    T.pack(side=tk.LEFT, fill=tk.Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
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
        full_text += "\n\n"
        T.insert(tk.END, full_text)
        link_label = tk.Label(display_link_frame, fg="blue", cursor="hand2", text=company_name[i])
        link_label.pack(pady=6)
        link_label.bind("<Button-1>", lambda e: callback(job_link[i]))


def show_price(item_title, index):
    price_track = price_tracker.PriceTracker(item_title)
    bestbuy, ebay = price_track.run()
    bestbuy_text = "BESTBUY: " + bestbuy[0] + ": " + bestbuy[1]
    eaby_text = "\nEABY:        " + ebay[0] + ": " + ebay[1]
    total_text = bestbuy_text + eaby_text

    # right_frame = tk.Frame(root, height=450, width=500)
    # right_frame.grid(row=1, column=4, rowspan=4, columnspan=2)

    bt = tk.Text(root, font=("Railway", 16), bd=0, highlightthickness=0)
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
    button_1 = tk.Button(root, textvariable=text_1, font=('Railway', 18), height=3, width=17,
                         highlightbackground="#20bebe",
                         fg="black", command=lambda: show_price(text_1.get(), 0))
    button_1.grid(row=1, column=0)

    text_2 = tk.StringVar()
    text_2.set("Xbox Series S(512GB)")
    button_2 = tk.Button(root, textvariable=text_2, font=('Railway', 18), height=3, width=17,
                         highlightbackground="#20bebe",
                         fg="black", command=lambda: show_price(text_2.get(), 1))
    button_2.grid(row=2, column=0)

    text_3 = tk.StringVar()
    text_3.set("Ipad pro 11-inch")
    button_3 = tk.Button(root, textvariable=text_3, font=('Railway', 18), height=3, width=17,
                         highlightbackground="#20bebe",
                         fg="black", command=lambda: show_price(text_3.get(), 2))
    button_3.grid(row=3, column=0)

    text_4 = tk.StringVar()
    text_4.set("AirPods(3rd gen)")
    button_4 = tk.Button(root, textvariable=text_4, font=('Railway', 18), height=3, width=17,
                         highlightbackground="#20bebe",
                         fg="black", command=lambda: show_price(text_4.get(), 3))
    button_4.grid(row=4, column=0)


root = tk.Tk()
root.title("Web Scraper Tool Box")
# root.configure()
root.geometry("800x600")

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
text_1 = tk.StringVar()
button_1 = tk.Button(root, textvariable=text_1, font=('Railway', 18), height=6, width=20, highlightbackground="#20bebe",
                     fg="white", command=lambda: website_info())
text_1.set("Article")
button_1.grid(row=1, column=1)

# button_1.place(relx=0.15, rely=0, relheight=0.2, relwidth=0.35)
text_2 = tk.StringVar()
button_2 = tk.Button(root, textvariable=text_2, font=('Railway', 18), height=6, width=20, highlightbackground="#20bebe",
                     fg="white", command=lambda: download_pic())
text_2.set("Download Picture")
button_2.grid(row=1, column=2)
# button_2.place(relx=0.6, rely=0, relheight=0.2, relwidth=0.35)

text_3 = tk.StringVar()
button_3 = tk.Button(root, textvariable=text_3, font=('Railway', 18), height=6, width=20, highlightbackground="#20bebe",
                     fg="white", command=lambda: price_tracker_gui())
text_3.set("Price Tracker")
button_3.grid(row=2, column=1)
# button_3.place(relx=0.15, rely=0.3, relheight=0.2, relwidth=0.35)

text_4 = tk.StringVar()
button_4 = tk.Button(root, textvariable=text_4, font=('Railway', 18), height=6, width=20, highlightbackground="#20bebe",
                     fg="white", command=lambda: search_job())
text_4.set("Search Job")
button_4.grid(row=2, column=2)
# button_4.place(relx=0.6, rely=0.3, relheight=0.2, relwidth=0.35)

root.mainloop()
