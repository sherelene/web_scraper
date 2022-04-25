# Zewen Lin
import tkinter as tk
import web_scraper

HEIGHT = 700
WIDTH = 800


# remove the main page(containing 4 buttons)
def forget_main_frame():
    button_1.place_forget()
    button_2.place_forget()
    button_3.place_forget()
    button_4.place_forget()
    frame.place_forget()


def website_info():
    forget_main_frame()


def download_pic():
    forget_main_frame()


# job searching
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

button_1 = tk.Button(frame, text="Website Info", font=('Courier', 18), command=lambda: website_info())
button_1.place(relx=0.15, rely=0, relheight=0.2, relwidth=0.35)
button_2 = tk.Button(frame, text="Download Picture", font=('Courier', 18), command=lambda: download_pic())
button_2.place(relx=0.6, rely=0, relheight=0.2, relwidth=0.35)
button_3 = tk.Button(frame, text="In Stock Alert", font=('Courier', 18), command=lambda: in_stock_alert())
button_3.place(relx=0.15, rely=0.3, relheight=0.2, relwidth=0.35)
button_4 = tk.Button(frame, text="Search Job", font=('Courier', 18), command=lambda: search_job())
button_4.place(relx=0.6, rely=0.3, relheight=0.2, relwidth=0.35)

root.mainloop()
