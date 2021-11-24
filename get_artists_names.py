#############
# Name: Ember Shan
# This file is to get a list of 200 artists names from the website
# and store it in a txt file
# Then create the Artists table in the database 
# based on the txt file scraped from the website
# a total of 200 artist names so a total of 10 times to add all items
#############

import os 
import sqlite3
from bs4 import BeautifulSoup
import requests
import os


def createSoup():
    url = "https://www.songkick.com/leaderboards/popular_artists"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup


def getData(soup):
    names = []
    table = soup.find('table')
    rows = table.find_all("tr")
    for r in rows[1:]:
        name_cols = r.find('td', class_ = "name")
        names.append(name_cols.text.lstrip('\n'))

    dir_path = os.path.dirname(os.path.realpath(__file__)) 
    path = dir_path + '/' + 'artist_names.txt'
    f = open(path, 'w')
    f.writelines(names[0:200])
    f.close()


def getDataFromFile():
    dir_path = os.path.dirname(os.path.realpath(__file__)) 
    path = dir_path + '/' + 'artist_names.txt'
    # get the names in the file
    with open(path, 'r') as file: 
        names = file.readlines()
    # return the list of names in order 
    return names


def createArtistDatabase(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS Artists (artist_id INTEGER PRIMARY KEY, name TEXT)')
    names = getDataFromFile()
    # checking what have already been stored to the database
    # get the last row of the database
    cur.execute('SELECT artist_id, name FROM Artists ORDER BY artist_id DESC LIMIT 1')
    row = cur.fetchone()
    # check if this is the first time inserting the data
    if row: 
        print(row)
        # get the id of the last inserted item 
        count = row[0]
    else: 
        count = 1 # count for id
    # insert only 20 items to the database
    end = count + 20 if len(names) >= count + 20 else len(names)
    for i in range(count-1, end): 
        cur.execute('INSERT OR IGNORE INTO Artists (artist_id, name) VALUES (?, ?)', \
            (count, names[i].strip('\n')))
        count += 1
    conn.commit()


def main():
    # scrap data from the website
    dir_path = os.path.dirname(os.path.realpath(__file__)) 
    path = dir_path + '/' + 'artist_names.txt'
    # checking if the file is empty
    if os.stat(path).st_size == 0:
        print("file is empty, getting the data from website")
        s = createSoup()
        getData(s)
    # create the artists database
    conn = sqlite3.connect(dir_path + '/' + "finalproject.db")
    cur = conn.cursor()
    createArtistDatabase(cur, conn)

    
if __name__ == "__main__":
    main()