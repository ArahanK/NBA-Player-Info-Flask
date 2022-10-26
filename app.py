from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
from searchbyplayer import search
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats as psc
import pandas


session = dict()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'arahan'
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/searchbyplayer.html', methods=["GET", "POST"])
def searchbyplayer():
    Search = search()
    result = Search.name.data
    if Search.validate_on_submit():
        session["var"] = result
        print("CHEK")
        return redirect(url_for('result'))
    return render_template('searchbyplayer.html', Search=Search)

@app.route('/results.html', methods=["GET"])
def result():
    res = session.get("var")
    print(type(res))
    player_dict = players.find_players_by_full_name(res)
    career = psc.PlayerCareerStats(player_id=player_dict[0]['id']).get_data_frames()[0]
    career = pandas.DataFrame(career)
    career.pop("PLAYER_ID")
    career.pop("TEAM_ID")
    career.pop("LEAGUE_ID")
    career.columns=['Season', 'Team', 'Age', 'GP', 'GS', 'Min', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA',
       'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF','PTS']
    ppg = []
    for i in range(len(career['PTS'])):
        ppg+=[round(career['PTS'][i]/career['GP'][i], 2)]
    
    career['PPG']=ppg
    
    return render_template('results.html', names=res, tables=[career.to_html(classes='table table-striped table-hover')], titles=career.columns.values)

if __name__ == "__main__":
    app.run(debug=True)
 