from flask import Flask, render_template, request
from backendAndData.online_functions import *
from strategy.strategy import *
from backendAndData.data_functions import *
from backendAndData.company_class import Company


app = Flask(__name__, template_folder='../templates')


def get_kwargs_company(name, start_time, end_time):
    interval = '1 month'

    ticker = get_ticker_by_name(name)

    comp = Company(ticker)
    if not comp.is_available:
        return 'Sorry'

    start_time = max(start_time, datetime.datetime.strptime(comp.get_info()['first_available_date'], '%Y-%m-%d %H:%M:%S'))
    candle_stocks = comp.get_stocks_any_format(start_time, end_time, interval, 'list_for_graph')
    point_stocks = comp.get_stocks_any_format(start_time, end_time, interval, 'list_for_graph_line')
    current_price = point_stocks[-1][1]

    history = comp.get_stocks_any_format(start_time, end_time, interval, 'close_prices_list')

    strategy_1 = get_strategy(history).predict_percent1()
    strategy_2 = mr_strategy(history, min(30, len(history)), min(90, len(history)), 5)

    kwargs = {'ticker': ticker, 'name': comp.get_name(),
              'logo': get_logo_from_db(ticker=ticker), 'candle_stocks': candle_stocks,
              'point_stocks': point_stocks, 'strategy_1': strategy_1, 'strategy_2': strategy_2,
              'current_price': current_price, 'description': get_description_db(ticker=ticker),
              'access_level': comp.get_info()['necessary_access_level']}
    return kwargs


@app.route("/company/<string:user>/<string:name>")
def company_user(user, name):
    start_time = datetime.datetime(2010, 1, 1)
    end_time = datetime.datetime.now()

    kwargs = get_kwargs_company(name, start_time, end_time)

    if is_email(user):
        kwargs['user'] = user
        kwargs['user_access_level'] = get_user(email=user)[3]

    else:
        kwargs['user'] = 'default'
        kwargs['user_access_level'] = 0

    return render_template("company.html", **kwargs)


@app.route("/company/<string:user>/<string:name>", methods=['POST'])
def company_post(user, name):
    start = datetime.datetime.strptime(request.form['startGraph'], '%Y-%m-%d')
    end = datetime.datetime.strptime(request.form['endGraph'], '%Y-%m-%d')

    kwargs = get_kwargs_company(name, start, end)

    if is_email(user):
        kwargs['user'] = user
        kwargs['user_access_level'] = get_user(email=user)[3]

    else:
        kwargs['user'] = 'default'
        kwargs['user_access_level'] = 0

    return render_template("company.html", **kwargs)


@app.route("/companies/<string:user>")
@app.route("/companies_list/<string:user>")
def companies_list_user(user):
    companies = get_names_available_companies(n=50)
    if is_email(user):
        kwargs = {'companies': [(name, get_logo_from_db(company=name)) for name in companies]}
        kwargs['user'] = user
        return render_template("companies_list.html", **kwargs)
    else:
        kwargs = {'companies': [(name, get_logo_from_db(company=name)) for name in companies]}
        kwargs['user'] = 'default'
        return render_template("companies_list.html", **kwargs)


@app.route("/")
@app.route("/index")
@app.route("/home")
@app.route("/PearInvesting")
def home():
    return render_template("home.html", **{'user': 'default'})


@app.route("/<string:user>")
@app.route("/index/<string:user>")
@app.route("/home/<string:user>")
@app.route("/PearInvesting/<string:user>")
def home_user(user):
    if is_email(user):
        return render_template("home.html", **{'user': user})

    return render_template("home.html", **{'user': 'default'})


@app.route("/rates")
def rates():
    return render_template("rates.html", **{'user': 'default'})


@app.route("/rates/<string:user>")
def rates_user(user):
    if is_email(user):
        return render_template("rates.html", **{'user': user})

    return render_template("rates.html", **{'user': 'default'})


@app.route('/login', methods=['POST'])
def enter_post():
    password = request.form['password']
    email = request.form['email']

    if is_user(email=email, password=password):
        return render_template('home.html', **{'user': email})

    else:
        return render_template('home.html', **{'user': 'default'})


@app.route('/login')
def enter():
    return render_template('login.html', **{'user': 'default'}
)


@app.route('/registration')
def registration():
    return render_template('reg.html', **{'user': 'default'}
)


@app.route('/registration', methods=['POST'])
def registrate_post():
    password = request.form['password']
    email = request.form['email']

    kwargs = {'user': email}

    if is_user(email=email, password=password):
        ...

    else:
        add_user_to_db(email=email, password=password)
        ...

    return render_template('home.html', **kwargs)
