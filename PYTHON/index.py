from flask import Flask, Blueprint, render_template
from loader import load_data_from_csv
from player_views import usage, per_div

home_bp = Blueprint('home', __name__)
players_data = load_data_from_csv('csv/rawplayerdata.csv')

def player_eff(pts, reb, ast, stl, blk, fg_miss, ft_miss, tov, poss, gp, team_poss):
    if gp == 0:
        return 0
    else:
        ur = 100*usage(pts, fg_miss, tov, ft_miss, team_poss)
        per_poss = (pts + reb + ast + stl + blk - fg_miss - ft_miss - tov) / (team_poss / gp)

        combined_metric = (0.7 * per_poss) + (0.3 * ur)
        return combined_metric
    
def defRtg(pts, poss):
    if poss == 0:
        return "N/A"
    else:
        return round(10*(pts/poss), 1)
    
a = []

for player in players_data:
    pts_against = player['intd_pts'] + player['pd_pts']
    poss_against = player['intd_poss'] + player['pd_poss']
    stocks = player['blk'] + player['stl']

    player['PER'] = player_eff(player['pts'], player['reb'], player['ast'], player['stl'], player['blk'],
                               (player['fga'] - player['fgm']), (player['fta'] - player['ftm']), player['to'],
                               player['poss'], player['games'], player['team_poss'])
    
    player['ppg'] = round(per_div(player['pts'], player['games']), 1)
    player['rpg'] = round(per_div(player['reb'], player['games']), 1)
    player['apg'] = round(per_div(player['ast'], player['games']), 1)
    player['FG%'] = round(100*per_div(player['fgm'], player['fga']), 1)
    player['3PT%'] = round(100*per_div(player['threem'], player['threea']), 1)
    player['FT%'] = round(100*per_div(player['ftm'], player['fta']), 1)
    player['DRtg'] = round((100*per_div(pts_against, poss_against))/(stocks+0.4), 1)

    a.append({
        'name': player['first_name'] + ' ' + player['last_name'],
        'team_id': player['team_id'],
        'id': player['id'],
        'class': player['class'],
        'PER':  player['PER'],
        'dposs': poss_against,
        'poss': player['poss'],
        'ppg': player['ppg'],
        'rpg': player['rpg'],
        'apg': player['apg'],
        'FG%': player['FG%'],
        '3PT%': player['3PT%'],
        'FT%': player['FT%'],
        'DRtg': player['DRtg']
    })


@home_bp.route('/')
def index():
    top_players = sorted(a, key=lambda x: x['PER'], reverse=True)[:10]
    scoring = sorted(a, key=lambda x: x['ppg'], reverse=True)[:5]
    rebounding = sorted(a, key=lambda x: x['rpg'], reverse=True)[:5]
    passing = sorted(a, key=lambda x: x['apg'], reverse=True)[:5]

    freshmen = list(filter(lambda x: x['class'] == 'Freshman', a))
    top_frosh = sorted(freshmen, key=lambda x: x['PER'], reverse=True)[:7]

    filtered_topdef = filter(lambda x: x['dposs'] >= 75, a)
    top_def = sorted(filtered_topdef, key=lambda x: x['DRtg'], reverse=False)[:7]


    # print(top_players)

    return render_template('index.html', top_players=top_players, scoring=scoring, passing=passing, rebounding=rebounding,
                           top_frosh=top_frosh, top_def=top_def)