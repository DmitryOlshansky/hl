# HL support library usable for your own custom Host List tool (maybe GUI?)
# See `hl` launcher for details
#
import os
import re
import yaml
import json
from collections import namedtuple

Token = namedtuple("Token", ["tk", "w"])

spec_home = os.path.join(os.environ['HOME'], '.config', 'hl')

if not os.path.isdir(spec_home):
    try:
        os.makedirs(spec_home)
    except Exception as e:
        print(e, output=os.stderr)
        exit(1)

padded_host_pattern = re.compile(r'(.*)\[(\d+)-(\d+)\](.*)')
# Python regex fails me:
# \b doesn't break between 0-9 and a-z and look(ahead|behind) somehow doesn't fly
#
word_splitter = re.compile(r'-|_')
boundary_replacement = re.compile(r'([a-z])([0-9])|([0-9])([a-z])')

# simple 2-pass regex-based tokenizer should work for the time being
def tokenize(s):
    repl = boundary_replacement.sub(r'\1-\2', s)
    return word_splitter.split(repl)

specs = {} # hierarchical spec of tags/hosts

for root, dir, files in os.walk(spec_home):
    for f in files:
        full = os.path.join(root, f)
        if f.endswith('.yml'):
            name, _ = os.path.splitext(f)
            specs[name] = yaml.load(open(full).read())
        elif f.endswith('.json'):
            name, _ = os.path.splitext(f)
            specs[name] = json.loads(open(full).read())
        elif f.endswith('.conf'):
            # TODO: parse config files
            pass
        else:
            print("Unrecognized file in config directory", f)

def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

# replace [00x-0yz] style of ranges
# the idea is to just use integer range but
# pad with zeros to the width of the first arg in range
def padded_int_range(name):
    m = padded_host_pattern.match(name)
    if m:
        prefix, low, up, tail = m.group(1), m.group(2), m.group(3), m.group(4)
        pad = len(low)
        fill = low[0]
        for i in range(int(low), int(up)+1):
            yield prefix + str(i).rjust(pad, fill) + tail
    else:
        yield name

class RecursiveBuilder(object):
    def __init__(self, root_tag):
        self.root_tag = root_tag

    def build_recursive(self, spec, path = []):
        for tag, item in spec.items():
            if type(item) is dict and 'hosts' in item:
                self.results.append((path, item))
            elif type(item) is list:
                for h in item:
                    self.results.append((path, h))
            else:
                self.build_recursive(item, path + [tag])

    def expand_patterns(self, host_def, tags):
        patterns = host_def['hosts']
         # TODO ports defaults in HL config
        if host_def.get('ports'):
            ports = merge_dicts({'ssh' : 22}, host_def['ports'])
        else:
            ports = {'ssh' : 22}
        if type(patterns) is list:
            return [Host(h, ports, [self.root_tag] + tags) for pat in patterns for h in padded_int_range(pat)]
        else:
            return [Host(h, ports, [self.root_tag] + tags) for h in padded_int_range(patterns)]

    def build_host_list(self, spec):
        self.results = []
        self.build_recursive(spec)
        return [h for (tags, host_def) in self.results for h in self.expand_patterns(host_def, tags) ]


class Host(object):
    def __init__(self, host, ports, tags):
        self.host = host
        self.ports = ports
        self.tags = tags
        host_tokens = [Token(tk, 1) for tk in tokenize(host)]
        tag_tokens = [Token(tags, (len(tags) - i) * 10) for i, tag in enumerate(tags)]
        self.tokens = host_tokens + tag_tokens

hosts = [] # Hosts flattened from hierarchical spec
for key, spec in specs.items():
    builder = RecursiveBuilder(key)
    hosts += builder.build_host_list(spec)

def query(strings, callback):
    # TODO: find best matches
    #
    query_tokens = [tk for s in strings for tk in tokenize(s)]
    for h in hosts:
        vec = [token.w * (token.tk in query_tokens) for token in h.tokens]
        raw_tk = [token.tk for token in h.tokens]
        print(h.host, raw_tk, sum(vec))
    callback(hosts)
