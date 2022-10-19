#!/usr/bin/env python3
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import urllib.request
import requests
import re
import json as JSON
import sqlite3
from sqlite3 import Error
import sys

transactionList=[]
pRefList=[]


gameDate, startTime, attendance, stadium, gameDur = " " * 5
teams = { 'ARI' : 'ARI',
                    'ATL': 'ATL',
                    'BAL': 'BAL',
                    'BOS': 'BOS',
                    'CHC': 'CHN',
                    'CHW': 'CHA',
                    'CIN': 'CIN',
                    'CLE': 'CLE',
                    'COL': 'COL',
                    'DET': 'DET',
                    'HOU': 'HOU',
                    'KCR': 'KCA',
                    'LAA': 'ANA',
                    'LAD': 'LAN',
                    'MIA': 'MIA',
                    'MIL': 'MIL',
                    'MIN': 'MIN',
                    'NYM': 'NYN',
                    'NYY': 'NYY',
                    'OAK': 'OAK',
                    'PHI': 'PHI',
                    'PIT': 'PIT',
                    'SDP': 'SDN',
                    'SFG': 'SFN',
                    'SEA': 'SEA',
                    'STL': 'SLN',
                    'TBR': 'TBA',
                    'TEX': 'TEX',
                    'TOR': 'TOR',
                    'WAS': 'WAS'}

battingNames = {"ATL":"AtlantaBravesbatting",
                    "ARI":"ArizonaDiamondbacksbatting",
                    "BAL":"BaltimoreOriolesbatting",
                    "BOS":"BostonRedSoxbatting",
                    "CHC":"ChicagoCubsbatting",
                    "CHW":"ChicagoWhiteSoxbatting",
                    "CIN":"CincinnatiRedsbatting",
                    "CLE":"ClevelandGuardiansbatting",
                    "COL":"ColoradoRockiesbatting",
                    "DET":"DetroitTigersbatting",
                    "KCR":"KansasCityRoyalsbatting",
                    "HOU":"HoustonAstrosbatting",
                    "LAA":"AnaheimAngelsbatting",
                    "LAD":"LosAngelesDodgersbatting",
                    "MIA":"MiamiMarlinsbatting",
                    "MIL":"MilwaukeeBrewersbatting",
                    "MIN":"MinnesotaTwinsbatting",
                    "NYM":"NewYorkMetsbatting",
                    "NYY":"NewYorkYankeesbatting",
                    "OAK":"OaklandAthleticsbatting",
                    "PHI":"PhiladelphiaPhilliesbatting",
                    "PIT":"PittsburghPiratesbatting",
                    "SDP":"SanDiegoPadresbatting",
                    "SEA":"SeattleMarinersbatting",
                    "SFG":"SanFranciscoGiantsbatting",
                    "STL":"StLouisCardinalsbatting",
                    "TBR":"TampaBayRaysbatting",
                    "TEX":"TexasRangersbatting",
                    "TOR":"TorontoBlueJaysbatting",
                    "WAS":"WashingtonNationalsbatting"}

pitchingNames = {"ATL":"AtlantaBravespitching",
                    "ARI":"ArizonaDiamondbackspitching",
                    "BAL":"BaltimoreOriolespitching",
                    "BOS":"BostonRedSoxpitching",
                    "CHC":"ChicagoCubspitching",
                    "CHW":"ChicagoWhiteSoxpitching",
                    "CIN":"CincinnatiRedspitching",
                    "CLE":"ClevelandGuardianspitching",
                    "COL":"ColoradoRockiespitching",
                    "DET":"DetroitTigerspitching",
                    "KCR":"KansasCityRoyalspitching",
                    "HOU":"HoustonAstrospitching",
                    "LAA":"AnaheimAngelspitching",
                    "LAD":"LosAngelesDodgerspitching",
                    "MIA":"MiamiMarlinspitching",
                    "MIL":"MilwaukeeBrewerspitching",
                    "MIN":"MinnesotaTwinspitching",
                    "NYM":"NewYorkMetspitching",
                    "NYY":"NewYorkYankeespitching",
                    "OAK":"OaklandAthleticspitching",
                    "PHI":"PhiladelphiaPhilliespitching",
                    "PIT":"PittsburghPiratespitching",
                    "SDP":"SanDiegoPadrespitching",
                    "SEA":"SeattleMarinerspitching",
                    "SFG":"SanFranciscoGiantspitching",
                    "STL":"StLouisCardinalspitching",
                    "TBR":"TampaBayRayspitching",
                    "TEX":"TexasRangerspitching",
                    "TOR":"TorontoBlueJayspitching",
                    "WAS":"WashingtonNationalspitching"}


def main():
    homeTeam = sys.argv[1]
    awayTeam = sys.argv[2]
    gameDate = sys.argv[3]
    team = teams[homeTeam]

    print()
    print('    ' + homeTeam + ' vs ' + awayTeam)
    print('-------------------')
    url = 'https://www.baseball-reference.com/boxes/%s/%s%s0.shtml' % (team,team,gameDate)
    res = requests.get(url)
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("", res.text), 'html.parser')

    scorebox = soup.find(attrs = {'class' : 'scorebox_meta'})
    divs = scorebox.find_all('div')
    gameDate = divs[0].text
    startTime = divs[1].text
    attendance = divs[2].text
    stadium = divs[3].text
    gameDur = divs[4].text
    #startTime = divs[1].text.strip("Start Time: ").replace(' Local','')
    #attendance = int(divs[2].text.strip("Attendance: ").replace(',',''))
    #stadium = divs[3].text.strip("Venue: ")
    #gameDur = divs[4].text.strip("Game Duration: ")
    gameInfo = [gameDate, startTime, attendance, stadium, gameDur]
    for i in gameInfo:
        print(i)

    print()
    print('------------------------------------------------------------')
    print('                         ' + homeTeam + ' Batting')
    print('------------------------------------------------------------')
    homeBatting = soup.find_all("table", {"id":"%s" % battingNames[homeTeam]})
    data_rows = homeBatting[0].findAll('tr')
    data_header = homeBatting[0].findAll('thead')
    data_header = data_header[0].findAll("tr")
    data_header = data_header[0].findAll("th")
    game_data = [[td.getText() for td in data_rows[i].findAll(['th','td'])]
        for i in range(len(data_rows))
        ]
    data = pd.DataFrame(game_data)
    header = []
    for i in range(len(data.columns)):
        header.append(data_header[i].getText())
    data.columns = header
    data = data.loc[data[header[0]] != header[0]]
    data = data.reset_index(drop = True)
    data.drop(columns=['BA','OBP','SLG','OPS','Pit','Str','WPA','WPA+','WPA-','cWPA','aLI','acLI','RE24','PO','A'],inplace=True)
    data = data[data.PA != '']
    print(data)


    print()
    print('------------------------------------------------------------')
    print('                         ' + awayTeam + ' Batting')
    print('------------------------------------------------------------')
    awayBatting = soup.find_all("table", {"id":"%s" % battingNames[awayTeam]})
    data_rows = awayBatting[0].findAll('tr')
    data_header = awayBatting[0].findAll('thead')
    data_header = data_header[0].findAll("tr")
    data_header = data_header[0].findAll("th")
    game_data = [[td.getText() for td in data_rows[i].findAll(['th','td'])]
        for i in range(len(data_rows))
        ]
    data = pd.DataFrame(game_data)
    header = []
    for i in range(len(data.columns)):
        header.append(data_header[i].getText())
    data.columns = header
    data = data.loc[data[header[0]] != header[0]]
    data = data.reset_index(drop = True)
    data.drop(columns=['BA','OBP','SLG','OPS','Pit','Str','WPA','WPA+','WPA-','cWPA','aLI','acLI','RE24','PO','A'],inplace=True)
    data = data[data.PA != '']
    print(data)


    print()
    print('------------------------------------------------------------------------')
    print('                         ' + homeTeam + ' Pitching')
    print('------------------------------------------------------------------------')
    homePitching = soup.find_all("table", {"id":"%s" % pitchingNames[homeTeam]})
    data_rows = homePitching[0].findAll('tr')
    data_header = homePitching[0].findAll('thead')
    data_header = data_header[0].findAll("tr")
    data_header = data_header[0].findAll("th")
    game_data = [[td.getText() for td in data_rows[i].findAll(['th','td'])]
        for i in range(len(data_rows))
        ]
    data = pd.DataFrame(game_data)
    header = []
    for i in range(len(data.columns)):
        header.append(data_header[i].getText())
    data.columns = header
    data = data.loc[data[header[0]] != header[0]]
    data = data.reset_index(drop = True)
    data.drop(columns=['Ctct','StS','StL','GB','FB','LD','Unk','GSc','IR','IS','WPA','aLI','cWPA','acLI','RE24'],inplace=True)
    print(data)


    print()
    print('------------------------------------------------------------------------')
    print('                         ' + awayTeam + ' Pitching')
    print('------------------------------------------------------------------------')
    awayPitching = soup.find_all("table", {"id":"%s" % pitchingNames[awayTeam]})
    data_rows = awayPitching[0].findAll('tr')
    data_header = awayPitching[0].findAll('thead')
    data_header = data_header[0].findAll("tr")
    data_header = data_header[0].findAll("th")
    game_data = [[td.getText() for td in data_rows[i].findAll(['th','td'])]
        for i in range(len(data_rows))
        ]
    data = pd.DataFrame(game_data)
    header = []
    for i in range(len(data.columns)):
        header.append(data_header[i].getText())
    data.columns = header
    data = data.loc[data[header[0]] != header[0]]
    data = data.reset_index(drop = True)
    data.drop(columns=['Ctct','StS','StL','GB','FB','LD','Unk','GSc','IR','IS','WPA','aLI','cWPA','acLI','RE24'],inplace=True)
    print(data)

    print()

if __name__ == "__main__":
   main()

"""

colNames = ['Season', 'Day', 'Name', 'Team', 'League', 'PreviousTeam', 'PreviousLeague', 'Type']
transactions = pd.DataFrame(transactionList, columns=colNames)
jaytran = transactions.to_json(orient='records')
jayson = JSON.loads(jaytran)
with open('transactions.json', 'w') as json_file:
    JSON.dump(jayson, json_file)
"""
"""

def create_connection(db_file):
    # create a database connection to a SQLite database
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_connection(r'/Users/danny/Desktop/okcproj/db/transactions.db')

conn = sqlite3.connect('/Users/danny/Desktop/okcproj/db/transactions.db')
transactions.to_sql('transactions', conn)

pcolNames = ['Name', 'Nationality', 'Position', 'Height', 'Weight']
players = pd.DataFrame(playersList, columns=pcolNames)
"""
