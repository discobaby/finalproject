#######
# Calculation and visualtions
#######
import os
import sqlite3
import matplotlib.pyplot as plt

dir_path = os.path.dirname(os.path.realpath(__file__))

def genderScatterPlot(cur, conn):
    # get the data from NetWorth and Artists
    cur.execute("SELECT Artists.name, NetWorth.gender, Artists.fans_count, NetWorth.net_worth FROM NetWorth JOIN Artists ON \
        Artists.artist_id = NetWorth.id WHERE gender != 'NA'")
    data = cur.fetchall()
    colors = ['salmon', 'lightblue']
    fig = plt.figure(figsize = (15, 10))
    for d in data:
        g = 1 if d[1] == 'female' else 0
        x = d[3]/1000000
        y = int(d[2].replace(',', ''))/1000000
        # begin plotting the data
        plt.scatter(x, y, label = d[0], color = colors[g])
        # plt.annotate(text=d[0], xy = (x+0.004, y+0.001), fontsize = 8)

    # customizing a little 
    plt.xlabel('Networth in Million Dollars', fontsize=14)
    plt.ylabel('Number of Fans in Million', fontsize=14)
    plt.title('Gender distributoin in relation to Networth and Number of Fans of Top {} Artists'.format(len(data)), fontsize=14)
    plt.legend(['Female', 'Male'], fontsize = 12)
    # save the plot 
    plt.savefig(dir_path + '/visualizations/genderScatterPlot.png')
    plt.show()
    

def getAvgNetworthByGender(cur):
    # extracting the data 
    cur.execute("SELECT net_worth FROM NetWorth WHERE gender = 'male'")
    male_networth = [x[0] for x in cur.fetchall()]
    cur.execute("SELECT net_worth FROM NetWorth WHERE gender = 'female'")
    female_networth = [x[0] for x in cur.fetchall()]
    # calculate the averages 
    avg_m = sum(male_networth) / len(male_networth) / 1000000
    avg_f = sum(female_networth) / len(female_networth) / 1000000
    # save the data to a file 
    f = open(dir_path + '/calculation_files/avg_networth_by_gender.txt', 'w')
    f.write(f'average networth of male celebrities: {avg_m}, average networth of female celebrities: {avg_f}')
    f.close()
    # plot the data
    plt.bar(['male', 'female'], [avg_m, avg_f], color = ['salmon', 'lightblue'], width = 0.5)
    plt.title('Average networth of celebrities by Gender')
    plt.xlabel("Gender")
    plt.ylabel('Avg Networth in millions')
    # save the plots
    plt.savefig(dir_path + '/visualizations/avgNetWorthByGender.png')
    plt.show()


def genderFollowersScatterPlot(cur, conn):
    dir_path = os.path.dirname(os.path.realpath(__file__))
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
    
    plt.savefig(dir_path + '/visualizations/genderFollowersScatterPlot.png')
    plt.show()


def main():
    conn = sqlite3.connect(dir_path + '/' + "finalproject.db")
    cur = conn.cursor()
    # first visualization  
    genderScatterPlot(cur, conn)
    # second visualization 
    getAvgNetworthByGender(cur)
    # third visualization 
    genderFollowersScatterPlot(cur, conn)


if __name__ == "__main__":
    main()
