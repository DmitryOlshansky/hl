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
# hl --ssh [--cmd='command to run'] query     | ssh to a random of best matching hosts in query, error if ambigious
# hl --ssh --any query                        | ssh to any of the best matching hosts
# hl --all --pssh --cmd=command query         | pssh to all of best matching hosts and execute a command
# hl --cqlsh query                            | connect via cqlsh to a random matching host
#
# Use curl to the best matching host the using 'http' key, err if not found or ambigious
# hl --http [--url=...] [--data=...] <query>
#
from hl import db
from hl import search
import json
import os
import random
import subprocess
import string
import sys
import pystache
from itertools import takewhile

def flags_from(args):
    def parse(flag):
        parts = flag.split("=")
        if len(parts) == 1:
            return { flag : True }
        else:
            flag_name = parts[0]
            flag_value = parts[1]
            pieces = flag_value.split(",")
            if len(pieces) == 1 and not ":" in flag_value:
                return { flag_name : flag_value }
            else:
                pairs = [p.split(":") for p in pieces]
                if all([len(p) == 1 for p in pairs]):
                    return { flag_name : pieces }
                elif all([len(p) == 2 for p in pairs]):
                    kv = {}
                    for p in pairs:
                        kv[p[0]] = p[1]
                    return { flag_name : kv }
                else:
                    print("Error in key-value flag {}, mixed array and k-v syntax", flag)
    flags = [x.lstrip("-") for x in takewhile(lambda s: s.startswith("-"), args)]
    parsed = [parse(f) for f in flags]
    result = {}
    for f in parsed: result.update(f)
    return result, args[len(flags):]

def add_host(base, flags, args):
    hosts = [{ 'host' : h, 'tags' : [], 'kv': flags } for h in args]
    for h in hosts:
        base.hosts.add(h)
    base.save_hosts()

def show_apps(base, flags, args):
    os.execv("/usr/bin/env", ["/usr/bin/env", "xdg-open", base.appsdir])

def show_hosts(base, flags, args):
    os.execv("/usr/bin/env", ["/usr/bin/env", "xdg-open", base.hosts_path])

def import_from_ansible(base, flags, args):
    proc = subprocess.Popen(["/usr/bin/env", "ansible", "--list-hosts", "-i", args[1], args[0]], stdout=subprocess.PIPE)
    lines = proc.communicate(timeout=10)[0].decode('utf-8').split("\n")
    hosts = [line.strip() for line in lines]
    hosts = filter(lambda h: len(h) != 0, hosts[1:])
    add_host(base, flags, hosts)

def json_hosts(base, flags, args):
    base = db.init(os.getenv("HOME"))
    pattern = args[0] if len(args) > 0 else ""
    hosts = base.hosts.list(pattern)
    for h in hosts:
        print(json.dumps(h))

def main_entry():
    args = sys.argv[1:]
    base = db.init(os.getenv("HOME"))
    flags, args = flags_from(args)
    useAnyAll = "default"
    if "any" in flags and "all" in flags:
        print("Only one of --any or --all allowed", file=sys.stderr)
        exit(1)
    elif "any" in flags:
        useAnyAll = "any"
        del flags["any"]
    elif "all" in flags:
        useAnyAll = "all"
        del flags["all"]
    #TODO: `--any` and `--all` handling
    app = base.app(list(flags.keys())[0]) if len(flags) > 0 else None
    if len(args) == 0:
        pattern = ""
    else:
        pattern = args[0]
        args = args[1:]
    flags, args = flags_from(args)
    hosts = base.hosts.list(pattern)
    def pick_any(items):
        if len(items) == 0:
            return []
        else:
            r = random.randint(0, len(items)-1)
            return items[r:r+1]

    if app == None:
        # default is all
        if useAnyAll == "any":
            hosts = pick_any(hosts)
        for host in hosts:
            print(host['host'])
    else:
        # default is any
        if useAnyAll != "all":
            hosts = pick_any(hosts)
        for h in hosts:
            kv = app['defaults'].copy()
            kv.update(h['kv'])
            kv.update(flags)
            kv.update({ 'host' : h['host'] })
            cmd = pystache.render(app['single'], kv)
            os.system(cmd)

def db_entry():
    args = sys.argv[1:]
    base = db.init(os.getenv("HOME"))
    handlers = {
        'add' : add_host,
        'apps': show_apps,
        'import': import_from_ansible,
        'hosts': show_hosts,
        'json': json_hosts
    }
    if len(args) == 0 or not args[0] in handlers.keys():
        print("Expected any of (%s) as first argument" % ", ".join(handlers.keys()))
        exit(1)
    cmd = args[0]
    flags, args = flags_from(args[1:])
    handlers[cmd](base, flags, args)
