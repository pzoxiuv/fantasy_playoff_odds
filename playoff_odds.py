import pandas as pd
import numpy as np
import random
import pickle 
import json
import math

teams = ["Simon", "Levi", "Traci", "Caleb", "Dan", "Zach", "Alex", "Carter"]

def random_winner(matchup):
  team_0 = matchup[0]
  team_1 = matchup[1]  
  #
  #   Pick the winner with random coin toss
  if random.random() <= .5:
    return team_0
  else:
    return team_1

def picked_winner(random_winner, matchup, week,  picks):
  team_0 = matchup[0]
  team_1 = matchup[1]  
  # 
  try:
    this_weeks_picks = picks[week]
    if team_0 in this_weeks_picks:
      return team_0
    elif team_1 in this_weeks_picks:
      return team_1
    else:
      return random_winner 
  except KeyError:
    return random_winner


def simulate_seasons(schedule, actual_record, n_iter, picks):
  ''' 
      Simulate the remaining games in a season and return an array of final wins.
  '''
  final_wins = []
  for i in range(n_iter):
  #
    c_wins = actual_record.copy()
  #
    for week in range(9, 15):
      ## get matchups this week
      matchups = schedule[week]
    #
    # setup empty wins and points this week
      wins = c_wins[week - 1].copy()
    #
      for matchup in matchups:
        winner = random_winner(matchup) ## get coin-toss winner
    #
        winner = picked_winner(winner, matchup, week, picks) ## override if there's a picked winner
        wins[int(winner) - 1] += 1
    #
      c_wins[week] = wins
  #
    final_wins.append(c_wins[-1])
  return final_wins


def get_playoffs(wins):
  '''
    Given the final number of wins from each team, figure out who makes playoffs.
    First we find the cutoff (# of wins of the 4th place team), then everyone above makes it.
    To break ties, we randomly pick from teams at the cutoff.
  '''
  cutoff = sorted(wins)[4]
  made_playoffs = np.where(np.array(wins) > cutoff)[0].tolist()
#
# now randomly chose a team at the cutoff
  bubble = np.where(np.array(wins) == cutoff)[0].tolist()
  sample_n = 4 - len(made_playoffs) ## how many more need to make it
  made_playoffs.extend( random.sample(bubble, sample_n)  )
#
  return(made_playoffs)

def playoff_odds(final_wins):
  '''
    Turn all the simulated wins into one set of playoff odds
  '''
  playoffs = [0] * 8
  for wins in final_wins:
    teams = get_playoffs(wins)
    for team in teams:
      playoffs[team] += 1
#
  odds = (np.array(playoffs) / len(final_wins))
  return odds


## ------------- Run Simulations ----------------------
def simulate(record_file = "data/actual_record.pkl", schedule_file = "data/schedule.pkl",
            n_iter = 10000, picks = {}):
  '''
    Main function to run the whole simulation
  '''
  fl = open(record_file, 'rb') 
  actual_record = pickle.load(fl)
#
  ## Get the schedule in order to simulate the remaining games
  fl2 = open(schedule_file, 'rb') 
  schedule = pickle.load(fl2)

  print(schedule)
  print(actual_record)
  print(picks)
#
  ## Simulate 10,000 seasons with this schedule
  final_wins = simulate_seasons(schedule, actual_record, 10000, picks)
#
  ## Get final playoff odds from these simulations
  odds = playoff_odds(final_wins)
#
  ## Display using actual team names
  #teams = ["Simon", "Levi", "Traci", "Caleb", "Dan", "Zach", "Alex", "Carter"]
  print(pd.DataFrame( [ teams, odds]))
#
  ## Make json object for the results
  odds_dict = {}
  for team_odds, team in zip(odds, teams):
    odds_dict[team] = str(round(team_odds * 100, 3)) + "%"
#
  return json.dumps(odds_dict, indent = 2)

def get_schedule(schedule_file = "data/schedule.pkl"):
  with open(schedule_file, 'rb') as f:
    return pickle.load(f)

print(simulate())
