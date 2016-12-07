import urllib2
import json
import requests
import pandas as pd

debug = 0

def get_info():
	valid_sys = ['pc', 'xbl', 'psn']
	valid_regs = ['us', 'eu', 'kr', 'cn', 'global']
	valid_heroes = ["Genji",
					"McCree",
					"Pharah",
					"Reaper",
					"Soldier 76",
					"Tracer",
					"Bastion",
					"Hanzo",
					"Junkrat",
					"Mei",
					"Torbjorn",
					"Widowmaker",
					"D.va",
					"Reinhardt",
					"Roadhog",
					"Winston",
					"Zarya",
					"Ana",
					"Lucio",
					"Mercy",
					"Symmetra",
					"Zenyatta"]
	flag = 1
	while flag:
		sys = raw_input("Please enter your system: ")
		if sys in valid_sys:
			break
		else:
			print "Please enter 'pc', 'xbl', or 'psn'."
	while flag:
		reg = raw_input("Please enter your region: ")
		if reg in valid_regs:
			break
		else:
			print "Please enter 'us', 'eu', 'kr', 'cn', or 'global'"
	while flag:
		hero = raw_input("What hero do you want data for? ")
		if hero in valid_heroes:
			break
		else:
			print "Please enter a valid hero name. Options are: \n"
			print valid_heroes
	battle_tag = raw_input("Enter battle_tag: ")

	return sys, reg, battle_tag, hero

if debug:
	url = "https://api.lootbox.eu/pc/us/boludo00-1183/quick-play/hero/Genji/"
else:
	sys, reg, battle_tag, hero = get_info()
	url = "https://api.lootbox.eu/" + sys + "/" + reg + "/" + battle_tag + "/quick-play/hero/" + hero +"/"

print "Getting request..."
request = requests.get(url=url)
data = json.loads(request.text)

df = pd.DataFrame(data)

print df
