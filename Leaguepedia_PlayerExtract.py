import mwclient
from LeaguePedia_Utils import GetColumns, GetFields
import csv
import pprint
pp = pprint.PrettyPrinter(indent=4)


def GetBaseData():
    site = mwclient.Site('lol.gamepedia.com', path='/')
    response = site.api('cargoquery',
        limit = "max",
    tables = "ScoreboardGames=SG, ScoreboardPlayers=SP, PlayerRedirects=PR",
    join_on = "SG.UniqueGame=SP.UniqueGame, SP.Link=PR.AllName",
    fields = GetFields(),
    where =  "SG.OverviewPage = 'LCS/2020 Season/Summer Season' AND SG.DateTime_UTC < '2020-06-26 00:00:00'" #first batch
    #where =  "SG.OverviewPage = 'LCS/2020 Season/Summer Season' AND SG.DateTime_UTC > '2020-06-26 00:00:00'" #second batch
    #where =  "SG.OverviewPage = 'LCS/2020 Season/Summer Season' AND SG.DateTime_UTC > '2020-07-27 00:00:00'" #third batch
    )

    return response


def GetKaBonus(kills, assists):
    if kills >= 10 or assists >= 10:
        return 2
    else:
        return 0


def CreateFantasyScores(match):
    fptsk = float(match['Kills']) * 3
    fptsd = float(match['Deaths']) - (float(match['Deaths']) * 2)
    fptsa = float(match['Assists']) * 2
    fptscs = float(match['CS']) * .02
    fptstenbonus = GetKaBonus(float(match['Kills']), float(match['Assists']))
    fptstotal = fptsk + fptsd + fptsa + fptscs + fptstenbonus

    return [fptsk, fptsd, fptsa, fptscs, fptstenbonus, fptstotal]


def CreateCalculatedFields(match):
    CSPM = float(match['CS'])/float(match['Gamelength Number'])
    GPM = float(match['Gold'])/float(match['Gamelength Number'])
    try:
        KPAR = (float(match['Kills'])+float(match['Assists']))/(float(match['Team1Kills']) if match['Team']==match['Team1'] else float(match['Team2Kills']))*100
    except ZeroDivisionError:
        KPAR = 0

    return [CSPM, GPM, KPAR]


def CreatePlayerCsv(tournament, response):
    with open(tournament.replace(' ', '-') + '.csv', 'w', newline='') as csvOutput:
        writer = csv.writer(csvOutput)
        writer.writerow(GetColumns(includeDerived = True))
    
        for match in response['cargoquery']:
            match = match['title']
            
            dataRowList = [match[attribute] for attribute in GetColumns(includeDerived = False)]
            dataRowList.extend(CreateCalculatedFields(match))
            dataRowList.extend(CreateFantasyScores(match))
            writer.writerow(dataRowList)
        
    print('CSV Output Created')


def main(tournament):
    response = GetBaseData()
    CreatePlayerCsv(tournament, response)


if __name__ == '__main__':
    tournament = 'LCS 2020 Summer Season'
    main(tournament)