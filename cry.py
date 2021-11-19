import pandas as pd,datetime,numpy as np,plotly.graph_objs as go,re,plotly.io as pio,pandas_datareader as web
from autots import AutoTS
pio.renderers.default = "browser";ab = input('ablitar grafico? ')
s = datetime.datetime(2016,1,1);e = datetime.datetime.now();
SE = (str(e.year)+'-'+str(e.month)+'-'+str(e.day))
data = web.DataReader('BTC-USD','yahoo',s,e);
data.reset_index(inplace=True)
model = AutoTS(forecast_length=30, frequency='infer', ensemble='simple', drop_data_older_than_periods=60)
model = model.fit(data, date_col='Date', value_col='Close', id_col=None)
prediction = model.predict()
forecast = prediction.forecast
tempo = data['Date'];preço = data['Close']
tempoP = forecast['Close'].index;preçoP = forecast['Close']
print (tempoP,preçoP)
if ab == 's':
    fig = go.Figure(go.Scatter(x=tempo,y=preço,name='btcF'))
    fig.add_trace(go.Scatter(x=tempoP,y=preçoP,name='btc-pred'))
    fig.update_layout(title="previsão de crypto")
    fig.show()
