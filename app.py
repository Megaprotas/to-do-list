import os
from flask import Flask, render_template, redirect, request, url_for
from config import Config
from forms import TaskForm, EditForm, DeleteForm
from flask_pymongo import PyMongo, DESCENDING
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["MONGO_DBNAME"] = "megaprotaslist"
app.config["MONGO_URI"] = os.environ.get("MONGODB_URI")
app.config.from_object(Config)
mongo = PyMongo(app)


@app.route('/')
@app.route('/all_tasks')
def all_tasks():
    tasks = mongo.db.tasks.find().sort([('due_day', DESCENDING)])
    return render_template('all_tasks.html', title='Tasker', tasks=tasks)


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    form = TaskForm(request.form)
    if form.validate_on_submit():
        task = mongo.db.tasks
        task.insert_one({
            'name': request.form['name'],
            'description': request.form['description'],
            'due_day': request.form['due_day'],
            'important': request.form.get('important'),
        })
        return redirect(url_for('all_tasks', title='You\'re back to main list'))
    return render_template('add_task.html', title='Add task', form=form)


@app.route('/edit_task/<task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = mongo.db.tasks.find_one_or_404({'_id': ObjectId(task_id)})
    form = EditForm(request.form)

    if request.method == 'GET':
        form = EditForm(data=task)
        return render_template('edit_task.html', title='Edit task', task=task, form=form)

    if form.validate_on_submit():
        task = mongo.db.tasks
        task.update_one({
            '_id': ObjectId(task_id),
        }, {
            '$set': {
                'name': request.form['name'],
                'description': request.form['description'],
                'due_day': request.form['due_day'],
                'important': request.form.get('important'),
            }
        })
        return redirect(url_for('all_tasks', title='New task has been added'))
    return render_template('edit_task.html', title='Edit task', task=task, form=form)


@app.route('/delete_task/<task_id>', methods=['GET', 'POST'])
def delete_task(task_id):
    task = mongo.db.tasks.find_one_or_404({'_id': ObjectId(task_id)})
    form = DeleteForm(request.form)

    if request.method == 'GET':
        form = DeleteForm(data=task)
        return render_template('delete_task.html', title='Delete task', task=task, form=form)

    if form.validate_on_submit():
        task = mongo.db.tasks
        task.delete_one({
            '_id': ObjectId(task_id),
        })
        return redirect(url_for('all_tasks', title='Task has been deleted'))
    return render_template('delete_task.html', title='Delete task', task=task, form=form)


@app.route('/task_done/<task_id>', methods=["POST"])
def task_done(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('all_tasks'))


@app.route('/all_tasks_progress/<task_id>', methods=["GET", "POST"])
def all_tasks_progress(task_id):
    task = mongo.db.tasks
    task.find_one_and_update(
        {'_id': ObjectId(task_id)},
        {
            '$inc': {"progress": 10}
        })
    return redirect(url_for('all_tasks'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
