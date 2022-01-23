import tkinter as tk,pandas_datareader as web,datetime,matplotlib.pyplot as plt,numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
try:from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
except ImportError:from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NavigationToolbar2TkAgg
from autots import AutoTS
from pandas import DataFrame
cya = input('crypto a ser analizada:')
root = tk.Tk()
root.wm_title("previsão de graficos")
try:
    s = datetime.datetime(2019,1,1);e = datetime.datetime.now();
    data = web.DataReader(cya.upper()+'-USD','yahoo',s,e);
    data.reset_index(inplace=True)
    finance = data[['Date','Close','Volume','High','Low']];finance.columns = ['data','valor','volume','alta','baixa']
    df = DataFrame(finance,columns=['data','valor','volume'])
except:print('não foi possivel conectar ao servidor')
dias = input('Dias a serem previstos:')
pmin = input('Minimo de Dias para ler:')
pmax = input('Maximo de Dias para ler:')
#B = tk.Button(root, text ="zoom", command = print('opa'))
#B.pack()
figure1 = plt.Figure(figsize=(5,5),dpi=100)
ax1 = figure1.add_subplot(111)
bar1 = FigureCanvasTkAgg(figure1, root)
bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
df1 = df[['data','volume']].groupby('data').sum()
df1.plot(kind='line', legend=True, ax=ax1)
ax1.set_title('volume')

figure2 = plt.Figure(figsize=(5,5),dpi=100)
ax2 = figure2.add_subplot(111)
for tempo in range(int(pmin),int(pmax)):
    t = tempo
    model = AutoTS(forecast_length=int(dias), frequency='infer', ensemble='simple', drop_data_older_than_periods=t)
    model = model.fit(df, date_col='data', value_col='valor', id_col=None)
    prediction = model.predict()
    forecast = prediction.forecast
    fv = forecast['valor']
    ax2.plot(fv,color='blue')
vt = finance['data'];va = finance['alta'];vb = finance['baixa'];
df2 = df[['data','valor']].groupby('data').sum()
df2.plot(kind='line', legend=True, ax=ax2)
ax2.plot(vt,vb,color='red');ax2.plot(vt,va,color='green')
ax2.set_title('alta-baixa-predição')
line2 = FigureCanvasTkAgg(figure2, root)
line2.get_tk_widget().pack(side=tk.RIGHT,fill=tk.BOTH)

toolbar1 = NavigationToolbar2TkAgg(bar1, root)
toolbar2 = NavigationToolbar2TkAgg(line2, root)
toolbar1.update()
toolbar2.update()
root.mainloop()