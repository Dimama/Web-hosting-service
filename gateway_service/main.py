from flask import Flask, jsonify, Response

app = Flask(__name__)


@app.route('/server', methods=['GET'])
def get_all_server_configurations():
    pass


@app.route('/server/<int:server_id>', methods=['GET'])
def get_info_about_server(server_id):
    pass


@app.route('/user/<int:user_id>/rent', methods=['GET'])
def get_rents_for_user(user_id):
    pass


@app.route('/user/<int:user_id>/rent', methods=['POST'])
def rent_server_for_user(user_id):
    pass


@app.route('/user/<int:user_id>/rent/<int:rent_id>', methods=['DELETE'])
def delete_server_from_user_rents(user_id, rent_id):
    return Response(status=204)


@app.route('/', methods=['GET'])
def get_index():
    pass


if __name__ == '__main__':
    app.run(host='localhost', port=8080)