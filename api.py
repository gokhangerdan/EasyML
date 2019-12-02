from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

from core.Node import Node


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)


class NodeExecuter(Resource):
    def post(self):
        request_body = request.get_json()

        node = Node(
            function=request_body["function"],
            settings=request_body["settings"],
            input_ports=request_body["input_ports"]
        )

        return node.output_ports


api.add_resource(NodeExecuter, '/node_executer')

if __name__ == '__main__':
    app.run(debug=True)
