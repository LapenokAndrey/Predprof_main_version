from flask import Flask, render_template, request
from backendAndData.online_functions import *
from strategy.strategy import *
from backendAndData.data_functions import *


app = Flask(__name__, template_folder='../templates')


@app.route("/company/<string:name>")
def company(name):
    if not is_company_available_online(company=name):
        return None

    start_time = datetime.datetime(2010, 1, 1)
    end_time = datetime.datetime.now()

    ticker = get_ticker_by_name(name)
    df = get_stocks(ticker=ticker, start=start_time, end=end_time, interval='1 day')
    candle_stocks = convert_df_to_list_for_graph(df)
    point_stocks = convert_df_to_list_for_graph_line(df)
    current_price = point_stocks[-1][1]

    history = convert_df_to_close_prices_list(df)

    strategy_1 = get_strategy(history).predict_percent1()
    strategy_2 = mr_strategy(history, min(30, len(history)), min(90, len(history)), 5)

    kwargs = {'ticker': ticker, 'name': get_name_by_ticker_online(ticker=ticker),
              'logo': get_company_logo_online(ticker=ticker), 'candle_stocks': candle_stocks,
              'point_stocks': point_stocks, 'strategy_1': strategy_1, 'strategy_2': strategy_2,
              'current_price': current_price, 'description': get_description_db(company=name)}
    return render_template("company.html", **kwargs)


@app.route("/companies")
@app.route("/companies_list")
def companies_list():
    companies = get_names_available_companies(n=20)
    kwargs = {'companies': [(name, get_logo_from_db(company=name)) for name in companies]}
    return render_template("companies_list.html", **kwargs)


@app.route("/companies", methods=['POST'])
@app.route("/companies_list", methods=['POST'])
def companies_list_input():
    company_name = request.form['company']
    ticker = get_ticker_by_name(company_name)
    companies = get_names_available_companies()

    kwargs = {'input_company': {'ticker': ticker, 'name': get_name_by_ticker(ticker=ticker),
                                'logo': get_company_logo_online(ticker=ticker)},
              'companies': [(name, get_company_logo_online(company=name)) for name in companies]}
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
