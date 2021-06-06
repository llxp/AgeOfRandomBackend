import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from aor_parser import \
    AORTechParser, AORCardParser, \
    AORStringsParser, HomecityParser

app = Flask(__name__, static_url_path='')
cors = CORS(app)

current_path = os.getcwd()

tech_parser = AORTechParser(
    current_path + '\\data\\Data\\techtreey.xml')
strings_parser = AORStringsParser(
    current_path + '\\data\\Data\\strings')
homecity_parser = HomecityParser(current_path + '\\data\\Data', current_path + '\\data\\Data\\civs.xml')
parser = AORCardParser(
    current_path + '\\data\\Data',
    tech_parser,
    strings_parser,
    homecity_parser
)


@app.route(
    '/api/get_cards',
    methods=['GET'])
def index():
    return parser.cards


@app.route('/img/<path:path>')
def send_js(path):
    return send_from_directory('data/pictures/Data/wpfg', path)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5005)
