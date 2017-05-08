from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flasgger import Swagger
import scraper
import os
import connexion


app = Flask(__name__, static_url_path="")
CORS(app)
Swagger(app)

"""
===================
PC system endpoints
===================
"""
# american server pc endpoint
ow_us_pc = "https://playoverwatch.com/en-us/career/pc/us/"

# european server pc endpoint
ow_eu_pc = "https://playoverwatch.com/en-us/career/pc/eu/"

# korean server pc endpoint
ow_kr_pc = "https://playoverwatch.com/en-us/career/pc/kr/"


"""
=====================
Xbox system endpoints
=====================
"""
ow_xbox = "https://playoverwatch.com/en-us/career/xbl/"


"""
====================
Ps4 system endpoints
====================
"""
ow_ps4 = "https://playoverwatch.com/en-us/career/psn/"



@app.route('/')
def index():
	return app.send_static_file('index.html')


"""
============
Xbox methods
============
"""

@app.route('/<string:btag>/<string:mode>/xbl/', methods = ['GET'])
def get_xbox_data(btag, mode):
	"""
        Get a JSON representation of all your hero's stats for Xbox users.
        ---
        tags:
          - Xbox
        parameters:
          - name: btag
            in: path
            description: Xbox gamertag
            required: true
            type: string
            default: none
          - name: mode
            in: path
            description: request competetive or quickplay stats. (Accepted parameters are "quickplay" or "competetive")
            required: true
            type: string
            default: none
        responses:
          200:
            description: Returns all heroes stats.
            schema:
                type: object
                items:
                    $ref: '#/definitions/Xbox'
        """
        
	resp = scraper.get_qp_hero_data(btag, mode, ow_xbox)
  resp.headers.add('Access-Control-Allow-Origin', '*')
	return jsonify(resp)



"""
===========
Ps4 methods
===========
"""
@app.route('/<string:btag>/<string:mode>/psn/', methods = ['GET'])
def get_ps4_data(btag, mode):
    """
    Get a JSON representation of all your hero's stats for Ps4 users.
    ---
    tags:
      - Ps4
    parameters:
      - name: btag
        in: path
        description: Psn ID
        required: true
        type: string
        default: none
      - name: mode
        in: path
        description: request competetive or quickplay stats. (Accepted parameters are "quickplay" or "competetive")
        required: true
        type: string
        default: none
    responses:
      200:
        description: Returns all heroes stats.
        schema:
            type: object
            items:
                $ref: '#/definitions/Ps4'
    """
    
    resp = scraper.get_qp_hero_data(btag, mode, ow_ps4)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return jsonify(resp)


"""
=====================
Korean server methods
=====================
"""
@app.route('/<string:btag>/<string:mode>/pc/kr', methods = ['GET'])
def get_pc_kr_data(btag, mode):
    """
    Get a JSON representation of all your hero's stats for PC Korean server users.
    ---
    tags:
      - PC - Korean
    parameters:
      - name: btag
        in: path
        description: Battle Tag (in format of battletag-1234 instead of battletag#1234)
        required: true
        type: string
        default: none
      - name: mode
        in: path
        description: request competetive or quickplay stats. (Accepted parameters are "quickplay" or "competetive")
        required: true
        type: string
        default: none
    responses:
      200:
        description: Returns all heroes stats for battle tags on Korean servers.
        schema:
            type: object
            items:
                $ref: '#/definitions/PC-KR'
    """
    
    resp = scraper.get_qp_hero_data(btag, mode, ow_kr_pc)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return jsonify(resp)


# @app.route('/<string:btag>/quickplay/pc/kr/', methods = ['GET'])
# def get_pc_quickplay_korea(btag):
# 	resp = scraper.get_qp_hero_data(btag, "quickplay", ow_kr_pc)
# 	return jsonify(resp)
	

# @app.route('/<string:btag>/competetive/pc/kr/', methods = ['GET'])
# def get_pc_competetive_korea(btag):
# 	resp = scraper.get_qp_hero_data(btag, "competetive", ow_kr_pc)
# 	return jsonify(resp)


"""
=====================
Europe server methods
=====================
"""
@app.route('/<string:btag>/<string:mode>/pc/eu/', methods = ['GET'])
def get_pc_eu_data(btag, mode):
    """
    Get a JSON representation of all your hero's stats for PC European server users.
    ---
    tags:
      - PC - Europe
    parameters:
      - name: btag
        in: path
        description: Battle Tag (in format of battletag-1234 instead of battletag#1234)
        required: true
        type: string
        default: none
      - name: mode
        in: path
        description: request competetive or quickplay stats. (Accepted parameters are "quickplay" or "competetive")
        required: true
        type: string
        default: none
    responses:
      200:
        description: Returns all heroes stats for battle tags on European servers.
        schema:
            type: object
            items:
                $ref: '#/definitions/PC-EU'
    """
    resp = scraper.get_qp_hero_data(btag, mode, ow_eu_pc)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return jsonify(resp)

# @app.route('/<string:btag>/quickplay/pc/eu/', methods = ['GET'])
# def get_pc_quickplay_europe(btag):
# 	resp = scraper.get_qp_hero_data(btag, "quickplay", ow_eu_pc)
# 	return jsonify(resp)
	

# @app.route('/<string:btag>/competetive/pc/eu/', methods = ['GET'])
# def get_pc_competetive_europe(btag):
# 	resp = scraper.get_qp_hero_data(btag, "competetive", ow_eu_pc)
# 	return jsonify(resp)
	

"""
======================
America server methods
======================
"""
@app.route('/<string:btag>/<string:mode>/pc/us/', methods = ['GET'])
def get_pc_us_data(btag, mode):
    """
    Get a JSON representation of all your hero's stats for PC North American server users.
    ---
    tags:
      - PC - North America
    parameters:
      - name: btag
        in: path
        description: Battle Tag (in format of battletag-1234 instead of battletag#1234)
        required: true
        type: string
        default: none
      - name: mode
        in: path
        description: request competetive or quickplay stats. (Accepted parameters are "quickplay" or "competetive")
        required: true
        type: string
        default: none
    responses:
      200:
        description: Returns all heroes stats for battle tags on Korean servers.
        schema:
            type: object
            items:
                $ref: '#/definitions/PC-NA'
    """
    resp = scraper.get_qp_hero_data(btag, mode, ow_us_pc)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return jsonify(resp)

# @app.route('/<string:btag>/quickplay/pc/us/', methods = ['GET'])
# def get_pc_quickplay_usa(btag):
# 	# print btag
# 	resp = scraper.get_qp_hero_data(btag, "quickplay", ow_us_pc)
# 	# print btag
# 	return jsonify(resp)

# @app.route('/<string:btag>/competetive/pc/us/', methods = ['GET'])
# def get_pc_competetive_usa(btag):
# 	resp = scraper.get_qp_hero_data(btag, "competetive", ow_us_pc)
# 	return jsonify(resp)


@app.route('/hello', methods = ['GET'])
def test():
	return "hello"



# for swagger
# if __name__ == '__main__':
#     app = connexion.App(__name__, specification_dir='./dist/')
#     app.add_api('swagger.yaml', arguments={'title': 'Move your app forward with the Overwatch API'})
#     app.run(port=8080)

# without swagger
if __name__== '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

	# get_hero_data("Genji")