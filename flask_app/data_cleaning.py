import os
import pandas as pd
import pickle
import plotly.graph_objects as go

# from kats.models.prophet import ProphetModel, ProphetParams
# from kats.models.sarima import SARIMAModel, SARIMAParams
# from kats.consts import TimeSeriesData

# with open(f"{os.getcwd()}\\user_inputs\\" + "in_parms.pickle", 'rb') as handle:
#     parameters_dict = pickle.load(handle)

# input_df = pd.read_csv(f"{os.getcwd()}\\user_inputs\\" + "input_file.csv", parse_dates=[parameters_dict["time_col"]])
# input_df = input_df[[parameters_dict["time_col"], parameters_dict["value_col"]]]

# # create TimeSeriesData
# tsdata = TimeSeriesData(time=input_df[parameters_dict["time_col"]], value=input_df[parameters_dict["value_col"]])

# print(tsdata)

# # # create a model param instance
# # params = ProphetParams(seasonality_mode='multiplicative') # additive mode gives worse results

# # # create a prophet model instance
# # m = ProphetModel(tsdata, params)

# # # fit model simply by calling m.fit()
# # m.fit()

# # # make prediction for next 30 month
# # fcst = m.predict(steps=parameters_dict["pred_length"], freq="D")

# # plot to visualize
# # m.plot()

# # create SARIMA param class
# params = SARIMAParams(
#     p = 2, 
#     d=1, 
#     q=1, 
#     trend = 'ct', 
#     seasonal_order=(1,0,1,12)
#     )

# # initiate SARIMA model
# m = SARIMAModel(data=tsdata, params=params)

# # fit SARIMA model
# m.fit()

# # generate forecast values
# fcst = m.predict(
#     steps=30, 
#     freq="D"
#     )

# make plot to visualize
# m.plot()

fig = go.Figure()

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

# # fig.add_vline(x=m.fcst_df.time[0], line_width=2, line_dash="dash", line_color="black")

fig.update_layout(
    title       = '<b>forecast</b>',
    title_x     = 0.5,
    xaxis_title = '<b>time</b>',
    yaxis_title = '<b>value</b>',
    height      = 780,
    width       = 1480,
    
)

# fig.show()

# fig.write_html(f"{os.getcwd()}\\templates\\" + "forecast.html")


plot_html = fig.to_html(f"{os.getcwd()}\\templates\\" + "forecast.html")
plot_html = plot_html.replace("<body>", "<body><form action='http://localhost:5000/plot'><center><input type='submit' value='Refresh'></center></form>")

print("<body>" in plot_html)


with open(f"{os.getcwd()}\\templates\\" + "forecast.html", "w") as file:
    file.write(plot_html)







