from flask import Flask, jsonify
import scraper


app = Flask(__name__)

@app.route('/')
def index():
	return "Index Page"


@app.route('/quickplay/<string:btag>', methods = ['GET'])
def get_quickplay(btag):
	print btag
	resp = scraper.get_qp_hero_data("Genji", btag, "quickplay")
	print btag
	return jsonify(resp)

def get_competetive(btag):
	jsonify(scraper.get_qp_hero_data("asdhasf", btag, "competetive"))

@app.route('/hello', methods = ['GET'])
def test():
	return "hello"


if __name__== '__main__':
	app.run(debug = True)
	# get_hero_data("Genji")