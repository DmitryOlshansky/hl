#!/usr/bin/env python3
#
# HL is a multicall script, depending on name hl tool does:
# hl query                           | list hosts by query
# hl-all query                       | find hosts and list protocols, tab separated
# hl-ssh query                       | ssh to the single matching host in query, error if ambigious
# hl-pssh query -- command line      | pssh 
# hl-<tool-name> query               | run tool using pattern from hl config
#
# Host lists are looked up as YAML here:
#
# ~/.config/hl/<project>.yml         | project name is just another tag (with highest weight)
#
# Same host lists can be in JSON:
# ~/.config/hl/<project>.json        | same semantics as YML lists
#
# Configs of HL itself:              | 
# ~/.config/hl/*.conf                | also use YAML syntax but .conf extension
#
#
# PS: HL is Python 3 but can be trivially ported to Python 2 if needed
import hl
import os

# A few built-in entry points
# TODO: make all of it configurable by user

def main_list(args):
    hl.query(args, list_hosts)

def main_ssh(args):
    hl.query(args, run_ssh)


def list_hosts(hosts):
    for h in hosts:
        print(h.host)

def run_ssh(hosts):
    if len(hosts) != 1:
        print("Ambigious query, matches multiple hosts:")
        for h in hosts:
            print("   %s" % h.host)
    else:
        target = hosts[0]
        cmd = "ssh %s" % hosts[0].host
        print("SSH-ing to %s" % cmd)
        os.execv("/usr/bin/env", ["ssh", hosts[0].host])

# for quick tests
if __name__ == "__main__":
    import sys
    if sys.argv[1] == "query":
        main_list(sys.argv[2:])
    elif sys.argv[1] == "ssh":
        main_ssh(sys.argv[2:])
    else:
        print("Unrecognized service: %s" % sys.argv[1])
