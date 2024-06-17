import math
from flask import Blueprint, render_template
from loader import load_data_from_csv

tag_views = Blueprint('tag', __name__)

def div(a, b):
    if b == 0:
        return 0
    else:
        return a/b

# SHOOTING
def volume_shooter(fga, gp):
    return div(fga, gp) >= 12

def floor_spacer(tpm, tpa, fga):
    tp_fg = div(tpm, tpa)
    return tp_fg >= 0.30 and tpa >= 8

def catch_n_shoot(cs_poss, cs_pts):
    return cs_poss >= 15 and div(cs_pts, cs_poss) >= 0.9

def free(fta):
    return fta >= 75

# FINISHING
def paint_masher(rim_pts, rim_poss, fga):
    ppp = div(rim_pts, rim_poss)
    return ppp >= 1 and div(rim_poss, fga) >= 0.6

def post_player(post_pts, post_poss, post_fga):
    # ppp = div(post_pts, post_poss)
    return post_fga >= 25

def above_the_rim(dunks):
    return dunks >= 5

# PLAYMAKING
def prof_passer(ast, gp):
    return div(ast, gp) >= 3.5

def pr_play(pr_poss):
    return pr_poss >= 35

def iso_threat(iso_poss, iso_pts):
    iso_ppp = div(iso_pts, iso_poss)
    return iso_poss >= 8 and iso_ppp >= 0.8

# DEFENDING/REBOUNDING
def per_stop(pd_pts, pd_poss):
    ppp = div(pd_pts, pd_poss)
    return ppp <= 0.6 and pd_poss >= 50

def post_stop(intd_pts, intd_poss, ht):
    ppp = div(intd_pts, intd_poss)
    return ppp <= 0.6 and intd_poss >= 25 and ht >= 76

def board(reb, gp):
    return div(reb, gp) >= 5

def thief(stl, gp):
    return div(stl, gp) >= 1.5

def trans(tr_fgm, tr_fga):
    return div(tr_fgm, tr_fga) >= 0.45 and tr_fga >= 35

def cutter(cut_poss):
    return cut_poss >= 15


##### Height (ignore)
def height(inches):
    feet = (str)(math.floor(inches/12))
    inch = (str)(round(inches%12))

    out = "" + feet + "'" + inch + "''"
    return out


@tag_views.route('/<int:player_id>/tags')
def tag_profile(player_id):
    players_data = load_data_from_csv('csv/rawplayerdata.csv')
    player = next((p for p in players_data if int(p['id']) == player_id), None)

    if player:
        
        player['height'] = height(player['height_in'])

        tags = []
        if volume_shooter(player['fga'], player['games']):
            tags.append("Gunner")

        if floor_spacer(player['threem'], player['threea'], player['fga']):
            tags.append("Floor Spacer")

        if catch_n_shoot(player['cs_poss'], player['cs_pts']):
            tags.append("Catch and Shoot")

        if paint_masher(player['rim_pts'], player['rim_poss'], player['fga']):
            tags.append("Paint Masher")

        if post_player(player['post_pts'], player['post_poss'], player['post_fga']):
            tags.append("Set-Up Shop")

        if above_the_rim(player['dunk_fgm']):
            tags.append("Above the Rim")

        if prof_passer(player['ast'], player['games']):
            tags.append("Proficient Passer")

        if pr_play(player['prb_poss']):
            tags.append("Pick & Roll Playmaker")

        if iso_threat(player['iso_poss'], player['iso_pts']):
            tags.append("Isolation Threat")

        if per_stop(player['pd_pts'], player['pd_poss']):
            tags.append("Perimeter Detterent")

        if post_stop(player['intd_pts'], player['intd_poss'], player['height_in']):
            tags.append("Rim Detterent")

        if board(player['reb'], player['games']):
            tags.append("Glass Cleaner")

        if thief(player['stl'], player['games']):
            tags.append("Pesky Hands")

        if thief(player['trans_fgm'], player['trans_fga']):
            tags.append("Transition Threat")

        if cutter(player['cut_poss']):
            tags.append("Off-Ball Threat")

        if free(player['fta']):
            tags.append("Charity Stripe")

        tag_desc = {
            # Perimeter Shooting
            "Gunner": "Takes a high number of shots per game",
            "Floor Spacer": "Stretches the floor with three-point shooting",
            "Catch and Shoot": "Efficient catch-and-shoot player",
            # Inside Scoring
            "Paint Masher": "Attacks the rim effectively",
            "Set-Up Shop": "Posts up on the block routinely",
            "Above the Rim": "Finishes above the cylinder",
            # Playmaking
            "Proficient Passer": "Totals high assist numbers",
            "Pick & Roll Playmaker": "Has a heavy pick & roll load",
            "Isolation Threat": "Tends to create in isolation",
            # Defense/Rebounding
            "Perimeter Detterent": "Prevents scoring on the perimeter",
            "Rim Detterent": "Prevents scoring at the rim",
            "Pesky Hands": "Grabs a high number of steals",
            "Glass Cleaner": "Collects a high number of rebounds",
            # Other
            "Transition Threat": "Effiecient scorer on the break",
            "Off-Ball Threat": "Active cutting for scores off the ball",
            "Charity Stripe": "Generates many free throw attempts"
        }

        name = player['first_name'] + " " + player['last_name']
        team = player['team_name']

        return render_template('tag_profile.html', tags=tags, tag_desc=tag_desc, team=team, player=player, name=name)
    else:
        return "Player not found"  # Handle the case where the player doesn't exist