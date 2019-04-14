# Module for building inverted index + scoring

def tokenize(text):
	pieces = []
	i = 0
	j = 0
	cur = ' '
	while i < len(text):
		prev = cur
		cur = text[i]
		if cur == '-' or cur == '.':
			if i != j:
				pieces.append(text[j:i])
			j = i + 1
		elif (cur.isdigit() ^ prev.isdigit()):
			if i != j:
				pieces.append(text[j:i])
			j = i
		i += 1
	if j < i:
		pieces.append(text[j:i])
	return pieces


def test_tokenize():
	assert(tokenize("app.cloud.tld") == ['app', 'cloud', 'tld'])
	assert(tokenize("..cloud...s") == ['cloud', 's'])
	assert(tokenize("abc-s-") == ['abc', 's'])
	assert(tokenize("monkey01.m1") == ['monkey', '01', 'm', '1'])
	assert(tokenize("1-22") == ["1", "22"])
	assert(tokenize("a1b") == ["a", "1", "b"])

# Bag Of Words
def to_bofw(tokens):
	kv = {}
	for tk in tokens:
		kv[tk] = kv.get(tk, 0) + 1
	return kv


def test_bofw():
	assert(to_bofw(["a", "a", "b", "c"]) == { "a" : 2, "b" : 1, "c" : 1})


def inverted_index_of(items):
	tks = [to_bofw(tokenize(x)) for x in items]
