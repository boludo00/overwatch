from bs4 import BeautifulSoup, NavigableString
import urllib
import json
import collections
import re
import get_data

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
			break

		categories.append(card.span.string)


	# data groups is a list containing both quickplay and comp stats.
	# The first half of this list is quickplay data while the last half is comp data.
	data_groups = soup.findAll("div", {"data-group-id": "stats"})

	# names is a list containing the names of all heroes the user has played for both
	# quickplay and competetive in the first and last half of the list,
	# plus some extra unwanted data surrounding both halves.
	names = soup.findAll("option")
	# print "DEBUG: " +str(names)

	# clean_names_up() replaces Lucio and Torbjorn with utf-8 encoding to handle
	# the spelling of their names.
	names = clean_names_up(names)

	# print "DEBUG: " + str(names)
	if quickplay:

		hero_start_index, hero_end_index = get_qp_hero_indices(names)
		# use the indeces to subset the names list to contain only heros wanted
		heros = names[hero_start_index:hero_end_index]

		# heros is a list of html tags, loop through this to find the string representation
		# of the hero and append to a list of heros
		qp_hero_list = []
		for hero in heros:
			qp_hero_list.append(hero["option-id"])

		dgs = data_groups[0:len(qp_hero_list)]

		# for thing in dgs:
		# 	print thing

		# print json.dumps(get_all_heros_json(dgs, qp_hero_list), indent = 4)
		return get_all_heros_json(dgs, qp_hero_list)

	else:

		# # maintain a list of heros that have already been seen.
		# # push heros onto list as you see them. when you encounter
		# # a hero again, record the index where you found the first duplicate
		# # then go locate the last name that shows up in the list being looped
		# # through. Record that as the ending index.
		heros_seen = []
		comp_heros = []
		looped_through_first = False
		started_second_round = False
		missed_because_looped_around = False
		found_first_index = False
		i = 0
		for name in names:
			if(name["option-id"] in get_possible_heros()):
				found_first_hero = True
				# print("Found name " + name["option-id"] + " that is in: " + str(get_possible_heros()))
				heros_seen.append(name["option-id"])
				looped_through_first = True


				if looped_through_first and missed_because_looped_around:
					comp_heros.append(name["option-id"])
					# this is the case where you come across the first appearance of the the second
					# set of names (corresponding to competetive), so remember this index
					if not found_first_index:
						hero_start_index = i

			else:

				# this is the case where you looped through all hero names in the
				# competetive portion of the list. remember the index of the last hero seen.
				# can break out of loop now.
				if(found_first_index):
					hero_end_index = i
					# print("Just found the last hero index i(in competetive) for " + name["option-id"] + " to be " + str(hero_end_index))
					break

				# print("Didnt find a match...")
				if looped_through_first:
					# print("But we already found the first half...")
					started_second_round = True
					missed_because_looped_around = True

			# print(name["option-id"] + " at index " + str(i))
			i += 1


		hero_start_index, hero_end_index = get_qp_hero_indices(names)
		
		# use the indeces to subset the names list to contain only heros wanted
		heros = names[hero_start_index:hero_end_index]

		# heros is a list of html tags, loop through this to find the string representation
		# of the hero and append to a list of heros
		qp_hero_list = []
		for hero in heros:
			qp_hero_list.append(hero["option-id"])


		comp_start_index = len(qp_hero_list)
		comp_end_index = len(data_groups)

		dgs = data_groups[comp_start_index:comp_end_index]

		# print json.dumps(get_all_heros_json(dgs, comp_heros), indent = 4)
		return get_all_heros_json(dgs, comp_heros)



def get_qp_hero_indices(names):

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



def clean_names_up(names):

	i = 0
	for name in names:

		hero_name = name["option-id"]

		torb_match = re.match("Torb", hero_name)
		lucio_match = re.match("L", hero_name)

		if torb_match:
			names[i]["option-id"] = "Torbjorn"
		if lucio_match:
			names[i]["option-id"] = "Lucio"
		i += 1
	return names


def get_all_heros_json(hero_data_groups, hero_list):

	full_resp = collections.OrderedDict()
	i = 0

	for hero_tag in hero_data_groups:
		print i
		print "Hero tag: ", hero_list[i]
		full_resp[hero_list[i]] = make_json_categories_keys(hero_tag)
		i += 1
	return full_resp



def make_json_categories_keys(hero_tag):

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
