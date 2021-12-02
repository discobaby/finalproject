#######
# Calculation and visualtiona
#######
import os
import sqlite3
import matplotlib.pyplot as plt


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

    plt.xlabel('Networth in Million Dollars', fontsize=14)
    plt.ylabel('Number of Fans in Million', fontsize=14)
    plt.title('Relationship among Gender, Networth and Number of Fans of Top {} Artists'.format(len(data)), fontsize=14)
    plt.legend(['Female', 'Male'], fontsize = 12)
    
    plt.savefig('genderScatterPlot.png')
    plt.show()
    

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(dir_path + '/' + "finalproject.db")
    cur = conn.cursor()
    # first visualization  
    genderScatterPlot(cur, conn)


if __name__ == "__main__":
    main()