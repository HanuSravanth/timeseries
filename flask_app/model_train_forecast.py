from kats.models.prophet import ProphetModel, ProphetParams
from kats.models.sarima import SARIMAModel, SARIMAParams
from kats.consts import TimeSeriesData

import os
import pandas as pd
import plotly.graph_objects as go


def model_train_forecast(input_df, parameters_dict):
# create TimeSeriesData
        tsdata = TimeSeriesData(time=input_df[parameters_dict["time_col"]], value=input_df[parameters_dict["value_col"]])

        # create SARIMA param class
        params = SARIMAParams(p = 2, d=1, q=1, trend = 'ct', seasonal_order=(1,0,1,12))

        # initiate SARIMA model
        m = SARIMAModel(data=tsdata, params=params)

        # fit SARIMA model
        m.fit()

        # generate forecast values
        fcst = m.predict(steps=int(parameters_dict["pred_length"]), freq="D")

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=m.data.time, y=m.data.value, name='training data', line=dict(color='blue')))
        # fig.add_trace(go.Scatter(x=tsdf_test.Date, y=tsdf_test.Close, name='test data', line=dict(color='green')))

        fig.add_trace(go.Scatter(x=m.fcst_df.time, y=m.fcst_df.fcst, name='forecast', line=dict(color='red')))

        fig.add_trace(go.Scatter(
            x=list(m.fcst_df.time)+list(m.fcst_df.time)[::-1],
            y=list(m.fcst_df.fcst_upper)+list(m.fcst_df.fcst_lower)[::-1],
            fill='toself',
            fillcolor='rgba(255,0,0,0.2)',
            line_color='rgba(255,255,255,0)',
            name='Confidence Interval',
            showlegend=True,
        ))

        fig.add_vline(x=(m.fcst_df['time'].values)[0], line_width=2, line_dash="dash", line_color="black")

        fig.update_layout(
            title       = '<b>Forecast</b>',
            title_x     = 0.5,
            xaxis_title = f"<b>{parameters_dict['time_col']}</b>",
            yaxis_title = f"<b>{parameters_dict['value_col']}</b>",
            height      = 780,
            width       = 1480,
            
        )

        # fig.show()

        # fig.write_html(f"{os.getcwd()}\\templates\\" + "forecast.html")

        plot_html = fig.to_html(f"{os.getcwd()}\\templates\\" + "forecast.html")
        plot_html = plot_html.replace("</head>", "<style> input[type=button], input[type=submit], input[type=reset] {background-color: #4CAF50;border: none;color: white;padding: 16px 32px;text-decoration: none;margin: 4px 2px;cursor: pointer;}</style></head>")
        plot_html = plot_html.replace("<body>", "<body><form action='http://localhost:5000/forecast_plot'><center><input type='submit' value='Refresh'></center></form>")

        with open(f"{os.getcwd()}\\templates\\" + "forecast.html", "w") as file:
            file.write(plot_html)

        # requests.get('http://localhost:5000/').content 