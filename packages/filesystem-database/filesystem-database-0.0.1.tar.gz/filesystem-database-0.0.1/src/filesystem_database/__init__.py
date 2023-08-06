from argparse import ArgumentError
import pathlib, shutil

# Requires an empty directory or pre-existing database directory for the path
class dbNode():
    hexLen = 4   # Length of key hex strings in bytes (two hex chars per byte)
    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.keys = []
        self.nodes = []

        self.loadKeys()
        self.loadNodes()

    def getHex(self, int):
        return hex(int)[2:].zfill(self.hexLen * 2)


    def loadKeys(self):
        self.keys = []
        files = [object for object in self.path.glob('key*') if object.is_file()]
        for file in files:
            self.keys.append(int('0x' + file.name[3:].lower(), base=16))

    def mkKey(self, key):
        if not key in self.keys:
            keyHex = self.getHex(key)
            self.keys.append(key)
            self.path.joinpath('key' + keyHex).touch()
        else:
            raise Exception('key {} exists'.format(key))

    def rmKey(self, key):
        if key in self.keys:
            keyHex = self.getHex(key)
            self.keys.remove(key)
            self.path.joinpath('key' + keyHex).unlink()
        else:
            raise Exception('key {} does not exist'.format(key))


    def loadNodes(self):
        self.nodes = []
        folders = [object for object in self.path.glob('node*') if object.is_dir()]
        for folder in folders:
            self.nodes.append(int('0x' + folder.name[4:].lower(), base=16))

    def mkNode(self, node):
        if not node in self.nodes:
            nodeHex = self.getHex(node)
            self.nodes.append(node)
            self.path.joinpath('node' + nodeHex).mkdir()
        else:
            raise Exception('node {} exists'.format(node))

    def rmNode(self, node):
        if node in self.nodes:
            nodeHex = self.getHex(node)
            self.nodes.remove(node)
            shutil.rmtree(str(self.path.joinpath('node' + nodeHex)))
        else:
            raise Exception('node {} does not exist'.format(node))


    def get(self, key):
        keyHex = self.getHex(key)
        if key in self.keys:    
            with open(self.path.joinpath('key' + keyHex), 'rb') as file:
                return file.read()
        else:
            raise KeyError('bad key {}'.format(key))

    def set(self, key, value):
        keyHex = self.getHex(key)
        if key in self.keys:    
            with open(self.path.joinpath('key' + keyHex), 'wb') as file:
                file.write(value)
        else:
            raise KeyError('bad key {}'.format(key))

    def node(self, node):
        nodeHex = self.getHex(node)
        if node in self.nodes:
            return dbNode(self.path.joinpath('node' + nodeHex))
        else:
            raise KeyError('bad node {}'.format(node))


    def search(self, value):
        matchingKeys = []
        for key in self.keys:
            if self.get(key) == value:
                matchingKeys.append(key)
        return matchingKeys

if __name__ == '__main__':
    from argparse import ArgumentParser

    nodes = [(None, '(no node)')]
    dbLoaded = False
    runFlag = True

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
        print(nodes[-1][0].mkKey(int(id)))
    
    def command_mkNode(id):
        if not dbLoaded:
            raise Exception('No database loaded')
        print(nodes[-1][0].mkNode(int(id)))
    
    def command_rmKey(id):
        if not dbLoaded:
            raise Exception('No database loaded')
        print(nodes[-1][0].rmKey(int(id)))
    
    def command_rmNode(id):
        if not dbLoaded:
            raise Exception('No database loaded')
        print(nodes[-1][0].rmNode(int(id)))

    def command_get(id):
        if not dbLoaded:
            raise Exception('No database loaded')
        print(nodes[-1][0].get(int(id)))

    def command_set(id, value):
        if not dbLoaded:
            raise Exception('No database loaded')
        nodes[-1][0].set(int(id), value.encode())

    def command_node(id, name):
        if not dbLoaded:
            raise Exception('No database loaded')
        nodes.append((nodes[-1][0].node(int(id)), name))

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
        'keys': command_keys,
        'nodes': command_nodes,
        'mk-key': command_mkKey,
        'mk-node': command_mkNode,
        'rm-key': command_rmKey,
        'rm-node': command_rmNode,
        'get': command_get,
        'set': command_set,
        'node': command_node,
        'drop-node': command_dropNode,
        'quit': command_quit
    }

    while runFlag:
        command, *args = input('{}:> '.format(nodes[-1][1])).split()
        try:
            function = commands[command]
        except KeyError:
            print('No command "{}"'.format(command))
            continue
        try:
            function(*args)
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
