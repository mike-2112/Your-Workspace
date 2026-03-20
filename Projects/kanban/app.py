from flask import Flask, render_template_string, request, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)
BOARD_FILE = '/root/.openclaw/workspace/memory/kanban.json'

def load_board():
    path = BOARD_FILE
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {'columns': {'Todo': [], 'In Progress': [], 'Done': []}}

def save_board(board):
    os.makedirs(os.path.dirname(BOARD_FILE), exist_ok=True)
    with open(BOARD_FILE, 'w') as f:
        json.dump(board, f)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Dingle Kanban</title>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 p-8">
    <h1 class="text-4xl font-bold mb-8 text-center text-purple-400">Pyramid Kanban 🚀</h1>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        {% for col, tasks in board.columns.items() %}
        <div class="bg-gray-800 p-6 rounded-xl shadow-xl">
            <h2 class="text-2xl font-bold mb-6 text-center">{{ col }}</h2>
            <div id="{{ col }}" class="space-y-3 min-h-[200px]">
                {% for task in tasks %}
                <div class="task bg-blue-600 p-4 rounded-lg cursor-move hover:bg-blue-500 transition flex justify-between items-center" hx-post="/move/{{ task.id }}" hx-include="select[name='col']">
                    <span>{{ task.text }}</span>
                    <select name="col" class="ml-2 bg-transparent border text-white">
                        {% for c in board.columns %}
                        <option value="{{ c }}" {% if c == col %}selected{% endif %}>{{ c }}</option>
                        {% endfor %}
                    </select>
                </div>
                {% endfor %}
            </div>
            <input placeholder="New {{ col }} task" class="new-task mt-6 w-full p-3 bg-gray-700 rounded-lg border" hx-post="/add/{{ col }}" hx-trigger="keyup[key=='Enter'] from:.new-task" hx-target="#{{ col }}">
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    board = load_board()
    return render_template_string(HTML, board=board)

@app.route('/add/<col>')
def add(col):
    board = load_board()
    text = request.args.get('text', 'New Task')
    id = max([max([t['id'] for t in tasks]) for tasks in board['columns'].values()] + [0]) + 1
    task = {'id': id, 'text': text}
    board['columns'][col].append(task)
    save_board(board)
    return '<div class="task bg-green-600 p-4 rounded-lg cursor-move hover:bg-green-500 transition flex justify-between items-center" hx-post="/move/' + str(id) + '" hx-include="select[name=\'col\']"><span>' + text + '</span><select name="col" class="ml-2 bg-transparent border text-white"><option value="' + col + '" selected>' + col + '</option><option>Todo</option><option>In Progress</option><option>Done</option></select></div>'

@app.route('/move/<int:task_id>')
def move(task_id):
    board = load_board()
    new_col = request.form.get('col')
    for col in board['columns']:
        for i, task in enumerate(board['columns'][col]):
            if task['id'] == task_id:
                board['columns'][new_col].append(board['columns'][col].pop(i))
                save_board(board)
                break
    return jsonify(board['columns'][new_col][-1])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
