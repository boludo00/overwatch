import urllib2
import json
import requests
import scraper

debug = 0

api_endpoint = "https://enhanced-ow-api.herokuapp.com/"

def get_info():
	valid_sys = ['pc', 'xbl', 'psn']
	valid_regs = ['us', 'eu', 'kr', 'cn', 'global']

	valid_heroes = scraper.get_possible_heros()


	flag = 1
	while flag:
		sys = raw_input("Please enter your system:\n" + str(valid_sys) + "\n")
		if sys in valid_sys:
			break
		else:
			print "Please enter 'pc', 'xbl', or 'psn'."
	while flag:
		reg = raw_input("Please enter your region:\n" + str(valid_regs) + "\n")
		if reg in valid_regs:
			break
		else:
			print "Please enter 'us', 'eu', 'kr', 'cn', or 'global'"
	while flag:
		hero = raw_input("What hero do you want data for?\n" + str(valid_heroes) + "\n")
		if hero in valid_heroes:
			break
		else:
			print "Please enter a valid hero name. Options are: \n"
			print valid_heroes
	while flag:
		mode = raw_input("quickplay or competetive? Enter [qp] or [comp]" + "\n")

		if mode == "qp":
			mode = "quickplay"
			break
		elif mode == "comp":
			mode = "competetive"
			break
		else:
			print "Please enter [qp] or [comp]"


	battle_tag = raw_input("Enter battle_tag: ")

	return sys, reg, battle_tag, mode, hero


def start_prompt(debug=False):
	if debug:
		url = "https://api.lootbox.eu/pc/us/boludo00-1183/quick-play/hero/Genji/"
	else:
		sys, reg, battle_tag, mode, hero = get_info()
		if(sys == "pc"):
			url = api_endpoint + battle_tag + "/" + mode + "/" + sys + "/" + reg + "/"
		else:
			url = api_endpoint + battle_tag + "/" + mode + "/" + sys + "/"

	print "Getting request at url " + url
	request = requests.get(url=url)

	json_req = request.json()

	returned_hero = {}
	returned_hero[hero] = json_req[hero]

	print json.dumps(returned_hero, indent = 4)