# HL support library usable for your own custom Host List tool (maybe GUI?)
# See `hl` launcher for details
# 
import os
import re
import yaml
import json
from collections import namedtuple

spec_home = os.path.join(os.environ['HOME'], '.config', 'hl')

if not os.path.isdir(spec_home):
    try:
        os.makedirs(spec_home)
    except Exception as e:
        print(e, output=os.stderr)
        exit(1)

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
    pass

Host = namedtuple("Host", ["host", "ports", "tags"])

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
            return [Host(h, ports, [self.root_tag] + tags) for h in patterns]
        else:
            return [Host(patterns, ports, [self.root_tag] + tags)]

    def build_host_list(self, spec):
        self.results = []
        self.build_recursive(spec)
        return [h for (tags, host_def) in self.results for h in self.expand_patterns(host_def, tags) ]


hosts = [] # Hosts flattened from hierarchical spec
for key, spec in specs.items():
    builder = RecursiveBuilder(key)
    hosts += builder.build_host_list(spec)


def query(strings, callback):
    for h in hosts:
        callback(h)
