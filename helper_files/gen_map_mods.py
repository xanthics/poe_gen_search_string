from json import load


def gen_mods():
	with open(r'C:\git\RePoE\RePoE\data\mods.json', 'r') as f:
		mods = load(f)
	with open(r'C:\git\RePoE\RePoE\data\stat_translations.json', 'r') as f:
		stats = load(f)

	map_mods = set()
	for mod in mods:
		if mods[mod]['generation_type'] in ['prefix', 'suffix'] and (any(x['weight'] > 0 for x in mods[mod]['spawn_weights'] if 'tier_map' in x['tag']) or (mods[mod]['domain'] == 'area' and any(x['weight'] > 0 for x in mods[mod]['spawn_weights'] if x['tag'] == 'default'))):
			for stat in mods[mod]['stats']:
				map_mods.add(stat['id'])
	map_mods.remove('dummy_stat_display_nothing')
	map_strings = set()
	bad_mods = {
		'Ground Effect has a radius of {0}',
		'Player chance to Dodge is Lucky',
		'Players gain {0}% increased Flask Charges',
		'Players have {0}% increased Chance to Block',
		'Players have {0}% more Area of Effect',
		'Players have {0}% more Armour',
		'Players have {0}% more Recovery Rate of Life and Energy Shield',
		'Unique Boss has {0}% reduced Area of Effect',
		'Unique Boss has {0}% reduced Life',
		'{0} patches with Ground Effect per 100 tiles',
		'{0}% Monster Life Leech Resistance',
		'{0}% Monster Mana Leech Resistance',
		'{0}% more effect of Curses on Monsters',
		'{0}% to Monster Critical Strike Multiplier',
		'{0}% reduced Monster Movement Speed',
		'Monsters have {0}% reduced Accuracy Rating',
		'Monsters have {0}% reduced Area of Effect',
		'Monsters have {0}% reduced Critical Strike Chance',
		'Monsters take {0}% increased Extra Damage from Critical Strikes',
		'Players Prevent {0}% of Suppressed Spell Damage',
		'Players fire {1} additional Projectiles',
		'Buffs on Players expire {0}% slower',
		"Players have {0}% more Accuracy Rating",
		"Players have {0}% more Cooldown Recovery Rate",
		"Players have {0}% increased effect of Non-Curse Auras from Skills",
	}
	found_mods = set()
	for stat in stats:
		if any(x in map_mods for x in stat['ids']):
			for x in stat['ids']:
				found_mods.add(x)
			for modstr in stat['English']:
				if modstr['string'] not in bad_mods:
					map_strings.add(modstr['string'])
	print('\n'.join(sorted(map_strings)))
	if map_mods - found_mods:
		print("\n*** Missing mods ***\n" + '\n'.join(map_mods - found_mods) + "\n*** Missing mods ***\n")
	if __name__ == "__main__":
		f = open('../gen_items.py', 'w')
	else:
		f = open('gen_items.py', 'w')

	f.write('gen_bases = [\n\t')
	f.write(',\n\t'.join([f'{{"name": "{x.replace("{0}", "#")}", "strs": {list(x.replace(" {0}", "{0}").replace("{0} ", "{0}").split("{0}"))}}}' for x in sorted(map_strings)]))
	f.write('\n]')


if __name__ == '__main__':
	gen_mods()