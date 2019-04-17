import unittest

from hl.search import tokenize, score, terms_from_tags, terms, to_bofw


class TestSearch(unittest.TestCase):
    def test_tokenize(self):
        assert(tokenize("app.cloud.tld") == ['app', 'cloud', 'tld'])
        assert(tokenize("..cloud...s") == ['cloud', 's'])
        assert(tokenize("abc-s-") == ['abc', 's'])
        assert(tokenize("monkey01.m1") == ['monkey', '01', 'm', '1'])
        assert(tokenize("1-22") == ["1", "22"])
        assert(tokenize("a1b") == ["a", "1", "b"])

    def test_bofw(self):
        assert(to_bofw(["a", "a", "b", "c"]) == { "a" : 2, "b" : 1, "c" : 1})

    def test_score(self):
        q = {"a" : 1, "b": 2, "c" : 3}
        doc = { "b": 2 }
        assert(score(q, doc) == 2)
        q = { "a" : 3, "c" : 1}
        assert(score(q, doc) == 0)

    def test_terms(self):
        q = "abc12"
        assert(score(terms(q), terms_from_tags(['abc', '123'])) == 10)

if __name__ == '__main__':
    unittest.main()
