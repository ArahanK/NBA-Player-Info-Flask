from compareplayer import compare
from flask import Flask, render_template, url_for, redirect, request, Response
from searchbyplayer import search
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats as psc
import pandas
from plotly.offline import plot
from plotly.graph_objs import Scatter, Layout, Figure

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


@app.route('/comparebyplayer.html', methods=['GET', 'POST'])
def comparebyplayer():
    Compare = compare()
    name1 = Compare.name1.data
    name2 = Compare.name2.data
    if Compare.validate_on_submit():
        session['name1']=name1
        session['name2']=name2
        
        return redirect(url_for('result2'))

    return render_template('comparebyplayer.html', Search=Compare)  

@app.route('/results2.html', methods=['GET'])
def result2(): 
    ppg1 = []
    ppg2 = []
    name1 = session.get("name1")
    name2 = session.get("name2")
    player1_dict = players.find_players_by_full_name(name1)
    player2_dict = players.find_players_by_full_name(name2)
    career1 = psc.PlayerCareerStats(player_id=player1_dict[0]['id']).get_data_frames()[0]
    career1 = pandas.DataFrame(career1)
    career2 = psc.PlayerCareerStats(player_id=player2_dict[0]['id']).get_data_frames()[0]
    career2 = pandas.DataFrame(career2)
    ppg1+=[round(career1['PTS'][i]/career1['GP'][i], 2) for i in range(len(career1['PTS']))]
    ppg2+=[round(career2['PTS'][i]/career2['GP'][i], 2) for i in range(len(career2['PTS']))] 
    points1 = ppg1[len(ppg1)-1]
    points2 = ppg2[len(ppg2)-1]
    ast1 = (career1['AST'][len(career1['AST'])-1])/career1['GP'][len(career1['GP'])-1]
    ast2 = (career2['AST'][len(career2['AST'])-1])/career2['GP'][len(career2['GP'])-1]
    reb1 = career1['REB'][len(career1['REB'])-1]/career1['GP'][len(career1['GP'])-1]
    reb2 = career2['REB'][len(career2['REB'])-1]/career2['GP'][len(career1['GP'])-1]
    tov1 = career1['TOV'][len(career1['TOV'])-1]/career1['GP'][len(career1['GP'])-1]
    tov2 = career2['TOV'][len(career2['TOV'])-1]/career2['GP'][len(career1['GP'])-1]
    blk1 = career1['BLK'][len(career1['BLK'])-1]/career1['GP'][len(career1['GP'])-1]
    blk2 = career2['BLK'][len(career2['BLK'])-1]/career2['GP'][len(career1['GP'])-1]
    stl1 = career1['STL'][len(career1['BLK'])-1]/career1['GP'][len(career1['GP'])-1]
    stl2 = career2['STL'][len(career2['BLK'])-1]/career2['GP'][len(career1['GP'])-1]
    ast1 = round(ast1, 2)
    ast2 = round(ast2, 2)
    reb1 = round(reb1, 2)
    reb2 = round(reb2, 2)
    tov1 = round(tov1, 2)
    tov2 = round(tov2, 2)
    blk1 = round(blk1, 2)
    blk2 = round(blk2, 2)
    stl1 = round(stl1, 2)
    stl2 = round(stl2, 2)
    first_name1 = name1.split(" ")[:1][0]
    last_name1 = name1.split(" ")[1:][0]
    first_name2 = name2.split(" ")[:1][0]
    last_name2 = name2.split(" ")[1:][0]
    career1['PPG1'] = ppg1
    career2['PPG2'] = ppg2
    link1 = f"https://nba-players.herokuapp.com/players/{last_name1}/{first_name1}"
    link2 = f"https://nba-players.herokuapp.com/players/{last_name2}/{first_name2}"
    # season1 = [row for row in career1['Season']]
    # values1 = [row for row in ppg1]
    # season2 = [row for row in career2['Season']]
    # values2 = [row for row in ppg2]
    season1 = [row for row in career1['SEASON_ID']]
    values1 = [round(row,2) for row in career1['PPG1']]
    season2 = [row for row in career2['SEASON_ID']]
    values2 = [round(row,2) for row in career2['PPG2']]
    trace0 = Scatter(x=season2, y=values1, mode='lines', name=name1)
    trace1 = Scatter(x=season2, y=values2, mode='lines', name=name2)
    data = [trace1, trace0]
    layout = Layout(title = "Graph")
    figure = Figure(data = data, layout = layout)
    plot_div = plot(figure, output_type='div')                

    return render_template("results2.html", name1 = name1, name2 = name2, link1 = link1, link2 = link2, points1 = points1, points2 = points2, ast1 = ast1, ast2 = ast2, reb1 = reb1, reb2 = reb2, tov1 = tov1, tov2 = tov2, blk1 = blk1, blk2 = blk2, stl1 = stl1, stl2 = stl2, plot_div = plot_div)



if __name__ == "__main__":
    app.run(debug=True)
 