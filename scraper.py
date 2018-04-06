# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
from threading import Thread
import os
import time

import tkinter as tk
from tkinter import ttk
import simpleaudio as sa
import pyperclip

# defining the pop-up for a match
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)


def popupmsg(rate, username, stock, sellvalue, buyvalue, buy, buy_with):
    popup = tk.Tk()
    popup.title("Entry found!")
    popup.iconify()
    msg = ("@" + username + "Hi, I'd like to buy your " + sellvalue + " " + buy +
           " for my " + buyvalue + " " + buy_with + " in Bestiary.")
    label1 = ttk.Label(popup, text='Kurs: ' + rate, font=NORM_FONT)
    label2 = ttk.Label(popup, text='Stock: ' + stock, font=NORM_FONT)
    label3 = ttk.Label(popup, text=msg, font=NORM_FONT)
    label1.pack(side="top", fill="x", pady=10, padx=100)
    label2.pack(side="top", fill="x", pady=10, padx=100)
    label3.pack(side="top", fill="x", pady=10)

    button_copy = ttk.Button(popup, text="Copy", command=lambda: pyperclip.copy(msg))
    button_copy.pack()
    button_exit = ttk.Button(popup, text="Exit", command=popup.destroy)
    button_exit.pack()
    popup.mainloop()


def start_scraping(buy, buy_with, rate):
    # periodically check for offers lower than the specified rate
    while 1:
        # specify the url

        quote_page = ('http://currency.poe.trade/search?league=Bestiary&online=x&want=' + currency_id[buy] +
                      '&have=' + currency_id[buy_with])

        # query the website and return the html to variable 'page'
        page = urlopen(quote_page)

        # parse html using beautiful soup and store in variable 'soup'
        soup = BeautifulSoup(page, 'html.parser')

        offer_box = soup.find('div', attrs={'class': 'displayoffer'})

        username = offer_box['data-ign']
        sellvalue = offer_box['data-sellvalue']
        buyvalue = offer_box['data-buyvalue']
        minrate = str(float(buyvalue) / float(sellvalue))
        sellvalue = sellvalue.split('.')[0]  # cut before decimal point
        buyvalue = buyvalue.split('.')[0]  # cut before decimal point
        try:
            stock = offer_box['data-stock']
        except:
            stock = "No Stock information"
        if (minrate <= rate):
            wave_obj.play()
            popupmsg(minrate, username, stock, sellvalue, buyvalue, buy, buy_with)
            break
        time.sleep(2)


# .wav file
wave_obj = sa.WaveObject.from_wave_file("sound.wav")

# get currency names and its id's
currency_id = {}
currency_names = []
quote_page = 'http://currency.poe.trade/'
page = urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')

currency_boxes = soup.find('div', attrs={'class': 'selector-contents'}).\
    find_all('div', attrs={'class': 'currency-selectable'})

for box in currency_boxes:
    currency_names.append(box['data-title'])
    currency_id[box['data-title']] = box['data-id']

app = tk.Tk()
app.title("POE currency alert")

label_buy = ttk.Labelframe(app, text="Buy")
label_with = ttk.Labelframe(app, text="With")
label_rate = ttk.Labelframe(app, text="Rate")

buy = tk.StringVar()
buy.set("exalted")
list_buy = ttk.Combobox(label_buy, textvariable=buy, values=currency_names)
buy_with = tk.StringVar()
buy_with.set("chaos")
list_with = ttk.Combobox(label_with, textvariable=buy_with, values=currency_names)

list_buy.pack()
list_with.pack()

rate = tk.StringVar()
field_rate = tk.Entry(label_rate, textvariable=rate)
field_rate.pack()
label_rate.pack(in_=app, side="bottom", pady=5, padx=10)

button_start = ttk.Button(app, text="Start", command=lambda: Thread(target=start_scraping, args=(list_buy.get(), list_with.get(), field_rate.get())).start())
button_start.pack(side="bottom")
label_buy.pack(in_=app, side="left", pady=5, padx=10)
label_with.pack(in_=app, side="right", pady=5, padx=10)
button_quit = ttk.Button(app, text="Quit", command=lambda: os._exit(1))
button_quit.pack()

app.mainloop()
