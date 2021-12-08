from collections import defaultdict

from gen_items import gen_bases


def gen_ngrams():
	# first keep track of the items we have to generate ngrams for
	required = {x['name'] for x in gen_bases}
	# generate all possible ngrams
	ngrams = defaultdict(set)
	bad_ngrams = set()
	bad_bases = [
		'Atlas:', 'Map Tier:', "Haewark Hamlet", "Tirn's End", "Lex Proxima", "Lex Ejoris", "New Vastir", "Glennach Cairns", "Valdo's Rest", "Lira Arthain",
		'Academy', 'Acid Caverns', 'Alleyways', 'Ancient City', 'Arachnid Nest', 'Arachnid Tomb', 'Arcade', 'Arena', 'Arid Lake', 'Armoury', 'Arsenal', 'Ashen Wood', 'Atoll', 'Barrows', 'Basilica', 'Bazaar', 'Beach', 'Belfry', 'Bog', 'Bone Crypt', 'Bramble Valley', 'Burial Chambers', 'Cage', 'Caldera', 'Canyon', 'Carcass', 'Castle Ruins', 'Cells',
		'Cemetery', 'Channel', 'Chateau', 'City Square', 'Cold River', 'Colonnade', 'Colosseum', 'Conservatory', 'Coral Ruins', 'Core', 'Courthouse', 'Courtyard', 'Coves', 'Crater', 'Crimson Temple', 'Crimson Township', 'Crystal Ore', 'Cursed Crypt', 'Dark Forest', 'Defiled Cathedral', 'Desert', 'Desert Spring', 'Dig', 'Dry Sea', 'Dunes', 'Dungeon',
		'Estuary', 'Excavation', 'Factory', 'Fields', 'Flooded Mine', 'Forbidden Woods', 'Forge of the Phoenix', 'Forking River', 'Foundry', 'Frozen Cabins', 'Fungal Hollow', 'Gardens', 'Geode', 'Ghetto', 'Glacier', 'Grave Trough', 'Graveyard', 'Grotto', 'Haunted Mansion', 'Iceberg', 'Infested Valley', 'Ivory Temple', 'Jungle Valley', 'Laboratory', 'Lair',
		'Lair of the Hydra', 'Lava Chamber', 'Lava Lake', 'Leyline', 'Lighthouse', 'Lookout', 'Malformation', 'Marshes', 'Mausoleum', 'Maze', 'Maze of the Minotaur', 'Mesa', 'Mineral Pools', 'Moon Temple', 'Mud Geyser', 'Museum', 'Necropolis', 'Orchard', 'Overgrown Ruin', 'Overgrown Shrine', 'Palace', 'Park', 'Pen', 'Peninsula', 'Phantasmagoria', 'Pier',
		'Pit', 'Pit of the Chimera', 'Plateau', 'Plaza', 'Port', 'Precinct', 'Primordial Blocks', 'Primordial Pool', 'Promenade', 'Racecourse', 'Ramparts', 'Reef', 'Relic Chambers', 'Residence', 'Scriptorium', 'Sepulchre', 'Shipyard', 'Shore', 'Shrine', 'Siege', 'Silo', 'Spider Forest', 'Spider Lair', 'Stagnation', 'Strand', 'Sulphur Vents', 'Summit',
		'Sunken City', 'Temple', 'Terrace', 'The Beachhead', 'Thicket', 'Tower', 'Toxic Sewer', 'Tropical Island', 'Underground River', 'Underground Sea', 'Vaal Pyramid', 'Vaal Temple', 'Vault', 'Villa', 'Volcano', 'Waste Pool', 'Wasteland', 'Waterways', 'Wharf'
	]
	for item in bad_bases:
		for i in range(len(item)):
			for j in range(i + 1, len(item) + 1):
				ch = item[i:j]
				if len(ch) > 46:
					continue
				if ch[0] != ' ' and ch[-1] != ' ':
					bad_ngrams.add(ch.lower())
	for item in gen_bases:
		base = item['name'].lower()
		for x in item['strs']:
			for i in range(len(x)):
				for j in range(i + 1, len(x) + 1):
					ch = x[i:j]
					if len(ch) > 46:
						continue
					if ch[0] != ' ' and ch[-1] != ' ':
						ngrams[base].add(ch.lower())
	# remove all ngrams that are too common
	counts = defaultdict(int)
	base_pairs = defaultdict(str)
	for base in ngrams:
		ngrams[base] -= bad_ngrams
		for gram in ngrams[base]:
			counts[gram] += 1
			base_pairs[gram] += base
	for base in ngrams.copy():
		# only need to keep track of 1 unique key per base
		# double sorted for stable results
		seen_combo = set()
		for key in sorted(sorted(ngrams[base]), key=len):
			if base_pairs[key] in seen_combo:
				ngrams[base].discard(key)
			else:
				seen_combo.add(base_pairs[key])
		if not ngrams[base]:
			if base in required:
				print("*** REQUIRED ITEM ***", end=' ')
			print(f"removing {base} because it is empty")
			del ngrams[base]
	# find all bases that are a substring of other base(s)
	searchpool = sorted(ngrams, key=len)
	child = {}
	for c, base in enumerate(searchpool):
		if any(base in x for x in searchpool[c+1:]):
			child[base] = [x for x in searchpool[c+1:] if base in x]
	for c in child:
		for bigger_base in child[c]:
			ngrams[f"{bigger_base}§{c}"] = ngrams[bigger_base] - ngrams[c]

	with open('ngram_generated.py', 'w', encoding='utf-8') as f:
		f.write('subnames = {\n')
		for base in child:
			f.write(f'\t"{base}": {sorted(child[base])},\n')
		f.write('}\n\n')

		f.write('ngrams = {\n')
		for base in sorted(ngrams):
			# to keep the order stable for spotting differences
			n_sort = '", "'.join(sorted(ngrams[base]))
			f.write(f'\t"{base}": {{"{n_sort}"}},\n')
		f.write('}')


if __name__ == '__main__':
	gen_ngrams()
