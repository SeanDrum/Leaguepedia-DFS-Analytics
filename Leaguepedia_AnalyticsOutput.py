import pandas as pd
import numpy as np
import xlsxwriter



def CreatePlayerAggregateFrame(results):
    playerMetaDataJoinDropColumns = ['Team1','Team2','WinTeam', 'fptsk', 'fptsd', 'fptsa', 'fptscs', 'fptstenbonus', 'fptstotal']
    playerMetaDataJoinFrame = results.copy()
    playerMetaDataJoinFrame = playerMetaDataJoinFrame.drop(columns=playerMetaDataJoinDropColumns, axis=1).drop_duplicates()
    playerMetaDataJoinFrame = playerMetaDataJoinFrame.set_index('OverviewPage')
    
    playerAggregateFrame = results.groupby('OverviewPage').sum().sort_values(by=['fptstotal'], ascending=False)     
    playerAggregateFrame = playerMetaDataJoinFrame.join(playerAggregateFrame)
    playerAggregateFrame = playerAggregateFrame.sort_values(by=['fptstotal'], ascending=False)

    playerMax = results.groupby('OverviewPage')['fptstotal'].max()
    playerMin = results.groupby('OverviewPage')['fptstotal'].min()

    # print(playerMin)

    return playerAggregateFrame


def CreateTeamAndPositionFrame(results, year):
    teamPointsPivotFrame = pd.pivot_table(results, values='fptstotal', index=['WinTeam'], aggfunc=np.sum)
    teamPointsPivotFrame = teamPointsPivotFrame.sort_values(by='fptstotal', ascending=False)

    teamPointsPivotFrame['Year'] = year
    teamPointsPivotFrame.rename(columns={'fptstotal': 'Points'}, inplace = True)
    teamPointsPivotFrame.index.names = ['Team']

    positionPointsPivotFrame = pd.pivot_table(results, values='fptstotal', index=['Role'], aggfunc=np.sum)
    positionPointsPivotFrame = positionPointsPivotFrame.sort_values(by='fptstotal', ascending=False)

    return teamPointsPivotFrame, positionPointsPivotFrame


def CreatePlayerPointsFrame(results):
    playerPointsPivotFrame = pd.pivot_table(results, values='fptstotal', index=['OverviewPage', 'Role'], aggfunc=np.sum)
    playerPointsPivotFrame = playerPointsPivotFrame.sort_values(by=['fptstotal'], ascending=False)

    positionList = ['''"Top"''','''"Jungle"''','''"Mid"''','''"Bot"''','''"Support"''']
    playerPointsFrameList = []
    
    for position in positionList:
        playerPointsFrame = playerPointsPivotFrame.query('Role == ' + position)
        playerPointsFrame.index.names = [position.replace('"', ''), 'delete']
        playerPointsFrame.reset_index(level='delete', drop=True, inplace=True)
        playerPointsFrameList.append(playerPointsFrame)

    return playerPointsFrameList     



def main(year, rawDataCsv):
  
    keepColumns = ['OverviewPage','Role','Team','Team1','Team2','WinTeam','fptsk', 'fptsd', 'fptsa', 'fptscs', 'fptstenbonus', 'fptstotal']

    playerFrame = pd.read_csv(rawDataCsv)

    dropColumns = [c for c in playerFrame.columns if c not in keepColumns]
    playerFrame.drop(dropColumns, inplace=True, axis=1)

    teamPointsPivotFrame, positionPointsPivotFrame = CreateTeamAndPositionFrame(playerFrame, year)
    playerPointsFrameList = CreatePlayerPointsFrame(playerFrame)
    playerAggregateFrame = CreatePlayerAggregateFrame(playerFrame)
    print(playerPointsFrameList)

    excelWriter = pd.ExcelWriter(rawDataCsv.split('.')[0]+'-analysis.xlsx', engine='xlsxwriter')

    teamPointsPivotFrame.to_excel(excelWriter, sheet_name='Team Points')
    positionPointsPivotFrame.to_excel(excelWriter, sheet_name='Position')
    playerAggregateFrame.to_excel(excelWriter, sheet_name='All Players')

    for frameList in playerPointsFrameList:     
        frameList.to_excel(excelWriter, sheet_name=frameList.index.name)

    excelWriter.save()
    

if __name__ == '__main__':
    rawDataCsv='LCS-2020-Summer-Season.csv'
    year=2020

    main(year, rawDataCsv)

'''
MORE ADVANCED
By Role:
    Player	
    Average Points
    Total Points
    Max Points
    Min Points
    Standard Deviation
    Games Played
'''