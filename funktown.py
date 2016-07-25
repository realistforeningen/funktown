from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask.ext.assets import Environment, Bundle
from flask_bootstrap import Bootstrap
import arrow

from models import Person, Role, Assignment, db_session, select, commit

app = Flask(__name__)
app.debug = True

## Flask-Bootstrap
Bootstrap(app)

## Flask-Assets
assets = Environment(app)
js = Bundle('js/selectize.min.js', 'js/main.js',
        output='assets/all.js')
css = Bundle('css/selectize.bootstrap3.css', 'css/style.css',
        output='assets/all.css')
assets.register('js', js)
assets.register('css', css)

def all_roles():
    return select(r for r in Role).order_by(Role.name)

app.add_template_global(all_roles, name='all_roles')
app.add_template_global(arrow.now, name='now')

@app.route('/')
@db_session
def index():
    return render_template('index.html')

@app.route('/roles.json', methods=['POST'])
@db_session
def roles_create():
    name = request.form['name']
    role = Role(name=name)
    commit()
    return jsonify(result=role.to_dict())

@app.route('/people.json')
@db_session
def person_query():
    query = request.args['query']
    people = select(p for p in Person if query in p.name)
    people = [p.to_dict() for p in people]
    return jsonify(results=people)

@app.route('/people', methods=['POST'])
@db_session
def person_create():
    person = Person(name=request.form['name'])
    commit()
    return redirect(url_for('person_show', id=person.id))

@app.route('/people/<id>')
@db_session
def person_show(id):
    person = Person[id]
    assignments = person \
        .assignments \
        .order_by(Assignment.year.desc(), Assignment.semester.desc())
    return render_template('person.html', person=person, assignments=assignments)

@app.route('/people/<id>', methods=['POST'])
@db_session
def person_update(id):
    person = Person[id]
    person.name = request.form['name']
    person.email = request.form['email']
    commit()
    return redirect(request.path)

@app.route('/people/<id>/assign', methods=['POST'])
@db_session
def person_assign(id):
    person = Person[id]
    role = Role[request.form['role']]
    assignment = Assignment(
        person=person,
        role=role,
        year=int(request.form['year']),
        semester=int(request.form['semester'])
    )
    commit()
    return redirect(url_for('person_show', id=person.id))

@app.route('/roles/<id>')
@db_session
def roles_show(id):
    pass

@app.route('/assignments/<id>/delete', methods=['POST'])
@db_session
def assignments_delete(id):
    assignment = Assignment[id]
    person_id = assignment.person.id
    assignment.delete()
    return redirect(url_for('person_show', id=person_id))

if __name__ == '__main__':
    app.run()

