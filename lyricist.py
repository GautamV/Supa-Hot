import random
from datamuse import Datamuse

api = Datamuse()
default_syllables = 8
default_topics = [
	'cars',
	'movies',
	'books',
	'music',
	'people',
	'earth',
	'buildings',
	'games',
	'animals',
	'fruits',
	'vegetables',
	'adventures',
	'planets',
	'government',
	'enlightenment',
	'peace',
	'gangs',
	'war',
	'soul',
	'religion',
	'politics'
]

common_words = [
	'the',
	'a',
	'or',
	'and',
	'is',
	'I',
	'am',
	'who',
	'why',
	'when',
	'what',
	'where',
	'in',
	'just,'
	'this',
	'that',
	'from',
	'you',
	'know',
	'he',
	'she',
	'though',
	'yo',
	'how'
]

def drop_verse(topic=None):
	if topic is None: 
		topic = random.choice(default_topics)
	words = find_words(topic)
	
	line = random_phrase(words, default_syllables)
	line_words = line.split()
	rhymes = find_rhymes(line_words[-1])
	
	verse = line + "\n" 
	for i in range(3):
		verse = verse + suggest_next_line(line, default_syllables, rhymes, words) + "\n" 
	return verse

def suggest_next_line(line, line_syllables=None, rhymes=None, words=None):
	if line_syllables is None:
		line_syllables = count_syllables(line)
	line_words = line.split()
	rhyme, word_syllables = get_random_rhyme(line_words[-1], line_syllables, rhymes)
	if word_syllables == line_syllables: 
		return rhyme 
	if words is None:
		words = find_words(random.choice(line_words))
	return random_phrase(words, line_syllables - word_syllables) + " " + rhyme

def random_phrase(words, syllables):
	cur_syllables = 0
	phrase = ""
	while cur_syllables != syllables:
		if random.random() < 0.65:
			word, word_syllables = get_random_word(words, syllables - cur_syllables)
		else:
			word, word_syllables = random.choice(common_words), 1
		phrase = phrase + " " + word
		cur_syllables += word_syllables
	return phrase[1:]	

def get_random_word(words, max_syllables):
	syllables = random.choice(words.keys())
	while syllables > max_syllables:
		syllables = random.choice(words.keys())
	return random.choice(words[syllables])['word'], syllables 

def get_random_rhyme(word, max_syllables, rhymes=None): 
	if rhymes is None:
		rhymes = find_rhymes(word)
	return get_random_word(rhymes, max_syllables)

def find_rhymes(word):
	#print 'finding rhymes for {0}'.format(word)
	rhymes = api.words(rel_rhy=word, max=100)
	if len(rhymes) < 20:
		rhymes += api.words(rel_nry=word, max=100)
	if len(rhymes) == 0: 
		return find_rhymes(get_similar_word(word))
	return categorize_by_syllable(rhymes)

def get_similar_word(word):
	if word.endswith('ism'):
		sim_word = 'prism'
	elif word.endswith('woman'):
		sim_word = 'woman'
	elif word.endswith('ilmed'):
		sim_word = 'chilled'
	elif word.endswith('ic'):
		sim_word = 'pick'
	elif word.endswith('eated'):
		sim_word = 'heated'
	elif word.endswith('ief'):
		sim_word = 'chief'
	elif word.endswith('ology'):
		sim_word = 'biology'
	elif word.endswith('ues'):
		sim_word = 'fuse'
	elif word.endswith('orbs'):
		sim_word = 'pores'
	elif word.endswith('erent'):
		sim_word = 'adherent'
	elif word.endswith('ist'):
		sim_word = 'fist'
	elif word.endswith('a'):
		sim_word = 'la'
	elif word.endswith('o') or word.endswith('oh'):
		sim_word = 'go'
	elif word.endswith('u'):
		sim_word = 'too'
	elif word.endswith('i'):
		sim_word = 'pie'
	elif word.endswith('ate'):
		sim_word = 'late'
	elif word.endswith('thon'):
		sim_word = 'pawn'
	elif word.endswith('isional'):
		sim_word = 'divisional'
	elif word.endswith('esis'):
		sim_word = 'thesis'
	elif word.endswith('ity'):
		sim_word = 'city'
	elif word.endswith('ude'):
		sim_word = 'food'
	elif word.endswith('ere') or word.endswith('eres'):
		sim_word = 'here'
	elif word.endswith('uke') or word.endswith('ukes'):
		sim_word = 'duke'
	elif word.endswith('b'):
		sim_word = 'see'
	elif word.endswith('ot'):
		sim_word = 'got'
	elif word.endswith('won'):
		sim_word = 'fun'
	elif word.endswith('onical'):
		sim_word = 'canonical'
	elif word.endswith('en'):
		sim_word = 'pen'
	elif word.endswith('ith'):
		sim_word = 'with'
	elif word.endswith('ation'):
		sim_word = 'vacation'
	elif word.endswith('od'):
		sim_word = 'odd'
	else: 
		#print "no rhymes for {0}".format(word)
		sim_word = 'cat'
	return sim_word

def find_words(topic):
	words = api.words(topics=topic, md='s', max=500)
	while len(words) < 50:
		words += api.words(topics=random.choice(default_topics), max=100)
	return categorize_by_syllable(words)

def categorize_by_syllable(words):
	words_by_syllable = {}
	for word in words: 
		num_syllables = word.get('numSyllables', -1)
		if num_syllables == -1:
			num_syllables = count_syllables(word['word'])
		if num_syllables in words_by_syllable:
			words_by_syllable[num_syllables].append(word)
		else:
			words_by_syllable[num_syllables] = [word]
	return words_by_syllable

def count_syllables(word):
    if not word:
    	return 0
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels and word[0] != 'y':
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels:
        	if word[index - 1] not in vowels: 
        		count += 1
        	elif word[index - 1] == 'y' and word[index] != 'y':
        		count += 1
        	elif word[index - 1] == 'i' and word[index] == 'a':
        		count += 1
    if word.endswith('e'):
    	if not (word[-2] == 'l' and word[-3] not in vowels):
        	count -= 1
    elif word.endswith('sm'):
    	count += 1
    if count == 0:
        count += 1
    return count
