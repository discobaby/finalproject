#######
# Calculation and visualtions
# Gender and Spotify Followers ScatterPlot
# Gender and Twitter Followers ScatterPlot
#######
import os
import sqlite3
import matplotlib.pyplot as plt


def genderFollowersScatterPlot(cur, conn):
    # get the data from Spotify and NetWorth 
    cur.execute("SELECT SpotifyArtistData.name, NetWorth.gender, SpotifyArtistData.followers, TwitterData.follower_count FROM NetWorth JOIN SpotifyArtistData ON SpotifyArtistData.id = NetWorth.id JOIN TwitterData ON TwitterData.id = NetWorth.id WHERE gender != 'NA'")
    data = cur.fetchall()
    colors = ['salmon', 'lightblue']
    fig = plt.figure(figsize = (15, 10))
    for d in data:
        g = 1 if d[1] == 'female' else 0
        x = d[2]/100000
        y = d[3]/100000
        # begin plotting the data
        plt.plot(x, y, 'o', color = colors[g])
    plt.xlabel('Number of Spotify Followers in Hundred-Thousands', fontsize=14)
    plt.ylabel('Number of Twitter Followers in Hundred-Thousands', fontsize=14)
    plt.title('Relationship among Gender and Follower Count', fontsize=14)
    plt.legend(['Female', 'Male'], fontsize = 12)
    
    plt.savefig('genderFollowersScatterPlot.png')
    plt.show()

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(dir_path + '/' + "finalproject.db")
    cur = conn.cursor()
    # first visualization  
    genderFollowersScatterPlot(cur, conn)


if __name__ == "__main__":
    main()