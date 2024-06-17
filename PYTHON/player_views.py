import math
import pandas as pd
from pandas import Series
from flask import Blueprint, render_template
from loader import load_data_from_csv
from awards_backend import mvp_model_instance

player_views = Blueprint('player', __name__)
players_data = load_data_from_csv('csv/rawplayerdata.csv')

########## Advanced Statistics ######
def per_div(a, b):
    try:
        if b == 0:
            return 0
        else:
            return float(a/b)
    except ValueError:
        return 0
def efg(fgm, tfgm, fga):
    if fga == 0:
        return 0
    else:
        return (fgm+(0.5*tfgm))/fga
def ts_pct(pts, fga, fta):
    if fga == 0:
        return 0
    else:
        return float(pts/(2*(fga +(0.44*fta))))
def tov_pct(tov, fga, fta):
    if (fga + 0.44*fta + tov) != 0:
        out = tov / (fga + 0.44*fta + tov)
        return out
    else:
        return 0.0

def height(inches):
    feet = (str)(math.floor(inches/12))
    inch = (str)(round(inches%12))

    out = "" + feet + "'" + inch + "''"
    return out

# Other #
def usage(pts, fg_miss, tov, ft_miss, team_poss):
    out = (pts + fg_miss + (0.44*ft_miss) + tov)/team_poss
    return out

######### Player Ratings #####
def player_eff(pts, reb, ast, stl, blk, fg_miss, ft_miss, tov, poss, gp, team_poss):
    if gp == 0:
        return "N/A"
    else:
        ur = 100*usage(pts, fg_miss, tov, ft_miss, team_poss)
        per_poss = (pts + reb + ast + stl + blk - fg_miss - ft_miss - tov) / (team_poss / gp)

        combined_metric = (0.7 * per_poss) + (0.3 * ur)

        return round(combined_metric, 2)
def offRtg(pts, ast, poss):
    if poss == 0:
        return "N/A"
    else:
        points_prod = pts + (2*ast/3)
        return round(100*(points_prod/poss), 1)
def defRtg(pts, poss):
    if poss == 0:
        return "N/A"
    else:
        return round(10*(pts/poss), 1)
    
def get_class(pClass):
    return pClass == "Freshman"

###### PER INSERTION ######
players_data.sort(key=lambda x: x['id']) 

for player in players_data:
   player['PER'] = player['PER'] = player_eff(player['pts'], player['reb'], player['ast'], player['stl'], player['blk'],
                                              (player['fga']-player['fgm']), (player['fta']-player['ftm']), player['to'],
                                              player['poss'], player['games'], player['team_poss'])


@player_views.route('/<int:player_id>')
def player_profile(player_id):
    #mvp_percentiles
    player = next((p for p in players_data if int(p['id']) == player_id), None)

    if player:
        player['height'] = height(player['height_in'])
        # Calculate statistics and add them to the player dictionary

        pts = int(player['pts'])
        reb = int(player['reb'])
        ast = int(player['ast'])
        blk = int(player['blk'])
        stl = int(player['stl'])
        tov = int(player['to'])

        pts_against = player['intd_pts'] + player['pd_pts']
        poss_against = player['intd_poss'] + player['pd_poss']

        poss = int(player['poss'])
        fgm = int(player['fgm'])
        fga = int(player['fga'])
        tpm = int(player['threem'])
        tpa = int(player['threea'])
        ftm = int(player['ftm'])
        fta = int(player['fta'])
        gp = int(player['games'])

        ###### Ratings
        player['oRtg'] = offRtg(pts, ast, player['team_poss'])
        player['dRtg'] = defRtg(pts_against, poss_against)

        ###### Awards Formulas
        # player['MVP_rank'] = percentiles[player['id']]
        
        ###### Per game numbers
        player['ppg'] = round(per_div(pts, gp), 1)
        player['rpg'] = round(per_div(reb, gp), 1)
        player['apg'] = round(per_div(ast, gp), 1)
        player['bpg'] = round(per_div(blk, gp), 1)
        player['spg'] = round(per_div(stl, gp), 1)
        
        ###### Scoring efficiency metrics
        player['ppp'] = round(per_div(pts, poss), 3)
        player['fg_pct'] = round(100*per_div(fgm, fga), 1)
        player['thr_fg_pct'] = round(100*per_div(tpm, tpa), 1)
        player['ft_pct'] = round(100*per_div(ftm, fta), 1)
        player['efg'] = round(100*efg(fgm, tpm, fga), 1)
        player['ts_pct'] = round(100*ts_pct(pts, fga, fta), 1)
        player['post_fg'] = round(100*per_div(int(player['post_fgm']), int(player['post_fga'])), 1)
        player['rim_fg'] = round(100*per_div(int(player['rim_fgm']), int(player['rim_poss'])), 1)
        player['post_ppp'] = round(per_div(player['post_pts'], player['post_poss']), 3)

        ###### Ball-handling efficiency
        player['atr'] = round(per_div(ast, tov), 2)
        player['prb_ppp'] = round(per_div(player['prb_pts'], player['prb_poss']), 3)
        player['usage'] = round(100*usage(pts, (fga-fgm), tov, (fta-ftm), player['team_poss']), 1)
        player['tov_pct'] = round(100*tov_pct(tov, fga, fta), 1)
        
        ###### Defensive Ratings
        player['intd_fg_pct'] = round(100*per_div(int(player['intd_fgm']), int(player['intd_fga'])), 1)
        player['intd_ppp'] = round(per_div(int(player['intd_pts']), int(player['intd_poss'])), 1)
        player['pd_fg_pct'] = round(100*per_div(int(player['pd_fgm']), int(player['pd_fga'])), 1)
        player['pd_ppp'] = round(per_div(int(player['pd_pts']), int(player['pd_poss'])), 1)

        name = player['first_name'] + " " + player['last_name']
        ID = (str)(player['id'])
        team = player['team_name']

        return render_template('player_profile.html', player=player, name=name, ID=ID, team=team)
    else:
        return "Player not found"  # Handle the case where the player doesn't exist
