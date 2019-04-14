import os
import sys
import json
from hl import search

#TODO: write files in $TEMP, then atomically update

#skeleton for HL DB
def skeleton():
    return {
        'ssh.json' :
        """
            { 
                "single" : "ssh -p {{ssh_port}} {{host}} {{#cmd}}{{cmd}}{{/cmd}}",
                "defaults" : {
                    "ssh_port" : 22
                }
            }
        """,
        'http.json' :
        """
            { 
                "single" : "curl {{host}}:{{http_port}}/{{path}}",
                "defaults" : {
                    "http_port" : 22
                }
            }
        """
    }

def init(home):
    base = os.path.join(home, '.config', 'hl')
    if not os.path.exists(base):
        os.mkdir(base)
    return Db(base)

class Db(object):

    def __init__(self, basedir):
        self.basedir = basedir
        self.appsdir = os.path.join(basedir, 'apps')
        self.hosts_path = os.path.join(basedir, 'hosts.json')
        if not os.path.exists(self.appsdir):
            os.mkdir(self.appsdir)
            self.apps = skeleton()
            for name, js in skeleton().items():
                with open(os.path.join(self.appsdir, name), "w") as f:
                    f.write(js)
            #TODO: git init
        else:
            self.apps = {}
            for _, _, name in os.walk(self.appsdir):
                if name[-5:] == '.json':
                    cmd = name[-5:]
                    with open(os.path.join(self.appsdir, name)) as f:
                        self.apps[cmd] = json.loads(f.read())
        self.hosts = []
        try:
            with open(self.hosts_path) as f:
                for line in f.readlines():
                    #TODO: validate JSON structure!
                    self.hosts.append(json.loads(line))
        except OSError:
            print("No hosts found at {}, creating new DB.", self.hosts_path, file=sys.stderr)
            pass

    def save(self):
        # SAVE hosts
        with open(self.hosts_path, 'w') as f:
            for h in self.hosts:
                f.write(json.dumps(h)+"\n")
        # TODO: git commit

    """
        Adds or replace one properly structured host entry
    """
    def add_host(self, host):
        for i in range(len(self.hosts)):
            if self.hosts[i] == host:
                self.hosts[i] = host
                return
        self.hosts.append(host)
    
    # TODO:
    def remove_by_query(self, query):
        pass
    
    """
        Returns indices of best matching host entries
    """
    def select(self, query):
        qt = search.terms(query)
        hts = [search.terms(h['host']) for h in self.hosts]
        scores = [search.score(qt, ht) for ht in hts]

