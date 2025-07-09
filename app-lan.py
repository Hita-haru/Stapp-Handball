import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

DATA_FILE = 'data.json'

def load_data():
    """データをファイルから読み込む"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    """データをファイルに保存する"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_data', methods=['POST'])
def submit_data():
    data = request.json

    # 各シュートとゴールの値を取得（整数に変換）
    shot_keys = ['shotlb', 'shotlt', 'shotc', 'shotrb', 'shotrt']
    goal_keys = ['goallb', 'goallt', 'goalc', 'goalrb', 'goalrt']

    try:
        shots_values = [int(data.get(k, 0)) for k in shot_keys]
        goals_values = [int(data.get(k, 0)) for k in goal_keys]
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input. Please provide numbers.'}), 400


    total_shots = sum(shots_values)
    total_goals = sum(goals_values)

    if total_shots > 0:
        shoot_rate = (total_goals / total_shots) * 100
    else:
        shoot_rate = 0

    # 保存するデータを作成
    record = {
        'timestamp': datetime.now().isoformat(),
        'team': data.get('team'),
        'player': data.get('player'),
        'position': data.get('position'),
        'details': {
            'left_bottom': {'shots': shots_values[0], 'goals': goals_values[0]},
            'left_top': {'shots': shots_values[1], 'goals': goals_values[1]},
            'center': {'shots': shots_values[2], 'goals': goals_values[2]},
            'right_bottom': {'shots': shots_values[3], 'goals': goals_values[3]},
            'right_top': {'shots': shots_values[4], 'goals': goals_values[4]},
        },
        'summary': {
            'total_shots': total_shots,
            'total_goals': total_goals,
            'shoot_rate': round(shoot_rate, 2)
        }
    }

    # 既存のデータを読み込み、新しいレコードを追加して保存
    all_data = load_data()
    all_data.append(record)
    save_data(all_data)

    return jsonify({
        'result': f'{shoot_rate:.2f}',
        'total_shots': total_shots,
        'total_goals': total_goals
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
