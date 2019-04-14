import math

# our simple tokenizer for hostnames
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

"""Bag OF Words - bofw"""
def to_bofw(tokens):
	kv = {}
	for tk in tokens:
		kv[tk] = kv.get(tk, 0) + 1
	return kv


def test_bofw():
	assert(to_bofw(["a", "a", "b", "c"]) == { "a" : 2, "b" : 1, "c" : 1})

def terms(s):
	return to_bofw(tokenize(s))

"""Score of query bofw vs document bofw"""
def score(qtk, htk):
	result = 0
	v = 0
	for q, freq in qtk.items():
		v = htk.get(q, 0)
		if v > 0:
			result += 1 + math.log(v, 2)
	return result

def test_score():
	q = {"a" : 1, "b": 2, "c" : 3}
	doc = { "b": 2 }
	assert(score(q, doc) == 2)
	q = { "a" : 3, "c" : 1}
	assert(score(q, doc) == 0)
