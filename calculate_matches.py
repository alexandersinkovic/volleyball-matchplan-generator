#TODO Add Documentation D:

import copy
import random
import csv


NUMBER_OF_TEAMS = 34
NUMBER_OF_TEAMMATES = 6
NUMBER_OF_FIELDS = 3
TOTAL_OCCURENCES = NUMBER_OF_TEAMS * NUMBER_OF_TEAMMATES
OUTPUT_FILENAME = '34Teams6Rounds'
USE_NAME_LIST = True


# ID and Number of necessary Teammates for every Team
availableTeams = [[x+1, NUMBER_OF_TEAMMATES] for x in range(NUMBER_OF_TEAMS)]
availableTeams.append([NUMBER_OF_TEAMS+1, 0])
# ID and Number of necessary Matches for every Team
availableMatches = [[x+1, NUMBER_OF_TEAMMATES] for x in range(NUMBER_OF_TEAMS)]
availableMatches.append([NUMBER_OF_TEAMS+1, 0])
if TOTAL_OCCURENCES % 2 == 1:
    availableTeams[NUMBER_OF_TEAMS][1] += 1
    availableMatches[NUMBER_OF_TEAMS][1] += 1
    TOTAL_OCCURENCES += 1
if TOTAL_OCCURENCES % 4 == 2:
    availableTeams[NUMBER_OF_TEAMS][1] += 2
    availableMatches[NUMBER_OF_TEAMS][1] += 2
    TOTAL_OCCURENCES += 2 


def mycontains(l1, l2):
    for i in l2:
        if i in l1:
            return True
    return False


def reduceAvailableMatches(availableMatches: list[list[int]], a, b):
    # Reduce Matches for Team a
    availableMatches[a-1][1] -= 1
    # Reduce Matches for Team b
    availableMatches[b-1][1] -= 1
    return availableMatches


def increaseAvailableMatches(availableMatches: list[list[int]], a, b):
    # Reduce Matches for Team a
    availableMatches[a-1][1] += 1
    # Reduce Matches for Team b
    availableMatches[b-1][1] += 1
    return availableMatches


def addEnemies(enemies: list[list[int]], a1: int, a2: int, b1: int, b2: int):
    enemies[a1-1].append(b1)
    enemies[a1-1].append(b2)
    enemies[a2-1].append(b1)
    enemies[a2-1].append(b2)
    enemies[b1-1].append(a1)
    enemies[b1-1].append(a2)
    enemies[b2-1].append(a1)
    enemies[b2-1].append(a2)


def getEmptyTeammates():
    if (NUMBER_OF_TEAMS * NUMBER_OF_TEAMMATES) % 2 == 1 or NUMBER_OF_TEAMS * NUMBER_OF_TEAMMATES % 4 == 2:
        return [[] for _ in range(NUMBER_OF_TEAMS+1)]
    return [[] for _ in range(NUMBER_OF_TEAMS)]


def getNewRoundsWaited():
    roundsWaited = [[i+1, 0] for i in range(NUMBER_OF_TEAMS + 1)]
    return roundsWaited


def getSubArrayElems(a: list[list[int]]):
    res = []
    for e in a:
        for t in e:
            res.append(t)
    return res


def adjustRoundsWaited(playingTeams: list[int], roundsWaited: list[list[int]]):
    for team in roundsWaited:
        if team[0] in playingTeams:
            team[1] = 0
        else:
            team[1] += 1
    return


# match [[1, 2],[3, 4]]
# roundsWaited [[1, 1][2, 1][3, 1]]; count rounds for every team that they havent played
def getPriority(match: list[list[int]], roundsWaited: list[list]):
    teams = copy.deepcopy(match[0])
    teams.append(match[1][0])
    teams.append(match[1][1])
    return sum([roundsWaited[x-1][1] for x in teams])


def getRoundsPerTeam(rounds: list[list[list[int]]]):
    res = [[] for _ in range(NUMBER_OF_TEAMS + 1)]
    for idx, round in enumerate(rounds):
        for match in round:
            for team in match:
                res[team[0]-1].append(str(idx+1))
                res[team[1]-1].append(str(idx+1))
    return res



def generate_teams(teammates: list[list[int]], availableTeams: list[list[int]]):
    # IDs of all Teams without enough teammates
    availableIds = [t[0] for t in availableTeams if t[1] > 0]
    if len(availableIds) == 0:
        return teammates, True
    availableTeamsCopy = copy.deepcopy(availableTeams)
    # First team chosen randomly
    randomTeamAIdx = random.randint(0, len(availableIds)-1)
    randomTeamA = availableIds.pop(randomTeamAIdx)
    # Reduce Teammate Counter for Team A
    availableTeamsCopy[randomTeamA-1][1] -= 1
    # Loop over all remaining available teammates
    while(len(availableIds) > 0):
        randomTeamBIdx = random.randint(0, len(availableIds)-1)
        randomTeamB = availableIds.pop(randomTeamBIdx)
        # Dont match if they have been matched already
        if ( randomTeamB in teammates[randomTeamA-1] or randomTeamA in teammates[randomTeamB-1]):
            continue
        teammates[randomTeamA-1].append(randomTeamB)
        teammates[randomTeamB-1].append(randomTeamA)
        # Copy available Teams
        availableTeamsCopyMiddle = copy.deepcopy(availableTeamsCopy)
        # Reduce Teammate Counter for Team B
        availableTeamsCopy[randomTeamB-1][1] -= 1
        teammates, success = generate_teams(teammates, availableTeamsCopy)
        if success:
            return teammates, True
        # Restore changes
        teammates[randomTeamA-1].pop()
        teammates[randomTeamB-1].pop()
        availableTeamsCopy = availableTeamsCopyMiddle
    return teammates, False


# Teammates = [[A,B][C,D]] 1 spielt mit A und B, 2 spielt mit C und D
# Enemies = [[2, D][1, B]] 1 hat bereits gegen 2 und D gespielt, 2 hat bereits gegen 1 und B gespielt
# matches = [[[1, B][2, D]]]
def generate_matches(teammates: list[list[int]], enemies: list[list[int]], availableMatches: list[list[int]], resMatches: list[list[list[int]]]):
    # IDs of all Teams without enough matches
    availableIds = [t[0] for t in availableMatches if t[1] > 0]
    if len(availableIds) == 0:
        return resMatches, True
    availableMatchesCopy = copy.deepcopy(availableMatches)
    # First team doesnt have to be chosen randomly so we chose highest idx ##TODO: Add backtracking
    randomAIdx = random.randint(0, len(availableIds)-1)
    a1ID = availableIds.pop(randomAIdx)
    # Select highest available Index as teammate ##TODO: Add Backtracking
    a2ID = teammates[a1ID-1].pop()
    teammates[a2ID-1].remove(a1ID)
    availableIds.remove(a2ID)
    # Reduce Matches Counter for Team A
    reduceAvailableMatches(availableMatchesCopy, a1ID, a2ID)
    # Loop over all remaining Teams without enough matches
    while(len(availableIds) > 0):
        b1Idx = random.randint(0, len(availableIds)-1)
        b1ID = availableIds.pop(b1Idx)
        if (b1ID in enemies[a1ID-1] or b1ID in enemies[a2ID-1]):
            continue
        # All available Teammates for B1 that havent played against A1 or A2
        b1Teammates = [x for x in copy.deepcopy(teammates[b1ID-1]) if x in availableIds and x not in enemies[a1ID-1] and x not in enemies[a2ID-1]]
        # Loop over all Teammates for B1
        while(len(b1Teammates) > 0):
            # Choose highest index because the list is unsorted
            b2ID = b1Teammates.pop()
            teammates[b2ID-1].remove(b1ID)
            teammates[b1ID-1].remove(b2ID)
            reduceAvailableMatches(availableMatchesCopy, b1ID, b2ID)
            newEnemies = copy.deepcopy(enemies)
            addEnemies(newEnemies, a1ID, a2ID, b1ID, b2ID)
            resMatches.append([[a1ID, a2ID], [b1ID, b2ID]])
            resMatches, success = generate_matches(teammates, newEnemies, availableMatchesCopy, resMatches)
            if success:
                return resMatches, True
            resMatches.pop()
            increaseAvailableMatches(availableMatchesCopy, b1ID, b2ID)
            teammates[b2ID-1].append(b1ID)
            teammates[b1ID-1].append(b2ID)
        pass
    teammates[a2ID-1].append(a1ID)
    teammates[a1ID-1].append(a2ID)
    return resMatches, False

# 
# matches [[[1, 2][3, 4]], [[1, 3][5, 6]]]
# roundsWaited [[1, 1][2, 1][3, 1]]; count rounds for every team that they havent played
def generate_rounds(matches: list[list[list[int]]], roundsWaited: list[list[int]], currentRound: list[list[list[int]]], rounds: list[list[list[int]]]):
    if (len(matches) == 0):
        return rounds, True
    priorities = [[idx, getPriority(match, roundsWaited)] for idx, match in enumerate(matches)]
    priorities = sorted(priorities, key=lambda x: x[1])
    if (currentRound == []):
        matchesCopy = copy.deepcopy(matches)
        # Choose Match with highest prio and remove match
        highestPrio = priorities.pop()
        firstMatch = matchesCopy.pop(highestPrio[0])
        # Get all 4 teams from First Match
        currentRound = getSubArrayElems(firstMatch)
        rounds.append([firstMatch])
        return generate_rounds(matchesCopy, roundsWaited, currentRound, rounds)
    while (len(priorities) > 0):
        matchesCopy = copy.deepcopy(matches)
        # Choose Match with highest prio and remove match
        highestPrio = priorities.pop()
        nextMatch = matchesCopy.pop(highestPrio[0])
        nextMatchTeams = getSubArrayElems(nextMatch)
        if mycontains(currentRound, nextMatchTeams):
            continue
        for t in nextMatchTeams:
            currentRound.append(t)
        rounds[-1].append(nextMatch)
        if (len(currentRound) == (NUMBER_OF_FIELDS * 4)):
            roundsWaitedCopy = copy.deepcopy(roundsWaited)
            adjustRoundsWaited(currentRound, roundsWaitedCopy)
            rounds, success = generate_rounds(matchesCopy, roundsWaitedCopy, [], rounds)
            if success:
                return rounds, success
        else:
            rounds, success = generate_rounds(matchesCopy, roundsWaited, currentRound, rounds)
            if success:
                return rounds, success
        currentRound = currentRound[0:-4:]
        rounds[-1].pop()
    rounds.pop()
    return rounds, False


def printRoundsToCsv(rounds: list[list[list[int]]], goggleDocPrint: bool):
    with open(OUTPUT_FILENAME+'.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar=';', quoting=csv.QUOTE_MINIMAL)
        # Runde, Feld 1 ,        ,      ,        ,        ,               , , Feld 2 ,        ,      ,        ,        ,                , , Feld 3 ,        ,      ,        ,        ,                
        #      , Team A1, Team A2,      , Team B1, Team B2, Schiedsrichter, , Team A1, Team A2,      , Team B1, Team B2, Schiedsrichter , , Team A1, Team A2,      , Team B1, Team B2, Schiedsrichter 
        #   1  , Team 1 , Team 2 , Gegen, Team 3 , Team 4 ,               , , Team 1 , Team 2 , Gegen, Team 3 , Team 4 ,                , , Team 1 , Team 2 , Gegen, Team 3 , Team 4 ,               
        writer.writerow(['Runde', 'Feld 1', '', '', '', '', '', '', 'Feld 2', '', '', '', '', '', '', 'Feld 3', '', '', '', '', '', ''])
        writer.writerow(['', 'Team A1', 'Team A2', '', 'Team B1', 'Team B2', 'Schiedsrichter', '', 'Team A1', 'Team A2', '', 'Team B1', 'Team B2', 'Schiedsrichter', '', 'Team A1', 'Team A2', '', 'Team B1', 'Team B2', 'Schiedsrichter', ''])
        for idx, round in enumerate(rounds):
            out = [str(idx+1)]
            for teamA, teamB in round:
                for team in teamA:
                    if goggleDocPrint:
                        out.append(f"= (Namen!E{team+1})")
                    else:
                        out.append(str(team))
                out.append('Gegen')
                for team in teamB:
                    if goggleDocPrint:
                        out.append(f"= (Namen!E{team+1})")
                    else:
                        out.append(str(team))
                out.append('')
                out.append('')
            writer.writerow(out)
        roundsPerTeam = getRoundsPerTeam(rounds)
        writer.writerow([''])
        writer.writerow(['Runden pro Team'])
        for idx, playsInRounds in enumerate(roundsPerTeam):
            if goggleDocPrint:
                writer.writerow([f"= (Namen!E{str(idx+2)})",'"' + ','.join(playsInRounds) + '"'])
            else:
                writer.writerow([str(team),'"' + ','.join(playsInRounds) + '"'])


def main():
    teammates, _ = generate_teams(getEmptyTeammates(), availableTeams)
    matches, _ = generate_matches(teammates, getEmptyTeammates(), availableMatches, [])
    rounds, _ = generate_rounds(matches, getNewRoundsWaited(), [], [])
    print("RESULT!!!!!!!!!!!!!!!!!!!!")
    printRoundsToCsv(rounds, USE_NAME_LIST)
    
main()