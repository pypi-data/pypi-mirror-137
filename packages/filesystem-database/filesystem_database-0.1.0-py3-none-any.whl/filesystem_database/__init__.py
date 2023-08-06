import pathlib, shutil, shlex

# Requires an empty directory or pre-existing database directory for the path
class dbNode():
    hexLen = 4   # Length of key hex strings in bytes (two hex chars per byte)

    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.keys = []
        self.keynames = {}
        self.nodes = []
        self.nodeNames = {}

        self.loadKeys()
        self.loadNodes()

    def getHex(self, int):
        return hex(int)[2:].zfill(self.hexLen * 2)

    def getInt(self, hex):
        return int('0x' + hex.lower(), base=16)

    def getKeyID(self, identifier):
        if isinstance(identifier, int):
            return identifier if identifier in self.keys else None
        elif isinstance(identifier, str):
            return self.keyNames[identifier] if identifier in self.keyNames.keys() else None
        else:
            raise Exception('Not a valid identifier')

    def getKeyName(self, identifier):
        if isinstance(identifier, str):
            return identifier if identifier in self.keyNames.keys() else None
        elif isinstance(identifier, int):
            return self.keyNames.keys[self.keyNames.values().index(identifier)] if identifier in self.keyNames.values() else None
        else:
            raise Exception('Not a valid identifier')

    def loadKeys(self):
        self.keys = []
        self.keyNames = {}

        files = [object for object in self.path.glob('key*') if object.is_file()]
        for file in files:
            self.keys.append(int('0x' + file.name[3:].lower(), base=16))

        try:
            with open(self.path.joinpath('keyNames'), 'r') as nameFile:
                for entry in nameFile.read().split('\n'):
                    name, idHex = entry.split(':')
                    idInt = self.getInt(idHex)
                    if idInt in self.keys:
                        self.keyNames[name] = idInt

        except FileNotFoundError:
            nameFile = open(self.path.joinpath('keyNames'), 'w')
            nameFile.close()

    def mkKey(self, id, name=None):
        if not self.getKeyID(id) is None:
            raise Exception('key {} exists'.format(id))
        elif not self.getKeyID(name) is None:
            raise Exception('key {} exists'.format(name))
        else:
            self.keys.append(id)
            self.path.joinpath('key' + self.getHex(id)).touch()
            if not name is None:
                self.keyNames[name] = id

    def rmKey(self, identifier):
        id = self.getKeyID(identifier)
        if id is None:
            raise Exception('Key {} does not exist'.format(repr(identifier)))
        else:
            idHex = self.getHex(id)
            self.keys.remove(id)
            self.path.joinpath('key' + idHex).unlink()

    def get(self, identifier):
        id = self.getKeyID(identifier)
        if id is None:
            raise Exception('Key {} does not exist'.format(repr(identifier)))
        idHex = self.getHex(id)
        with open(self.path.joinpath('key' + idHex), 'rb') as file:
            return file.read()

    def set(self, identifier, value):
        id = self.getKeyID(identifier)
        if id is None:
            raise Exception('Key {} does not exist'.format(repr(identifier)))
        idHex = self.getHex(id)
        with open(self.path.joinpath('key' + idHex), 'wb') as file:
            file.write(value)


    def getNodeID(self, identifier):
        if isinstance(identifier, int):
            return identifier if identifier in self.nodes else None
        elif isinstance(identifier, str):
            return self.nodeNames[identifier] if identifier in self.nodeNames.keys() else None
        else:
            raise Exception('Not a valid identifier')

    def getNodeName(self, identifier):
        if isinstance(identifier, str):
            return identifier if identifier in self.nodeNames.keys() else None
        elif isinstance(identifier, int):
            return self.nodeNames.keys[self.nodeNames.values().index(identifier)] if identifier in self.nodeNames.values() else None
        else:
            raise Exception('Not a valid identifier')

    def loadNodes(self):
        self.nodes = []
        self.nodeNames = {}

        folders = [object for object in self.path.glob('node*') if object.is_dir()]
        for folder in folders:
            self.nodes.append(int('0x' + folder.name[4:].lower(), base=16))

        try:
            with open(self.path.joinpath('nodeNames'), 'r') as nameFile:
                for entry in nameFile.read().split('\n'):
                    name, idHex = entry.split(':')
                    idInt = self.getInt(idHex)
                    if idInt in self.nodes:
                        self.nodeNames[name] = idInt

        except FileNotFoundError:
            nameFile = open(self.path.joinpath('nodeNames'), 'w')
            nameFile.close()

    def mkNode(self, id, name=None):
        if not self.getNodeID(id) is None:
            raise Exception('node {} exists'.format(id))
        elif not self.getNodeID(name) is None:
            raise Exception('node {} exists'.format(name))
        else:
            nodeHex = self.getHex(id)
            self.nodes.append(id)
            self.path.joinpath('node' + nodeHex).mkdir()
            if not name is None:
                self.nodeNames[name] = id

    def rmNode(self, identifier):
        id = self.getNodeID(identifier)
        if id is None:
            raise Exception('Key {} does not exist'.format(repr(identifier)))
        else:
            nodeHex = self.getHex(identifier)
            self.nodes.remove(identifier)
            shutil.rmtree(str(self.path.joinpath('node' + nodeHex)))

    def node(self, identifier):
        id = self.getNodeID(identifier)
        idHex = self.getHex(identifier)
        if id is None:
            raise Exception('Node {} does not exist'.format(repr(identifier)))
        else:
            return dbNode(self.path.joinpath('node' + idHex))


    def search(self, value):
        matchingKeys = []
        for key in self.keys:
            if self.get(key) == value:
                matchingKeys.append(key)
        return matchingKeys

def cli():
    nodes = [(None, '(no node)')]
    dbLoaded = False
    runFlag = True

    def getIdentifier(string):
        try:
            return int(string)
        except:
            return str(string)

    def command_load(path):
        global dbLoaded, nodes
        if dbLoaded:
            raise Exception('Already have a database loaded')
        nodes = [(dbNode(path), 'dbRoot')]
        dbLoaded = True

    def command_unload():
        global dbLoaded, nodes
        if not dbLoaded:
            raise Exception('No database loaded')
        nodes = [(None, '(no node)')]
        dbLoaded = False
    
    def command_keys():
        if not dbLoaded:
            raise Exception('No database loaded')
        print(nodes[-1][0].keys)
    
    def command_nodes():
        if not dbLoaded:
            raise Exception('No database loaded')
        print(nodes[-1][0].nodes)
    
    def command_mkKey(id):
        if not dbLoaded:
            raise Exception('No database loaded')
        print(nodes[-1][0].mkKey(getIdentifier(id)))
    
    def command_mkNode(id):
        if not dbLoaded:
            raise Exception('No database loaded')
        print(nodes[-1][0].mkNode(getIdentifier(id)))
    
    def command_rmKey(id):
        if not dbLoaded:
            raise Exception('No database loaded')
        print(nodes[-1][0].rmKey(getIdentifier(id)))
    
    def command_rmNode(id):
        if not dbLoaded:
            raise Exception('No database loaded')
        print(nodes[-1][0].rmNode(getIdentifier(id)))

    def command_get(id):
        if not dbLoaded:
            raise Exception('No database loaded')
        print(nodes[-1][0].get(getIdentifier(id)))

    def command_set(id, value):
        if not dbLoaded:
            raise Exception('No database loaded')
        nodes[-1][0].set(getIdentifier(id), value.encode())

    def command_node(id, name):
        if not dbLoaded:
            raise Exception('No database loaded')
        nodes.append((nodes[-1][0].node(getIdentifier(id)), name))

    def command_dropNode():
        if not dbLoaded:
            raise Exception('No database loaded')
        if len(nodes) <= 1:
            raise Exception('Can\'t drop root node')
        del(nodes[-1])

    def command_quit():
        global runFlag
        runFlag = False

    commands = {
        'load': command_load,
        'unload': command_unload,
        'mk-key': command_mkKey,
        'rm-key': command_rmKey,
        'keys': command_keys,
        'get': command_get,
        'set': command_set,
        'mk-node': command_mkNode,
        'rm-node': command_rmNode,
        'nodes': command_nodes,
        'node': command_node,
        'drop-node': command_dropNode,
        'quit': command_quit
    }

    while runFlag:
        command, *args = shlex.split(input('{}:> '.format(nodes[-1][1])))
        try:
            function = commands[command]
        except KeyError:
            print('No command "{}"'.format(command))
            continue
        try:
            function(*args)
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))

if __name__ == '__main__':
    cli()
