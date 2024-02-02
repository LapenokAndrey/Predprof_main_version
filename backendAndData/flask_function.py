from flask import Flask, render_template, request
from backendAndData.functions import *
from strategy.strategy import *


app = Flask(__name__, template_folder='../templates')


@app.route("/company/<string:name>")
def company(name):
    if not is_company_available(company=name):
        return None

    start_time = datetime.datetime(2010, 1, 1)
    end_time = datetime.datetime.now()

    ticker = get_ticker_by_name(name)
    candle_stocks = get_stocks_list_for_graph(ticker=ticker, start=start_time, end=end_time, interval='1 day')
    point_stocks = get_stocks_list_for_graph_line(ticker=ticker, start=start_time, end=end_time, interval='1 day')
    future_price = get_strategy(get_close_prices_list(
        ticker=ticker, start=start_time, end=end_time, interval='1 day')).predict()
    current_price = point_stocks[-1][1]
    difference = future_price - current_price

    kwargs = {'ticker': ticker, 'name': get_name_by_ticker(ticker=ticker),
              'logo': get_company_logo(ticker=ticker), 'candle_stocks': candle_stocks,
              'point_stocks': point_stocks, 'future_price': future_price, 'current_price': current_price,
              'difference': difference, 'description': get_description(company=name)}
    return render_template("company.html", **kwargs)


@app.route("/companies")
@app.route("/companies_list")
def companies_list():
    companies = get_names_yahoo_available_companies()
    kwargs = {'companies': [(name, get_logo_from_db(company=name)) for name in companies]}
    return render_template("companies_list.html", **kwargs)


@app.route("/companies", methods=['POST'])
@app.route("/companies_list", methods=['POST'])
def companies_list_input():
    company_name = request.form['company']
    ticker = get_ticker_by_name(company_name)
    companies = get_names_yahoo_available_companies()

    kwargs = {'input_company': {'ticker': ticker, 'name': get_name_by_ticker_yahoo(ticker=ticker),
                                'logo': get_company_logo(ticker=ticker)},
              'companies': [(name, get_company_logo(company=name)) for name in companies]}
    return render_template("companies_list.html", **kwargs)


@app.route("/")
@app.route("/index")
@app.route("/home")
@app.route("/PearInvesting")
def home():
    return render_template("home.html")


@app.route("/rates")
def rates():
    return render_template("rates.html")


@app.route('/login', methods=['POST'])
def enter_post():
    password = request.form['password']
    email = request.form['email']

    if is_user(email=email, password=password):
        ...

    else:
        ...


@app.route('/login')
def enter():
    return render_template('login.html')


@app.route('/registration', methods=['POST'])
def registrate_post():
    password = request.form['password']
    email = request.form['email']

    if is_user(email=email, password=password):
        ...

    else:
        add_user_to_db(email=email, password=password)
        ...
