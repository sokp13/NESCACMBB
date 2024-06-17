import pandas as pd
import numpy as np
from loader import load_data_no_dict
from flask import Blueprint, render_template
import json

def per_game(val, gp):
    return val/gp

def efg(fgm, tfgm, fga):
    return 100*(fgm+(0.5*tfgm))/fga

def ts_pct(pts, fga, fta):
    return 100*(pts/(2*(fga +(0.44*fta))))

def usage(pts, fg_miss, tov, ft_miss, team_poss):
    out = (pts + fg_miss + (0.44*ft_miss) + tov)/team_poss
    return out

def player_eff(pts, reb, ast, stl, blk, fg_miss, ft_miss, tov, poss, gp, team_poss):
    ur = 100*usage(pts, fg_miss, tov, ft_miss, team_poss)
    per_poss = (pts + reb + ast + stl + blk - fg_miss - ft_miss - tov) / (team_poss / gp)

    combined_metric = (0.7 * per_poss) + (0.3 * ur)

    return combined_metric


pctile = Blueprint('ranks', __name__)
db = load_data_no_dict('csv/rawplayerdata.csv')

db['FG%'] = np.where(db['fga'] != 0, round(100*(db['fgm'] / db['fga']), 1), 0)
db['3PT%'] = np.where(db['threea'] != 0, round(100*(db['threem'] / db['threea']), 1), 0)
db['FT%'] = np.where(db['fta'] != 0, round(100*(db['ftm'] / db['fta']), 1), 0)
db['PER'] = player_eff(db['pts'], db['reb'], db['ast'], db['stl'], db['blk'],
                        (db['fga'] - db['fgm']), (db['fta'] - db['ftm']), db['to'],
                        db['poss'], db['games'], db['team_poss'])
db['TS%'] = ts_pct(db['pts'], db['fga'], db['fta'])
db['eFG%'] = efg(db['fgm'], db['threem'], db['fga'])
# db['atr'] = per_game(db['ast'], db['to'])

db['ppg'] = round(per_game(db['pts'], db['games']), 1)
db['rpg'] = round(per_game(db['reb'], db['games']), 1)
db['apg'] = round(per_game(db['ast'], db['games']), 1)
db['spg'] = round(per_game(db['stl'], db['games']), 1)
db['bpg'] = round(per_game(db['blk'], db['games']), 1)

db.fillna(0, inplace=True)

# db['pts_rank'] = round(db['ppg'].apply(lambda x: percentileofscore(db['ppg'], x)), 0)
# db['reb_rank'] = round(db['rpg'].apply(lambda x: percentileofscore(db['rpg'], x)), 0)
# db['ast_rank'] = round(db['apg'].apply(lambda x: percentileofscore(db['apg'], x)), 0)
# db['stl_rank'] = round(db['spg'].apply(lambda x: percentileofscore(db['spg'], x)), 0)
# db['blk_rank'] = round(db['bpg'].apply(lambda x: percentileofscore(db['bpg'], x)), 0)


###### AVERAGE LEAGUE MARKS ######
avg_marks = {
    'ppg': round(per_game(db['pts'].sum(), db['games'].sum()), 1),
    'rpg': round(per_game(db['reb'].sum(), db['games'].sum()), 1),
    'apg': round(per_game(db['ast'].sum(), db['games'].sum()), 1),
    'spg': round(per_game(db['stl'].sum(), db['games'].sum()), 1),
    'bpg': round(per_game(db['blk'].sum(), db['games'].sum()), 1),
    'FG%': round(100*per_game(db['fgm'].sum(), db['fga'].sum()), 1),
    '3PT%': round(100*per_game(db['threem'].sum(), db['threea'].sum()), 1),
    'FT%': round(100*per_game(db['ftm'].sum(), db['fta'].sum()), 1),
    'eFG%': round(efg(db['fgm'].sum(), db['threem'].sum(), db['fga'].sum()), 1),
    'TS%': round(ts_pct(db['pts'].sum(), db['fga'].sum(), db['fta'].sum()), 1)
}


###### LEAGUE LEADER MARKS ######

q_db = db[db['poss'] >= 75]

# Filter the DataFrame based on the minimum threshold
q_db_fg = q_db[q_db['fga'] >= 50]
q_db_three = q_db[q_db['threea'] >= 25]
q_db_ft = q_db[q_db['fta'] >= 50]


ll_marks = {
    'ppg': q_db['ppg'].max(),
    'rpg': q_db['rpg'].max(),
    'apg': q_db['apg'].max(),
    'spg': q_db['spg'].max(),
    'bpg': q_db['bpg'].max(),
    'FG%': q_db_fg['FG%'].max(),
    '3PT%': q_db_three['3PT%'].max(),
    'FT%': q_db_ft['FT%'].max(),
    'eFG%': q_db_fg['eFG%'].max(),
    'TS%': q_db_fg['TS%'].max()
}

# Get the player who holds the league leader marks for each metric
ll_player_ppg = q_db[q_db['ppg'] == ll_marks['ppg']].iloc[0]
ll_player_rpg = q_db[q_db['rpg'] == ll_marks['rpg']].iloc[0]
ll_player_apg = q_db[q_db['apg'] == ll_marks['apg']].iloc[0]
ll_player_spg = q_db[q_db['spg'] == ll_marks['spg']].iloc[0]
ll_player_bpg = q_db[q_db['bpg'] == ll_marks['bpg']].iloc[0]
ll_player_fg = q_db_fg[q_db_fg['FG%'] == ll_marks['FG%']].iloc[0]
ll_player_three = q_db_three[q_db_three['3PT%'] == ll_marks['3PT%']].iloc[0]
ll_player_ft = q_db_ft[q_db_ft['FT%'] == ll_marks['FT%']].iloc[0]
ll_player_efg = q_db_fg[q_db_fg['eFG%'] == ll_marks['eFG%']].iloc[0]
ll_player_ts = q_db_fg[q_db_fg['TS%'] == ll_marks['TS%']].iloc[0]

# Construct a dictionary of league leader names and marks
ll_leader_names = {
    'ppg': ll_player_ppg['first_name'][0] + '. ' + ll_player_ppg['last_name'],
    'rpg': ll_player_rpg['first_name'][0] + '. ' + ll_player_rpg['last_name'],
    'apg': ll_player_apg['first_name'][0] + '. ' + ll_player_apg['last_name'],
    'spg': ll_player_spg['first_name'][0] + '. ' + ll_player_spg['last_name'],
    'bpg': ll_player_bpg['first_name'][0] + '. ' + ll_player_bpg['last_name'],
    'FG%': ll_player_fg['first_name'][0] + '. ' + ll_player_fg['last_name'],
    '3PT%': ll_player_three['first_name'][0] + '. ' + ll_player_three['last_name'],
    'FT%': ll_player_ft['first_name'][0] + '. ' + ll_player_ft['last_name'],
    'eFG%': ll_player_efg['first_name'][0] + '. ' + ll_player_efg['last_name'],
    'TS%': ll_player_ts['first_name'][0] + '. ' + ll_player_ts['last_name']
}

# Update ll_marks dictionary to include leader names
ll_marks_with_names = {key: {'value': value, 'leader_name': ll_leader_names[key]} for key, value in ll_marks.items()}

# Convert the pandas DataFrame to a list of dictionaries
player_data_json = []
for _, player in db.iterrows():
    player_dict = {
        "name": f"{player['first_name']} {player['last_name']}",
        "PER": player["PER"],
    }
    player_data_json.append(player_dict)

# Convert the list of dictionaries to JSON format
json_data = json.dumps(player_data_json)

@pctile.route('/<int:player_id>/ranks')
def player_pctiles(player_id):
    player_data = db[db['id'] == player_id].iloc[0]
    
    name = player_data['first_name'] + ' ' + player_data['last_name']

    return render_template('pctile.html', player_data=player_data, name=name, avg_marks=avg_marks, ll_marks_with_names=ll_marks_with_names, json_data=json_data)
