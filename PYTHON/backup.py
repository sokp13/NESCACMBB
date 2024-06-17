import pandas as pd
import numpy as np
from loader import load_data_no_dict
from flask import Blueprint, render_template
from scipy.stats import percentileofscore

def per_game(val, gp):
    return val/gp

def efg(fgm, tfgm, fga):
    return 100*(fgm+(1.5*tfgm))/fga

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

# league_fg_avg = round(100*(db['fgm'].sum() / db['fga'].sum()), 1)
# league_three_avg = round(100*(db['threem'].sum() / db['threea'].sum()), 1)
# league_ft_avg = round(100*(db['ftm'].sum() / db['fta'].sum()), 1)

avg_ts = round(ts_pct(db['pts'].sum(), db['fga'].sum(), db['fta'].sum()), 1)
avg_eFG = round(efg(db['fgm'].sum(), db['threem'].sum(), db['fga'].sum()), 1)
avg_atr = round(per_game(db['ast'].sum(), db['to'].sum()))
avg_PER = round(player_eff(db['pts'].sum(), db['reb'].sum(), db['ast'].sum(), db['stl'].sum(), db['blk'].sum(),
                       (db['fga'].sum() - db['fgm'].sum()), (db['fta'].sum() - db['ftm'].sum()), db['to'].sum(),
                       db['poss'].sum(), db['games'].sum(), db['team_poss'].sum()))

db['Qualify'] = 'DNQ'
db.loc[((db['fga'] + db['threea'] + db['fta']) >= 75), 'Qualify'] = 'Qualified'

# db['FG%'] = np.where(db['fga'] != 0, round(100*(db['fgm'] / db['fga']), 1), 0)
# db['3PT%'] = np.where(db['threea'] != 0, round(100*(db['threem'] / db['threea']), 1), 0)
# db['FT%'] = np.where(db['fta'] != 0, round(100*(db['ftm'] / db['fta']), 1), 0)
db['PER'] = player_eff(db['pts'], db['reb'], db['ast'], db['stl'], db['blk'],
                       (db['fga'] - db['fgm']), (db['fta'] - db['ftm']), db['to'],
                       db['poss'], db['games'], db['team_poss'])
db['TS%'] = ts_pct(db['pts'], db['fga'], db['fta'])
db['eFG%'] = efg(db['fgm'], db['threem'], db['fga'])
db['atr'] = per_game(db['ast'], db['to'])

db['ppg'] = round(per_game(db['pts'], db['games']), 1)
db['rpg'] = round(per_game(db['reb'], db['games']), 1)
db['apg'] = round(per_game(db['ast'], db['games']), 1)
db['spg'] = round(per_game(db['stl'], db['games']), 1)
db['bpg'] = round(per_game(db['blk'], db['games']), 1)

db.fillna(0, inplace=True)

db['PER_pctile'] = round(db['PER'].apply(lambda x: percentileofscore(db['PER'], x)), 0)
db['TS%_pctile'] = round(db['TS%'].apply(lambda x: percentileofscore(db['TS%'], x)), 0)
db['eFG%_pctile'] = round(db['eFG%'].apply(lambda x: percentileofscore(db['eFG%'], x)), 0)
db['atr_pctile'] = round(db['eFG%'].apply(lambda x: percentileofscore(db['eFG%'], x)), 0)

db['pts_rank'] = round(db['ppg'].apply(lambda x: percentileofscore(db['ppg'], x)), 0)
db['reb_rank'] = round(db['rpg'].apply(lambda x: percentileofscore(db['rpg'], x)), 0)
db['ast_rank'] = round(db['apg'].apply(lambda x: percentileofscore(db['apg'], x)), 0)
db['stl_rank'] = round(db['spg'].apply(lambda x: percentileofscore(db['spg'], x)), 0)
db['blk_rank'] = round(db['bpg'].apply(lambda x: percentileofscore(db['bpg'], x)), 0)

@pctile.route('/<int:player_id>/ranks')
def player_pctiles(player_id):
    player_data = db[db['id'] == player_id].iloc[0]
    
    name = player_data['first_name'] + ' ' + player_data['last_name']
    return render_template('pctile.html', player_data=player_data, name=name, avg_ts=avg_ts, avg_eFG=avg_eFG, avg_atr=avg_atr, avg_PER=avg_PER)
