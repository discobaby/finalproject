import unittest
import sqlite3
import json
import os
import numpy as np
import matplotlib.pyplot as plt

path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path+'/'+'finalproject.db')
cur = conn.cursor()

#Creating a list of genres from the SpotifyGenreData database, so I can iterate through them in my main function.
def createGenrelist(cur, conn):
    cur.execute('SELECT genre_id FROM SpotifyGenreData')
    conn.commit()
    data = cur.fetchall()
    genre_list = []
    genre_list.append(data)
    return genre_list
    

#Creating a list of the names of the genres, so I can use them for my plot x-axis label later
def createGenrelistname(cur, conn):
    cur.execute('SELECT genre FROM SpotifyGenreData')
    conn.commit()
    data = [x[0] for x in cur.fetchall()]
    return data

#Creating my main function to iterate through each genre, get the number of twitter followers for each artist that has the specific genre_id, and then get the average.
# Then I plot the data.
 
def getTwitterFollowersByGenre(cur, conn): 
    #Calling my function to get the list of genre id's
    genre_id_list = createGenrelist(cur, conn)
    #Creating an empty list to add the average followers to
    avg_list = []
    #Calling the function to get the list of genre id names
    genre_name_list = createGenrelistname(cur, conn)

    # Iterating through the genre_ids to get my follower count data, which is the first item in a tupple.
    for i in genre_id_list[0]:
        cur.execute('SELECT follower_count FROM TwitterData JOIN SpotifyArtistData ON TwitterData.id = SpotifyArtistData.id WHERE SpotifyArtistData.genre_id=?', (i[0],))
        conn.commit()
        rows = cur.fetchall()
        #Creating empty follower list and adding the artists' followers to that for.
        follower_list = []
        follower_list.append(rows)
        count = 0
        artists = 0
        for num in follower_list:
            #Doing this to avoid the divide by zero or any index error, because some genres have 0 twitter followers averages.
            if len(num) == 0:
                pass
            else: 
                count += int(num[0][0])
        #Getting the length of follower list to divide by and get the averages
        artists = len(follower_list)
        average_num = (int(count) / int(artists))
        #Appending my averages to a list, for all of the genres.
        avg_list.append(average_num)
    
    #Creating my plot, passing in genre_name_list and avg_list for my axes.
    fig = plt.figure(figsize = (15, 10))
    plt.bar(genre_name_list, avg_list)
    plt.xlabel('Genres', fontsize = 12)
    #Setting accurate labels because there is such a wide range of data, that it has to be (in hundres of millions) for it to all fit into one.
    plt.ylabel('Number of Twitter Followers (in hundreds of millions)', fontsize = 10)  
    plt.title('Avg Number of Twitter Followers per Top Spotify Genre')
    #Rotating my x ticks so they do not get overlapped
    plt.xticks(rotation = 90, fontsize = 7)
    plt.show()



#Calling the main function which runs all of my code, looping through the databases, grabs the genre_id list and genre_id_name lists. 
def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'finalproject.db')
    cur = conn.cursor()
    getTwitterFollowersByGenre(cur, conn)

if __name__ == "__main__":
    main()
