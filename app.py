from flask import Flask, jsonify
import scraper
import os

app = Flask(__name__)


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
	return "Index Page"


"""
============
Xbox methods
============
"""
@app.route('/<string:btag>/quickplay/xbl/', methods = ['GET'])
def get_xbox_quickplay(btag):
	resp = scraper.get_qp_hero_data(btag, "quickplay", ow_xbox)
	return jsonify(resp)

@app.route('/<string:btag>/competetive/xbl/', methods = ['GET'])
def get_xbox_competetive(btag):
	resp = scraper.get_qp_hero_data(btag, "competetive", ow_xbox)
	return jsonify(resp)



"""
===========
Ps4 methods
===========
"""
@app.route('/<string:btag>/quickplay/psn/', methods = ['GET'])
def get_ps4_quickplay(btag):
	resp = scraper.get_qp_hero_data(btag, "quickplay", ow_ps4)
	return jsonify(resp)

@app.route('/<string:btag>/competetive/psn/', methods = ['GET'])
def get_ps4_competetive(btag):
	resp = scraper.get_qp_hero_data(btag, "competetive", ow_ps4)
	return jsonify(resp)



"""
=====================
Korean server methods
=====================
"""
@app.route('/<string:btag>/quickplay/pc/kr/', methods = ['GET'])
def get_pc_quickplay_korea(btag):
	resp = scraper.get_qp_hero_data(btag, "quickplay", ow_kr_pc)
	return jsonify(resp)
	

@app.route('/<string:btag>/competetive/pc/kr/', methods = ['GET'])
def get_pc_competetive_korea(btag):
	resp = scraper.get_qp_hero_data(btag, "competetive", ow_kr_pc)
	return jsonify(resp)


"""
=====================
Europe server methods
=====================
"""
@app.route('/<string:btag>/quickplay/pc/eu/', methods = ['GET'])
def get_pc_quickplay_europe(btag):
	resp = scraper.get_qp_hero_data(btag, "quickplay", ow_eu_pc)
	return jsonify(resp)
	

@app.route('/<string:btag>/competetive/pc/eu/', methods = ['GET'])
def get_pc_competetive_europe(btag):
	resp = scraper.get_qp_hero_data(btag, "competetive", ow_eu_pc)
	return jsonify(resp)
	

"""
======================
America server methods
======================
"""
@app.route('/<string:btag>/quickplay/pc/us/', methods = ['GET'])
def get_pc_quickplay_usa(btag):
	# print btag
	resp = scraper.get_qp_hero_data(btag, "quickplay", ow_us_pc)
	# print btag
	return jsonify(resp)

@app.route('/<string:btag>/competetive/pc/us/', methods = ['GET'])
def get_pc_competetive_usa(btag):
	resp = scraper.get_qp_hero_data(btag, "competetive", ow_us_pc)
	return jsonify(resp)


@app.route('/hello', methods = ['GET'])
def test():
	return "hello"


if __name__== '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

	# get_hero_data("Genji")