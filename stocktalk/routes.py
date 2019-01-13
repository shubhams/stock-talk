from flask import request, redirect, url_for, render_template, json
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from stocktalk import app, User
from stocktalk.helpers import get_search_results
from stocktalk.models.forms import RegForm, LoginForm
from stocktalk.models.user import UserSymbols


@app.route('/')
def hello_world():
	return 'Hello World!'


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('dashboard'))
	form = LoginForm()
	error_message = None
	if request.method == 'POST':
		if form.validate():
			check_user = User.objects(username=form.username.data).first()
			if check_password_hash(check_user['password'], form.password.data):
				if form.remember.data:
					login_user(check_user, remember=True)
				else:
					login_user(check_user)
				return redirect(url_for('dashboard'))
			else:
				error_message = 'Invalid credentials'
	return render_template('login.html', form=form, error=error_message)



@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegForm()
	if request.method == 'POST':
		if form.validate():
			existing_user = User.objects(username=form.username.data).first()
			if existing_user is None:
				pass_hash = generate_password_hash(form.password.data, method='sha256')
				new_user = User(form.username.data, pass_hash).save()
				login_user(new_user)
				return redirect(url_for('dashboard'))
	return render_template('register.html', form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))


@app.route('/search', methods=['GET'])
@login_required
def search_symbols():
	sym = request.args.get('sym')
	results = get_search_results(sym)

	symbols_list = list()
	for result in results['bestMatches']:
		symbol = dict()
		symbol['id'] = result['1. symbol']
		text = result['2. name']
		symbol['text'] = text + ' (' + symbol['id'] + ')'
		symbols_list.append(symbol)
	symbol_results = dict()
	symbol_results['results'] = symbols_list

	response = app.response_class(
		response=json.dumps(symbol_results),
		status=200,
		mimetype='application/json'
	)
	return response


@app.route('/save', methods=['POST'])
@login_required
# @csrf.exempt
def save_symbol():
	sym = request.form.get('sym')
	if sym:
		saved_symbols = UserSymbols.objects(username=current_user.username)
		if not saved_symbols:
			UserSymbols(current_user.username, [sym]).save()
		else:
			UserSymbols.objects(username=current_user.username).update_one(add_to_set__symbols=[sym])
		return "Success!"
	return "Failed! Try again!"


@app.route('/dashboard')
@login_required
def dashboard():
	return render_template('dashboard.html')