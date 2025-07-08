from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    shots = int(request.form.get('shots', 0))
    goals = int(request.form.get('goals', 0))

    if shots > 0:
        shoot_rate = (goals / shots) * 100
    else:
        shoot_rate = 0

    return jsonify({'result': f'{shoot_rate:.2f}'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
