import pandas as pd
import numpy as np
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models.widgets import Panel, Tabs
from sklearn.preprocessing import StandardScaler
from django.conf import settings

pd.options.mode.chained_assignment = None # disabled settingwithcopy warning

def get_stock(symbol = 'spy'):
    """
		This function gets stock information of required symbol. Default is SP500.
		Info is obtained from Kaggle
		- Symbol -> Stock Symbol (e.g SPX)
    """
    filename = "{0}.us.txt".format(symbol.lower())
    try:
        stock = pd.read_csv("{0}/{1}".format(settings.FILE_DIR, filename), sep = ',') # try to find file...
    except:
        stock = pd.read_csv("{0}/spy.us.txt".format(settings.FILE_DIR), sep = ',') # if file does not exist, use this exception
        symbol = 'spy'
    stock = stock.drop('OpenInt', axis = 1)
    
    stock_info = pd.read_json('https://api.iextrading.com/1.0/ref-data/symbols') #retrieves names of companies based on symbols. Used for displaying company name on site.
    company_name = stock_info[stock_info['symbol'] == symbol.upper()]['name']
    
    if len(company_name) == 0:
        
        company_name = "NA"
        
    else:
        
        company_name = company_name.iloc[0]
    
    return stock, company_name

def get_more_attributes(stock_data):
    
    closing_data = stock_data['Close'].to_numpy()
    last_10_days = closing_data[-10:-1] 
    volatility = round(np.std(last_10_days), 4) #compute volatility for last 10 days
    
    one_day_percent_change = (np.log(closing_data[-1])-np.log(closing_data[-2]))*100 #compute percentage change from yesterday close
    
    return volatility, round(one_day_percent_change, 4)

def create_bokeh_plot(stock_data, symbol, predictions = None):
    
    #this generates plot tabs for all available data. A plot will be generated for each of the labels below.
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
    plots = ['Close', 'Open', 'High', 'Low', 'Volume']
    graph_tabs = []
    
    for plot_type in plots:
        # for each plot type, generate and save a plot to a the tabs list.
        graph = figure(plot_width=800, plot_height=250, x_axis_type = 'datetime', 
                       title='{0} Data of {1}'.format(plot_type, symbol))
        
        hover = plot_type.lower()
        
        data = stock_data[[plot_type, 'Date']]
        data.columns = ['y', 'date']
        data_cds = ColumnDataSource(data)
        
        if plot_type == 'Volume':
            hover = HoverTool(tooltips=[('Date', '@date{%Y-%m-%d}'), ('Value', '@y{0.2f}'),],
                      formatters={'date': 'datetime', '{0}'.format(plot_type.lower()): 'printf'})
        else:
            hover = HoverTool(tooltips=[('Date', '@date{%Y-%m-%d}'), ('Value', '$@y{0.2f}'),],
                      formatters={'date': 'datetime', '{0}'.format(plot_type.lower()): 'printf'})
        
        graph.line('date', 'y', color = 'green', alpha = 0.5, source = data_cds, legend_label = symbol.upper())
        
        if predictions is not None:
            
            prediction = predictions[['Date', plot_type]]
            prediction.columns = ['date', 'y']
            prediction['date'] = pd.to_datetime(prediction['date']) #used for managing predictions from NN
            prediction_cds = ColumnDataSource(prediction)
            graph.line("date", 'y', color='red', alpha = 0.5, source = prediction_cds,
                       legend_label = "{0} Predictions".format(symbol.upper()))
        
        graph.legend.location = 'top_left'
        graph.legend.click_policy = 'hide' # plot settings
        graph.add_tools(hover) 
        graph.title.align = 'center'
        
        tab = Panel(child = graph, title = '{0} Data'.format(plot_type))
        
        graph_tabs.append(tab)
    
    tabs = Tabs(tabs = graph_tabs) # create a bokeh tab using generated plots above
    
    script, div = components(tabs) # generate script and div components of graph for use in template files
    
    return script, div
            

def generate_predictions(stock_data):
    
    #used to generate predictions for each of the features below. Predictions are made from generic NN's trained in the build_model file.
    features = ['Close', 'Open', 'High', 'Low', 'Volume']
    
    predictions = stock_data['Date']
    
    for feature in features:
        
        X = stock_data.drop(feature, axis = 1)
        
        X['Date'] = np.arange(0, len(X))
        
        X = X.to_numpy()
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        
        prediction = settings.MODELS[feature].predict(X)
        
        prediction = pd.DataFrame(prediction, columns = [feature])
        
        predictions = pd.concat((predictions, prediction), axis = 1)

    return predictions
    
    