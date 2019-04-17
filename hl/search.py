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

"""Bag OF Words - bofw"""
def to_bofw(tokens):
	kv = {}
	for tk in tokens:
		kv[tk] = kv.get(tk, 0) + 1
	return kv

def terms(s):
	return to_bofw(tokenize(s))

def terms_from_tags(tags):
	kv = {}
	for t in tags:
		kv[t] = 512
	return kv

"""Score of query bofw vs document bofw"""
def score(qtk, htk):
	result = 0
	v = 0
	for q, freq in qtk.items():
		v = htk.get(q, 0)
		if v > 0:
			result += 1 + math.log(v, 2)
	return result

