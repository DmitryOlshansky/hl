import os

class Db(object):

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

def init():
    dotconf = os.path.join(home, '.config')
    if not os.path.exists(dotconf):
        os.mkdir(dotcoonf)
    base = os.path.join(dotconf, 'hl')
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
                with open(name, "w") as f:
                    f.write(js)
        else:
            self.apps = {}
            for _, _, name in os.walk(self.appsdir):
                if name[-5:] == '.json':
                    cmd = name[-5:]
                    self.apps[cmd] = json.loads(os.path.join(self.appsdir, name))
        self.hosts = []
        try:
            with open('hosts.json') as f:
                for line in f.readlines():
                    #TODO: validate JSON structure!
                    hosts.append(json.loads(line))
        except OSError:
            pass

    
    def inverted_index(self):
        if (hasattr(self, 'index')):
            return self.index
        else:
            self.index = search.compute_index(hosts)
            return self.index

    # TODO:
    def add_hosts(self, hosts):
        pass
    
    # TODO:
    def remove_by_query(self, query):
        pass
    
    def select(self, query):
        qt = search.terms(query)
        return self.inverted_index()(qt)
