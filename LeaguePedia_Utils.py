def GetFields():
    return "SG.DateTime_UTC, \
            SG.MatchHistory, \
            SG.Team1, \
            SG.Team2, \
            SG.WinTeam, \
            SG.Team1Dragons, \
            SG.Team2Dragons, \
            SG.Team1RiftHeralds, \
            SG.Team2RiftHeralds, \
            SG.Team1Barons, \
            SG.Team2Barons, \
            SG.Team1Towers, \
            SG.Team2Towers, \
            SG.Team1Inhibitors, \
            SG.Team2Inhibitors, \
            SG.Team1Gold, \
            SG.Team2Gold, \
            SG.Team1Kills, \
            SG.Team2Kills, \
            SG.Gamelength_Number, \
            SG.Gamelength, \
            PR.OverviewPage, \
            SP.Champion, \
            SP.Role, \
            SP.Team, \
            SP.Kills, \
            SP.Deaths, \
            SP.Assists, \
            SP.Gold, \
            SP.CS"  
    
    
def GetColumns(includeDerived):
    columnList = ['DateTime UTC', 
            'MatchHistory', 
            'Team1', 
            'Team2', 
            'WinTeam', 
            'Team1Dragons', 
            'Team2Dragons', 
            'Team1RiftHeralds', 
            'Team2RiftHeralds', 
            'Team1Barons', 
            'Team2Barons', 
            'Team1Towers', 
            'Team2Towers', 
            'Team1Inhibitors', 
            'Team2Inhibitors', 
            'Team1Gold', 
            'Team2Gold', 
            'Team1Kills', 
            'Team2Kills', 
            'Gamelength Number', 
            'Gamelength', 
            'OverviewPage', 
            'Champion', 
            'Role', 
            'Team', 
            'Kills', 
            'Deaths', 
            'Assists', 
            'Gold', 
            'CS']

    if includeDerived:
        columnList.extend([
            'CSPM', 
            'GPM',
            'KPAR',
            'fptsk',
            'fptsd',
            'fptsa',
            'fptscs',
            'fptstenbonus',
            'fptstotal'])
    
    return columnList