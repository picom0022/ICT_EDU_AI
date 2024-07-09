from flask import Flask, request, jsonify

app = Flask(__name__)

items = [
    {"id" : 1, "name":"Apple", "price" : 5000},
    {"id" : 2, "name":"Banana", "price" : 4000},
    {"id" : 3, "name":"Mango", "price" : 6000},
]

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/items', methods=['POST'])
def add_items():
    # 요청 정보가 json방식으로
    item = request.get_json()
    items.append(item)
    return jsonify(items)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

