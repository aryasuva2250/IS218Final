import simplejson as json
from flask import Flask, request, Response, redirect, make_response
from flask import render_template
from pymysql.cursors import DictCursor
from flaskext.mysql import MySQL
from flask_assets import Environment

from app.application.home.forms import ContactForm

app = Flask(__name__, template_folder="templates")
app.config.from_pyfile('config.py')
mysql = MySQL(cursorclass=DictCursor)

assets = Environment(app)

mysql.init_app(app)
'''
app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'biostats2'
mysql.init_app(app)
'''

@app.route('/', methods=['GET'])
def index():
    user = {'username': "Miguel's Project"}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biostats1')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, persons=result)


@app.route('/view/<int:person_id>', methods=['GET'])
def record_view(person_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biostats1 WHERE id=%s', person_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', person=result[0])


@app.route('/edit/<int:person_id>', methods=['GET'])
def form_edit_get(person_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biostats1 WHERE id=%s', person_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', person=result[0])


@app.route('/edit/<int:person_id>', methods=['POST'])
def form_update_post(person_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Name'), request.form.get('Sex'), request.form.get('Age'),
                 request.form.get('Height_in'), request.form.get('Weight_lbs'),person_id)
    sql_update_query = """UPDATE biostats1 t SET t.Name = %s, t.Sex = %s, t.Age = %s, t.Height_in = 
    %s, t.Weight_lbs = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/persons/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Person Form')


@app.route('/persons/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Name'), request.form.get('Sex'), request.form.get('Age'),
                 request.form.get('Height_in'), request.form.get('Weight_lbs'))
    sql_insert_query = """INSERT INTO biostats1 (Name,Sex,Age,Height_in,Weight_lbs ) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:person_id>', methods=['POST'])
def form_delete_post(person_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM biostats1 WHERE id = %s """
    cursor.execute(sql_delete_query, person_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/persons', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biostats1')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/persons/<int:person_id>', methods=['GET'])
def api_retrieve(person_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biostats1 WHERE id=%s', person_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/persons/<int:person_id>', methods=['PUT'])
def api_edit(person_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Name'], content['Sex'], content['Age'],
                 content['Height_in'], content['Weight_lbs'],
                    person_id)
    sql_update_query = """UPDATE biostats1 t SET t.Name = %s, t.Sex = %s, t.Age = %s, t.Height_in = 
           %s, t.Weight_lbs = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/persons/', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['Name'], content['Sex'], content['Age'],
                 content['Height_in'], content['Weight_lbs'])
    sql_insert_query = """INSERT INTO biostats1 (Name,Sex,Age,Height_in,Weight_lbs) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/v1/persons/<int:person_id>', methods=['DELETE'])
def api_delete(person_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM biostats1 WHERE id = %s """
    cursor.execute(sql_delete_query, person_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp
@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        return redirect("/", code=302)
    return render_template("contact.html", form=form)

@app.errorhandler(404)
def not_found():
    """Page not found."""
    return make_response(
        'SORRY. THIS PAGE IS NOT FOUND.',
        404
     )

@app.errorhandler(400)
def bad_request():
    """Bad request."""
    return make_response(
        'BAD REQUEST! THIS SERVER DOES NOT SUPPORT YOUR REQUEST.',
        400
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
