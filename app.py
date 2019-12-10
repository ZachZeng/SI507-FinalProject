from flask import Flask, render_template, request
import model
import plotly
import plotly.graph_objects as go
import numpy as np
import json
from flask import make_response

# your code goes here
app = Flask(__name__)



@app.route('/',methods=['GET', 'POST'])
def index():
    pie_results = model.get_platform_percentage()
    labels = []
    values = []
    for result in pie_results:
        labels.append(result[0])
        values.append(int(result[1]))

    pie_trace = go.Pie(labels=labels, values=values,
               hoverinfo='label+value', textinfo='label',
               textfont=dict(size=10),
               marker=dict(line=dict(color='#fff', width=1)),
               hole=.3,
               automargin=True,
               )
    
    
    pie_data = [pie_trace]
    pie_graphJSON = json.dumps(pie_data, cls=plotly.utils.PlotlyJSONEncoder)
    
    bar_results = model.get_platform_ratings()

    xScale = []
    yScale = []

    for result in bar_results:
        xScale.append(result[0])
        yScale.append(round(result[1],2))


    bar_trace = go.Bar(
        x = xScale,
        y = yScale,
    )

    bar_data = [bar_trace]
    bar_graphJSON = json.dumps(bar_data, cls=plotly.utils.PlotlyJSONEncoder)


    platform_top_games = model.get_platform_top()
    top_platform_game_result = ''
    game_detail_result = ''
    
    if request.method == 'POST':
        if request.form['prodId'] == 'form_platform':
            for i in platform_top_games:
                if(i.platform == request.form['platform']):
                    top_platform_game_result = i
                    break
        else:
            game_name = request.form['gamename']
            game_detail_result = model.get_game_detail(game_name)
    else:
        game_name = ''
        game_detail_result = ''
        top_platform_game_result = ''



    resp = make_response(render_template('index.html', pie_graphJSON=pie_graphJSON, bar_graphJSON=bar_graphJSON, platform_top_games=platform_top_games, top_platform_game_result=top_platform_game_result,game_detail_result=game_detail_result))
    resp.set_cookie('sessionID', '', expires=0)
    return resp


if __name__ == '__main__':
    app.run(debug=True) 