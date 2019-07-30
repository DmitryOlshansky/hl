import os
import sys
import json
from hl import search
from hl import hlist
from hl import repo

#TODO: write files in $TEMP, then atomically update
#TODO: checkpoint every .save() as git commit

#skeleton for HL DB
def skeleton():
    return {
        'ssh.json' :
        """
            { 
                "single" : "ssh -p {{{ssh_port}}} {{{host}}} {{#cmd}}{{{cmd}}}{{/cmd}}",
                "defaults" : {
                    "ssh_port" : 22
                }
            }
        """,
        'http.json' :
        """
            { 
                "single" : "curl {{{proto}}}://{{{host}}}:{{{http_port}}}/{{{path}}}",
                "defaults" : {
                    "proto" : "http",
                    "http_port" : 8080
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
        self.repo = repo.Repo(basedir)
        self.basedir = basedir
        self.appsdir = os.path.join(basedir, 'apps')
        self.hosts_path = os.path.join(basedir, 'hosts.json')
        if not os.path.exists(self.appsdir):
            os.mkdir(self.appsdir)
            self.apps = skeleton()
            for name, js in skeleton().items():
                with open(os.path.join(self.appsdir, name), "w") as f:
                    f.write(js)
            repo.init()
        else:
            self.apps = {}
            for _, _, names in os.walk(self.appsdir):
                for name in names:
                    if name[-5:] == '.json':
                        cmd = name[:-5]
                        with open(os.path.join(self.appsdir, name)) as f:
                            self.apps[cmd] = json.loads(f.read())
        try:
            with open(self.hosts_path) as f:
                self.hosts = hlist.HList(f.read())
        except OSError:
            print("No hosts found at {}, creating new DB.", self.hosts_path, file=sys.stderr)
            self.hosts = hlist.HList()

    def save_hosts(self):
        with open(self.hosts_path, 'w') as f:
            f.write(str(self.hosts))
        self.repo.commit()

    def app(self, name):
        return self.apps[name]

    """
        Add json with template from path
    """
    def add_app(self, path):

        # TODO: git commit
        pass

    def rm_app(self, name):
        # TODO: git commit
        pass
