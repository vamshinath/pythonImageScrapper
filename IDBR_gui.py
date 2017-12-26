#!/usr/bin/python3
from tkinter import *
from tkinter import filedialog
from bs4 import BeautifulSoup as soup
from urllib.parse import urljoin
import os, re, requests, sys
import matplotlib.pyplot as plt
import signal,time
import webbrowser

chances = 5
pgno=0
# debg=open("debug_ImgScrap.txt","a")
def skip():
    global chances
    chances=5
    
    global pgno
    print("skipping {}".format(pgno))
    pgno+=1
    
    clicked()



def cleanup(path):
    os.chdir(path)
    print("Cleaning Up in:{}" + path)
    files = os.listdir()
    for fl in files:
        if os.stat(fl).st_size < 1500 and os.path.isfile(fl):
            os.remove(fl)


def download(urls, path):
    global label
    skp=1
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        #urls=urls.sort()
        for url in urls:
            if skp % 2 == 0:
                skp=skp+1
                continue
            url = re.sub('th_', '', url)
            filename = url.split('/')[-1]

            print("Downloading {}".format(url))

            data = requests.get(url)

            file = open(path + "/" + filename, "wb")
            for chunk in data.iter_content(chunk_size=2048):
                if chunk:
                    file.write(chunk)
            file.close()
            skp=skp+1
        label['text'] = "Downloading Completed"
        cleanup(path)
    except:
        label['text'] = "Downloading Failed !!"


def scrap(url, dirr):
    global label
    try:
        label['text'] = "Downloading....."
        page = requests.get(url)
        html = soup(page.text, "html.parser")
        images = html.findAll('img')
        imglinks = []
        for img in images:
            imglinks.append(urljoin(url, img.get("src")))
        # debg.write(urljoin(url,img.get("src"))+"\n")

        # debg.close
        imglinks = set(imglinks)
        download(imglinks, dirr)
    except:
        label['text'] = "Downloading Failed ,Please check URL !!"


def clicked():
    global chances
    global pgno
    global label
    if pgno == 0:
        url = entry_ln.get()
        label['text'] = "Downloading....."
        path = filedialog.askdirectory(title="Download to")
        pgno=int(re.sub(r'[A-Za-z]','',str(url.split("/")[-2])))
    actname=re.sub(r'[^A-Za-z]','',str(url.split("/")[-2]))
    url="http://www.idlebrain.com/movie/photogallery/"
    pgbk=pgno
    flag=0
    while chances > -1:
        page=requests.get(url+actname+str(pgno)+"/index.html")
        if page.status_code != 200:
            chances-=1
        else:
            #webbrowser.open(url+actname+str(pgno)+"/index.html")
            #time.sleep(5)
            scrap(url+actname+str(pgno)+"/index.html", path+"/"+actname+"/"+actname+str(pgno))
            
            chances=5
		
        if chances == 0 and flag == 0:
            chances=5
            pgno=pgbk
            flag=1
        if flag == 0:
            pgno+=1
        else:
            pgno-=1
    label['text'] = "Pages done"
root = Tk()
root.geometry("300x300")
signal.signal(signal.SIGINT, skip)
Label(root, text="Enter URL:").grid(row=0, sticky=W)

entry_ln = Entry(root)
entry_ln.grid(row=0, column=1)

b_start = Button(root, text="start")
b_start.grid(row=7, column=1)

label = Label(root, text="status")
label.grid(row=8, column=1)

b_start['command'] = clicked
root.mainloop()
