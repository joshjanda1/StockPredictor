from django.template import loader
from django.http import HttpResponse, Http404
from django.conf import settings
from . import services
import random
import os
# Create your views here.

def detail_view(request):
    """
    Gives details on stock symbol.
        Parameters:
        - Request -> Request
        - Symbol -> Trading Symbol, such as SPX for SP500
    """
    symbol = 'spy'
    symbol = request.GET.get('usr_search')
    template = loader.get_template('stocks/detail.html')
	
    stock_data, company_name = services.get_stock(symbol)#gets stock info
    prediction_data = services.generate_predictions(stock_data)#generates predictions of stock data
	
    volatility_data, one_day_percent_change = services.get_more_attributes(stock_data)#compute volatility and percent change from previous close
    script, div = services.create_bokeh_plot(stock_data, symbol, predictions = prediction_data)
	
    if stock_data is None:
        raise Http404("Stock {0} does not exist, try again.".format(symbol))
	
    stock_info = {
        'symbol': symbol.upper(),
        'today_close': stock_data['Close'].iloc[-1],#gets todays closing price
        'today_open': stock_data['Open'].iloc[-1],#gets todays open price
        'today_high': stock_data['High'].iloc[-1],#gets todays high
        'today_low': stock_data['Low'].iloc[-1],#gets todays low
		'today_volume': stock_data['Volume'].iloc[-1],
		'current_volatility': volatility_data,
		'one_day_percent_change': one_day_percent_change,
		'company': company_name,
		'script': script,
		'div': div,
	}
    
    return HttpResponse(template.render(stock_info, request))

def random_view(request):
    """
    Gives details on a randomized stock symbol.
        Parameters:
        - Request -> Request
        - Symbol -> Trading Symbol, such as SPX for SP500
    """
    
    random_filename = random.choice(os.listdir(settings.FILE_DIR)) # chooses random file name from data directory
    symbol = random_filename.strip('.us.txt') # strips file extension from filename to obtain stock symbol..
    template = loader.get_template('stocks/detail.html')
    stock_data, company_name = services.get_stock(symbol)#gets stock info
    prediction_data = services.generate_predictions(stock_data)#generates predictions of stock data
	
    volatility_data, one_day_percent_change = services.get_more_attributes(stock_data)#compute volatility and percent change from previous close
    script, div = services.create_bokeh_plot(stock_data, symbol, predictions = prediction_data)
	
    if stock_data is None:
        raise Http404("Stock {0} does not exist, try again.".format(symbol))
	
    stock_info = {
        'symbol': symbol.upper(),
        'today_close': stock_data['Close'].iloc[-1],#gets todays closing price
        'today_open': stock_data['Open'].iloc[-1],#gets todays open price
        'today_high': stock_data['High'].iloc[-1],#gets todays high
        'today_low': stock_data['Low'].iloc[-1],#gets todays low
		'today_volume': stock_data['Volume'].iloc[-1],
		'current_volatility': volatility_data,
		'one_day_percent_change': one_day_percent_change,
		'company': company_name,
		'script': script,
		'div': div,
	}
    
    return HttpResponse(template.render(stock_info, request))

def index(request):
	#displays home page
	template = loader.get_template('stocks/index.html')
	context = {}
	return HttpResponse(template.render(context, request))

def about(request):
	#displays about page
    template = loader.get_template('stocks/about.html')
    context = {}
    return HttpResponse(template.render(context, request))
