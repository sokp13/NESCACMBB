from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfghjkl'  # Change this to a random secret key

# Import other blueprints as needed
from index import home_bp  # Import the Blueprint instance
from player_views import player_views
from team_views import team_views
from tag_views import tag_views
from pctile import pctile

app.register_blueprint(home_bp, url_prefix='/home')  # Register the Blueprint instance
app.register_blueprint(player_views, url_prefix='/players')
app.register_blueprint(team_views, url_prefix='/teams')
app.register_blueprint(tag_views, url_prefix='/players')
app.register_blueprint(pctile, url_prefix='/players')

if __name__ == '__main__':
    app.run(debug=True)