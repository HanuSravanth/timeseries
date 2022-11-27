from flask import Flask, render_template, request
import os
import pickle
import requests
import pandas as pd
import plotly.graph_objects as go
from kats.models.prophet import ProphetModel, ProphetParams
from kats.models.sarima import SARIMAModel, SARIMAParams
from kats.consts import TimeSeriesData

from model_train_forecast import * 

print("running flask app...")
forecast_app = Flask(__name__)

if "forecast.html" in os.listdir(f"{os.getcwd()}\\templates\\"):
    os.remove(f"{os.getcwd()}\\templates\\" + "forecast.html")

@forecast_app.route('/')
@forecast_app.route('/home')
def index():
    return render_template('index.html')

@forecast_app.route('/inputform')
def inputForm():
    return render_template('input_form.html')

@forecast_app.route('/plot')
def plot():
    return render_template('blank_plot.html')

@forecast_app.route('/forecast_plot')
def forecast_plot():
    return render_template('forecast.html')

@forecast_app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # save the input file as csv
        f = request.files['input_file']
        f.save(f"{os.getcwd()}\\user_inputs\\" + "input_file.csv")
        parameters_dict = { 
                            'time_col'    : request.form['time_col'],
                            'value_col'   : request.form['value_col'],
                            'pred_length' : request.form['pred_length']
                          }
        # save the input parameters as pickle file
        with open(f"{os.getcwd()}\\user_inputs\\" + "in_parms.pickle", 'wb') as handle:
            pickle.dump(parameters_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


        with open(f"{os.getcwd()}\\user_inputs\\" + "in_parms.pickle", 'rb') as handle:
            parameters_dict = pickle.load(handle)

        input_df = pd.read_csv(f"{os.getcwd()}\\user_inputs\\" + "input_file.csv", parse_dates=[parameters_dict["time_col"]])
        input_df = input_df[[parameters_dict["time_col"], parameters_dict["value_col"]]]

        model_train_forecast(input_df, parameters_dict)

        # # create TimeSeriesData
        # tsdata = TimeSeriesData(time=input_df[parameters_dict["time_col"]], value=input_df[parameters_dict["value_col"]])

        # # create SARIMA param class
        # params = SARIMAParams(p = 2, d=1, q=1, trend = 'ct', seasonal_order=(1,0,1,12))

        # # initiate SARIMA model
        # m = SARIMAModel(data=tsdata, params=params)

        # # fit SARIMA model
        # m.fit()

        # # generate forecast values
        # fcst = m.predict(steps=int(parameters_dict["pred_length"]), freq="D")

        # fig = go.Figure()

        # fig.add_trace(go.Scatter(x=m.data.time, y=m.data.value, name='training data', line=dict(color='blue')))
        # # fig.add_trace(go.Scatter(x=tsdf_test.Date, y=tsdf_test.Close, name='test data', line=dict(color='green')))

        # fig.add_trace(go.Scatter(x=m.fcst_df.time, y=m.fcst_df.fcst, name='forecast', line=dict(color='red')))

        # fig.add_trace(go.Scatter(
        #     x=list(m.fcst_df.time)+list(m.fcst_df.time)[::-1],
        #     y=list(m.fcst_df.fcst_upper)+list(m.fcst_df.fcst_lower)[::-1],
        #     fill='toself',
        #     fillcolor='rgba(255,0,0,0.2)',
        #     line_color='rgba(255,255,255,0)',
        #     name='Confidence Interval',
        #     showlegend=True,
        # ))

        # fig.add_vline(x=(m.fcst_df['time'].values)[0], line_width=2, line_dash="dash", line_color="black")

        # fig.update_layout(
        #     title       = '<b>Forecast</b>',
        #     title_x     = 0.5,
        #     xaxis_title = f"<b>{parameters_dict['time_col']}</b>",
        #     yaxis_title = f"<b>{parameters_dict['value_col']}</b>",
        #     height      = 780,
        #     width       = 1480,
            
        # )

        # # fig.show()

        # # fig.write_html(f"{os.getcwd()}\\templates\\" + "forecast.html")

        # plot_html = fig.to_html(f"{os.getcwd()}\\templates\\" + "forecast.html")
        # plot_html = plot_html.replace("<body>", "<form action='http://localhost:5000/forecast_plot'><center><input type='submit' value='Refresh'></center></form>")

        # with open(f"{os.getcwd()}\\templates\\" + "forecast.html", "w") as file:
        #     file.write(plot_html)

        # # requests.get('http://localhost:5000/').content 
        
        # return render_template('upload_file.html')

        return f"""
    <h3>File upload successful!</h3>
    <p>Parameters passed:</p>
    <p>Time Column: {parameters_dict['time_col']}</p>
    <p>Value Column: {parameters_dict['value_col']}</p>
    <p>Forecast Length: {parameters_dict['pred_length']}</p>
    <h3>Press refresh button to see the forecast plot!</h3>
    <br>
    <p>Refresh page for another forecast!</p>
        """


if __name__ == "__main__":
    forecast_app.run(debug=True)