from bs4 import BeautifulSoup, NavigableString
import urllib
import json
import collections
import re

# ow_us_pc = "https://playoverwatch.com/en-us/career/pc/us/"
# ow_eu_pc "https://playoverwatch.com/en-us/career/pc/eu/"


def get_possible_heros():

	with open("poss_heros.txt") as f:
		possible_heros = f.read().splitlines()

	for i in range(0, len(possible_heros)):
		torb_match = re.match("Torb", possible_heros[i])
		lucio_match = re.match("L", possible_heros[i])
		if torb_match:
			possible_heros[i] = "Torbjorn"
		if lucio_match:
			possible_heros[i] = "Lucio"
	return possible_heros



def get_comp_hero_data(btag):
	response = urllib.open(ow_default_endpoint + btag).read()
	soup = BeautifulSoup(response, "lxml")



def get_qp_hero_data(btag, mode, endpoint):

	# print "mode: " + str(mode)
	if mode == "quickplay":
		print "setting qp to true"
		quickplay = True
	elif mode == "competetive":
		quickplay = False

	# get the html data from the endpoint + whatever battletag 
	response = urllib.urlopen(endpoint + btag).read()
	soup = BeautifulSoup(response, "lxml")

	# stats are organized by a card stat div element
	card_stats = soup.findAll("div", {"class": "card-stat-block"})

	# iterate through the card stats and append each category of stats to a list
	categories = []
	for card in card_stats:
		
		if card.span.string in categories:
			break;

		categories.append(card.span.string)

	# print categories

	# data groups is a list containing both quickplay and comp stats. 
	# The first half of this list is quickplay data while the last half is comp data.
	data_groups = soup.findAll("div", {"data-group-id": "stats"})

	# names is a list containing the names of all heroes the user has played for both
	# quickplay and competetive in the first and last half of the list, 
	# plus some extra unwanted data surrounding both halves.
	names = soup.findAll("option")

	# clean_names_up() replaces Lucio and Torbjorn with utf-8 encoding to handle
	# the spelling of their names.
	names = clean_names_up(names)

	for name in names:
		print name["option-id"]

	# get_hero_index() will go through the names list and return the start 
	# and end indeces where the hero names reside.
	hero_start_index, hero_end_index = get_hero_indices(names, quickplay)

	# use the indeces to subset the names list to contain only heros wanted
	heros = names[hero_start_index:hero_end_index]

	comp_heros_dgs = names[36:(len(names) - 7)]

	comp_heros = []
	for hero in comp_heros_dgs:
		comp_heros.append(hero["option-id"])
	# print comp_heros

	# heros is a list of html tags, loop through this to find the string representation
	# of the hero and append to a list of heros
	hero_list = []
	for hero in heros:
		hero_list.append(hero["option-id"])


	qp_dgs = data_groups[0:len(hero_list)]
	comp_dgs = data_groups[23:len(data_groups)]
	# print len(qp_dgs)


	# print("\n...About to pass in " + str(qp_dgs) + " and " + str(hero_list) + " to get_all_heros_json method...")
	print json.dumps(get_all_heros_json(qp_dgs, hero_list), indent = 4)
	return get_all_heros_json(qp_dgs, hero_list)



def get_hero_indices(names, quickplay):

	print "in get_hero_indices"
	if quickplay:
		print "quickplay was true"
		names = clean_names_up(names)
		poss_heros = get_possible_heros()
		i = 0
		found_start_index = False
		for name in names:
			hero_name = name["option-id"]
			if hero_name in poss_heros:
				if not found_start_index:
					hero_start_index = i
					found_start_index = True
			if found_start_index and hero_name not in poss_heros:
				hero_end_index = i
				return hero_start_index, hero_end_index
			i += 1
	else:
		# logic for returning competetive hero indeces here
		names = clean_names_up(names)
		poss_heros = get_possible_heros()
		i = 0
		for name in names:
			pass



def clean_names_up(names):

	i = 0
	for name in names:

		hero_name = name["option-id"]

		# print "Hero from web scraping: " + hero_name

		torb_match = re.match("Torb", hero_name)
		lucio_match = re.match("L", hero_name)

		if torb_match:
			# print "Found a match with " + hero_name 
			names[i]["option-id"] = "Torbjorn"
			# replaced_torb = True
		if lucio_match:
			# print "Found a match with " + hero_name
			names[i]["option-id"] = "Lucio"
			# replaced_lucio = True
		i += 1
	return names


def get_all_heros_json(hero_data_groups, hero_list):
	full_resp = collections.OrderedDict()
	i = 0
	for hero_tag in hero_data_groups:
		full_resp[hero_list[i]] = make_json_categories_keys(hero_tag)
		i += 1
	return full_resp


def make_json_categories_keys(hero_tag):
	# print("\n\nMaking JSON categories out of: " + str(hero_tag))
	inner = {}
	cat_response = collections.OrderedDict()

	for child in hero_tag.descendants:
		# pharah_test_response["Pharah"] = child
		if isinstance(child, NavigableString):
			continue
		if child.has_attr("class"):
			# found the child tag that corresponds to the category of stats 
			# (Assists, Deaths, etc...)
			if child["class"][0] == "stat-title":
				inner[child.string] = ""
				# print child.string + ": {"
				for parent in child.parents:
					data_response = collections.OrderedDict()
					if parent.name == "thead":
						next_data_group = parent.next_sibling
						# print next_data_group
						list_of_data =  next_data_group.findAll("td")

						# print(child.string + ":\n")

						for i in range(0, len(list_of_data)):
							# even indices are data title, odd indices are data values
							if i % 2 == 0:
								data_response[list_of_data[i].string] = list_of_data[i + 1].string
						cat_response[child.string] = data_response

	return cat_response




gianny = "boludo00-1183"
tuck = "xTuckNastyy-1211"
peter = "PKeks-1544"
swede_guy = "Zebbosai-2381"

if __name__ == "__main__":
	print "Data for " + peter
	get_qp_hero_data(peter, "quickplay", "https://playoverwatch.com/en-us/career/pc/us/")



