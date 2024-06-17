import math
from flask import Blueprint, render_template
from loader import load_data_from_csv

team_views = Blueprint('team', __name__)

@team_views.route('/<team_id>')
def team_profile(team_id):
    team_data = load_data_from_csv('csv/rawplayerdata.csv')
    team = next((t for t in team_data if (t['team_id']) == team_id), None)

    if team:
        players_data = load_data_from_csv('csv/rawplayerdata.csv')
        team_players = [p for p in players_data if p['team_id'] == team_id]

        roster = sorted(team_players, key=lambda x: int(x['number']))

        team['games'] = int(team['wins']) + int(team['losses'])
        team['t_ppg'] = round(int(team['team_pts'])/int(team['games']), 1)
        team['t_fg_pct'] = round(100*int(team['team_fgm'])/int(team['team_fga']), 1)
        team['t_th_pct'] = round(100*int(team['team_threem'])/int(team['team_threea']), 1)

        return render_template('team_profile.html', team=team, roster=roster)
    else:
        return "Team not found"