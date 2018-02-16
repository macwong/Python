#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def index():
    return "Hello, World!"

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/testapi/tasks', methods=['GET'])
def get_tasks():
    return jsonify({ 'tasks': tasks })

@app.route('/testapi/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/testapi/tasks', methods=['POST'])
def create_task():
    json = request.get_json()
    print(json)
#    print('title' in request.json)
    if not json or not 'title' in json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': json['title'],
        'description': json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/testapi/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    json = request.get_json()
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
#    if 'title' in json and type(json['title']) != unicode:
#        abort(400)
#    if 'description' in json and type(json['description']) is not unicode:
#        abort(400)
    if 'done' in json and type(json['done']) is not bool:
        abort(400)
    task[0]['title'] = json.get('title', task[0]['title'])
    task[0]['description'] = json.get('description', task[0]['description'])
    task[0]['done'] = json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/testapi/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)