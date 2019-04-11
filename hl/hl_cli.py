#!/usr/bin/env python3
#
# HL is a multicall script. 
# hl-db manages configuration, adds/removes hosts,
# (any is useful for $(hl --any "abc") substitutions)
# hl [--any] <query>
# hl --app [--opt1=xyz --opt2=kws]] <query>
#
# Import from Ansible and optionally set tags + key value pairs ==
# hl-db import [--tags=tag1,tag2,.] [--kv=key1:value1,key2:value2..] 'pattern' inventory-file 
#
# Export as Ansible inventory file, key value pairs are written, tags are not ==
# hl-db export <query> [inventory-file]
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
# For advanced users - allows to switch branches
# hl-db git [commands]
#
# git reset --hard HEAD~1
# hl-db undo


# hl --ssh query                     | ssh to the single matching host in query, error if ambigious
# hl --ssh --any query               | ssh to any of the best matching hosts
# hl --pssh --cmd=command query      | pssh to all of best matching hosts and execute a command
# hl --cqlsh query                   | connect via cqlsh
#
# Use curl to the best matching hosts the using 'http' key, err if not found or ambigious
# hl --http [--opts=...] <query>/path-to-resource 
#
#
try:
    from hl import hl
except:
    import hl

import os
import sys


def run_ssh(hosts):
    if len(hosts) != 1:
        print("Ambigious query, matches multiple hosts:")
        for h in hosts:
            print("   %s" % h.host)
    else:
        target = hosts[0]
        cmd = "ssh %s" % hosts[0].host
        os.execv("/usr/bin/env", ["/usr/bin/env", "ssh", hosts[0].host])

# for quick tests
if __name__ == "__main__":
    import sys
    if sys.argv[1] == "query":
        sys.argv = sys.argv[1:]
        main_list()
    elif sys.argv[1] == "ssh":
        sys.argv = sys.argv[1:]
        main_ssh()
    else:
        # TODO: use argv[0] to determine the service to call
        print("Unrecognized service: %s" % sys.argv[1])
