from compareplayer import compare
from flask import Flask, render_template, url_for, redirect, request, Response
from searchbyplayer import search
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats as psc
import pandas
from plotly.offline import plot
from plotly.graph_objs import Scatter

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
    fgmfan = Search.fgmfan.data
    fgafan = Search.fgafan.data
    tovfan = Search.tovfan.data
    rebfan = Search.rebfan.data
    astfan = Search.astfan.data
    pointsfan = Search.pointsfan.data
    stlsfan = Search.stlsfan.data
    blkfan = Search.blkfan.data
    if Search.validate_on_submit():
        session["name"] = result
        session["fgmfan"] = fgmfan
        session["fgafan"] = fgafan
        session["tovfan"] = tovfan
        session["rebfan"] = rebfan
        session["astfan"] = astfan
        session["pointsfan"] = pointsfan
        session["stlsfan"] = stlsfan
        session["blkfan"] = blkfan

        
        return redirect(url_for('result'))
    return render_template('searchbyplayer.html', Search=Search)

@app.route('/results.html', methods=["GET"])
def result():
    res = session.get("name")
    fgafan = float(session.get("fgafan"))
    fgmfan = float(session.get("fgmfan"))
    tovfan = float(session.get("tovfan"))
    rebfan = float(session.get("rebfan"))
    astfan = float(session.get("astfan"))
    pointsfan = float(session.get("pointsfan"))
    stlsfan = float(session.get("stlsfan"))
    blkfan = float(session.get("blkfan"))
    player_dict = players.find_players_by_full_name(res)
    career = psc.PlayerCareerStats(player_id=player_dict[0]['id']).get_data_frames()[0]
    career = pandas.DataFrame(career)
    career.pop("PLAYER_ID")
    career.pop("TEAM_ID")
    career.pop("LEAGUE_ID")
    career.columns = ['Season', 'Team', 'Age', 'GP', 'GS', 'Min', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA',
       'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF','PTS']
    ppg = []
    tov = []
    blk= []
    ast = []
    oreb = []
    dreb = []
    fgm=[]
    fga=[]
    fg3m=[]
    fg3a=[]
    min=[]
    reb=[]
    stl=[]
    fanpts = []
    ''' calculation for fantasy points: 
        ppg*multiplier + assists*multiplier + rebounds*multiplier - turnovers*multiplier - fga*multiplier + fgm*multiplier
    '''
    
    for i in range(len(career['PTS'])):
       ppg+=[round(career['PTS'][i]/career['GP'][i], 2)]
       tov += [round(career['TOV'][i]/career['GP'][i], 2)]
       blk += [round(career['BLK'][i]/career['GP'][i], 2)]
       ast += [round(career['AST'][i]/career['GP'][i], 2)]
       oreb += [round(career['OREB'][i]/career['GP'][i], 2)]
       dreb += [round(career['DREB'][i]/career['GP'][i], 2)]
       fgm += [round(career['FGM'][i]/career['GP'][i], 2)]
       fga += [round(career['FGA'][i]/career['GP'][i], 2)]
       fg3m += [round(career['FG3M'][i]/career['GP'][i], 2)]
       fg3a += [round(career['FG3A'][i]/career['GP'][i], 2)]
       min += [round(career['Min'][i]/career['GP'][i], 2)]
       reb += [round(career['REB'][i]/career['GP'][i], 2)] 
       stl+=[round(career['STL'][i]/career['GP'][i], 2)]
       fanpts+=[round((ppg[i]*pointsfan) + (ast[i]*astfan) + (reb[i]*rebfan) - (tov[i]*tovfan) - (fga[i] * fgafan) + (fgm[i] * fgmfan) + (stl[i]*stlsfan) + (blk[i]*blkfan), 2)]

    career['PPG']=ppg
    career['TOV']=tov
    career['BLK']=blk
    career['AST']=ast
    career['OREB']=oreb
    career['DREB']=dreb
    career['FGM']=fgm
    career['FGA']=fga
    career['FG3M']=fg3m
    career['FG3A']=fg3a
    career['Min']=min
    career['REB']=reb
    career['STL']=stl
    career['Fantasy Points Estimate']=fanpts
    career.pop("GS")
    career.pop("FG3_PCT")
    career.pop("FG_PCT")
    career.pop("FT_PCT")
    career.pop("FTM")
    career.pop("FTA")
    career.pop('PTS')
    career.pop("PF")

    season = [row for row in career['Season']]
    values = [round(row,2) for row in career['PPG']]
    plot_div = plot([Scatter(x=season, y=values,
                mode='lines', name='test', opacity=1, marker_color='red')], output_type='div')
    first_name = res.split(" ")[:1][0]
    last_name = res.split(" ")[1:][0]
    link = f"https://nba-players.herokuapp.com/players/{last_name}/{first_name}"
    
    return render_template('results.html', names=res, tables=[career.to_html(classes='table table-striped table-hover')], season=season, values=values, plot_div = plot_div, link_ = link, res_ = res)


@app.route('/comparebyplayer.html', methods=['GET'])
def comparebyplayer():
    Compare = compare()
    name1 = Compare.name1.data
    name2 = Compare.name1.data
    fgmfan = Compare.fgmfan.data
    fgafan = Compare.fgafan.data
    tovfan = Compare.tovfan.data
    rebfan = Compare.rebfan.data
    astfan = Compare.astfan.data
    pointsfan = Compare.pointsfan.data
    stlsfan = Compare.stlsfan.data
    blkfan = Compare.blkfan.data
    


    return render_template('comparebyplayer.html', )  

if __name__ == "__main__":
    app.run(debug=True)
 