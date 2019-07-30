import json
from hl import search

def ensure(cond, err):
    if not cond: raise Exception(err)

def check_host(h):
    ensure(type(h['host']) is str, "host name must be string")
    ensure(type(h['tags']) is list, "tags is a list")
    ensure(type(h['kv']) is dict, "key-value pairs is object")

class HList(object):
    def __init__(self, nd_json=None):
        if not nd_json:
            self.hosts = []
        else:
            self.hosts = [json.loads(line) for line in nd_json.split("\n") if line.strip() != '']
            for h in self.hosts: check_host(h)

    def __str__(self):
        return "\n".join([json.dumps(h) for h in self.hosts])

    """
        Adds or replace one properly structured host entry
    """
    def add(self, host):
        check_host(host)
        for i in range(len(self.hosts)):
            if self.hosts[i] == host:
                self.hosts[i] = host
                return
        self.hosts.append(host)

    """
        Remove hosts matching query
    """
    def remove_by_query(self, query):
        to_remove = set(self.select(query))
        to_keep = [self.hosts[i] for i in range(len(self.hosts)) if i not in to_remove]
        self.hosts = to_keep

    """
        List hosts matching query
    """
    def list(self, query):
        return [self.hosts[i] for i in self.select(query)]

    """
        Return indices of best matching host entries
    """
    def select(self, query):
        if query == "":
            return range(len(self.hosts))
        if len(self.hosts) == 0:
            return []
        qt = search.terms(query)
        hts = [search.terms(h['host']) for h in self.hosts]
        scores = [search.score(qt, ht) for ht in hts]
        best = max(scores)
        if best == 0:
            return []
        else:
            return [pair[0] for pair in enumerate(scores) if pair[1] == best]

