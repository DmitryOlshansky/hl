#!/usr/bin/env python3
#
#
# HL is a multicall script. 
# hl-db manages configuration, adds/removes hosts,
#
# Manually add a host(s) to db
# hl-db add --tags=tag1,tag2 --kv=key1:value1,key2:values hostname1 hostname2 ...
# 
# Import from Ansible and optionally set tags + key value pairs ==
# hl-db import [--tags=tag1,tag2,.] [--kv=key1:value1,key2:value2..] 'pattern' inventory-file 
#
# Export as Ansible inventory file, key value pairs are written, tags are not ==
# hl-db export <query> [inventory-file]
#
# hl-db rm <query>
#
# Register git remote for your local HL database
# hl-db remote [git-remote] 
# Push changes to remote server
# hl-db push
# Pull changes from remote server
# hl-db pull
#
# Checkout new branch, unlike git cmd-line tool this 
# creates skeleton DB for new branch if it doesn't exists
# hl-db checkout <branch-name>
#
# For advanced users - allows to switch branches, etc.
# hl-db git [commands]
#
# git reset --hard HEAD~1
# hl-db undo
#
# List best matching hosts
# hl [--any] <query>
# (any is useful for $(hl --any "abc") substitutions)
#
# run application using app-name.json template
# hl --app-name [--opt1=xyz --opt2=kws]] <query>
#
# hl --ssh query                     | ssh to the single matching host in query, error if ambigious
# hl --ssh --any query               | ssh to any of the best matching hosts
# hl --pssh --cmd=command query      | pssh to all of best matching hosts and execute a command
# hl --cqlsh query                   | connect via cqlsh
#
# Use curl to the best matching host the using 'http' key, err if not found or ambigious
# hl --http [--opts=...] <query>/path-to-resource 
#
from hl import db
from hl import search
import os
import subprocess
import sys
import pystache
from itertools import takewhile

def process_flags(args):
    def parse(flag):
        parts = flag.split("=")
        if len(parts) == 1:
            return flag
        else:
            pieces = parts[1].split(",")
            if len(pieces) == 1:
                return { parts[0] : parts[1] }
            else:
                pairs = [p.split(":") for p in pieces]
                if all([len(p) == 1 for p in pairs]):
                    return { parts[0] : pieces }
                elif all([len(p) == 2 for p in pairs]):
                    kv = {}
                    for p in pairs:
                        kv[p[0]] = kv[p[1]]
                    return { parts[0] : kv }
                else:
                    print("Error in key-value flag {}, mixed array and k-v syntax", flag)
    flags = [x.lstrip(["-"]) for x in takewhile(lambda s: s.startswith("-"), args)]
    parsed = [parse(f) for f in flags]
    return parsed, args[len(flags):]

def add_host(base, flags, args):
    hosts = [{ 'host' : h, 'tags' : [], 'kv': {} } for h in args]
    for h in hosts:
        base.add_host(h)
    base.save()

def import_from_ansible(base, flags, args):
    out = subprocess.run(["/usr/bin/env", "ansible", "--list-hosts", "-i", args[3], args[2]], check=True)
    print(out)

def main_entry(args):
    base = db.init(os.getenv("HOME"))
    flags, args = process_flags(args)
    app = base.app(flags[0]) if len(flags) > 0 else None
    pattern = args[0]

    flags, args = process_flags(args[1:])
    if app == None:
        print(base.select(pattern))
    else:
        kw = app['defaults'].copy().update()
        cmd = pystache.render(app['single'], kw)
        os.system(cmd)

def db_entry(args):
    base = db.init(os.getenv("HOME"))
    flags = [] # TODO: extract all leading '--flag'
    handlers = {
        'add' : add_host,
        'import': import_from_ansible,
    }
    handlers[args[0]](base, flags, args[1:])


# for quick tests
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No first argument provided, expected hl or hl-db", file=sys.stderr)
        sys.exit(1)
    tool = sys.argv[1]
    if tool == "hl":
        main_entry(sys.argv[2:])
    elif tool == "hl-db":
        db_entry(sys.argv[2:])
    else:
        print("Use hl or hl-db as first argument.", file=sys.stderr)
        sys.exit(1)
