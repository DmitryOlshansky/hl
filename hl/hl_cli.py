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

def main_list(args):
    hl.query(args[1:], print)

# for quick tests
if __name__ == "__main__":
    import sys
    if sys.argv[1] == "query":
        hl.query(sys.argv[2:], print)
