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
try:
    from hl import hl
except:
    import hl

import os
import sys

# TODO: make all of it configurable by user
# query list built-in
def main_list():
    hl.query(sys.argv, list_hosts)

# ssh built-in
def main_ssh():
    hl.query(sys.argv, run_ssh)

# TODO: config all aspects of HL utility
# register/unregister new service command to hl as `hl-<service-name>`
# - enable/disable
# hl-config project name (enable|disable|default)
# 
# hl-config service add name @args 
# hl-config service rm name
# hl-config service list
#
def main_config():
    args = sys.argv
    print("Config section %s args: %s" % (args[0], args[1:]))

def list_hosts(hosts):
    for h in hosts:
        print(h.host)

def trace_hosts(hosts):
    for h in hosts:
        vec = " ".join([("%s:%s" % (k,v)) for k,v in h.hw_vec.items()])
        print("%-18s | %60s" % (h.host, vec))

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
    elif sys.argv[1] == "trace":
        hl.query(sys.argv, trace_hosts)
    elif sys.argv[1] == "ssh":
        sys.argv = sys.argv[1:]
        main_ssh()
    elif sys.argv[1] == "config":
        sys.argv = sys.argv[1:]
        main_config()
    else:
        # TODO: use argv[0] to determine the service to call
        print("Unrecognized service: %s" % sys.argv[1])
