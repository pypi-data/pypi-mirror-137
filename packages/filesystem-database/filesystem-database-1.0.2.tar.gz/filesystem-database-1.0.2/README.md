# filesystem-database
This database is easy to set up: Just make an empty folder and initialize a `dbNode` object in it! The database structure consists of `dbNode` objects. `dbNode`s contain more `dbNode`s and keys, which store a byte value.

# Usage
To initalize a database:
```python
import filesystem_database as fs_db

rootNode = fs_db.dbNode('/path/to/database/directory')
```
The directory passed to `dbNode()` must either be empty or contain *only* data from a `dbNode`.

To use keys:
```python
rootNode.mkKey(0, 'exampleKey')     # Create a key with ID 0 and name `exampleKey`
rootNode.set(0, b'test data :D')    # Set a value to key 0
rootNode.get(0)     # Get the value of key 0 (returns `b'test data :D'` in this case)
rootNode.keys       # A list containing key IDs
rootNode.keyNames   # A dictionary containing key names and the key IDs they correspond to
```
Here `0` is the ID to give the key and `'exampleNode'` is the optional name to assign to the key. Neither the ID nor the name may be used for multiple keys. `get` and `set` will accept either an integer for a key ID or a string for a key name.

To use nodes:
```python
subNode = rootNode.mkNode(0, 'exampleNode') # Create a node (ID 0, name 'exampleNode') under `rootNode`
rootNode.node(0)    # Get node 0 from `rootNode`
rootNode.nodes      # A list containing node IDs
rootNode.nodeNames  # A dictionary containing node names and the node IDs they correspond to

```
`subNode` is a `dbNode` object whose contents are within `rootNode`. Here `0` is the ID to give the node (must not be taken) and `'exampleNode'` is the optional name to assign to the node. Neither the ID nor the name may be used for multiple nodes. `get` and `set` will accept either an integer for a key ID or a string for a key name.

# Command Line Utility
There is an included command line utility for easier management of databases. To run it, enter the following in a Python terminal:
```python
>>> from filesystem_database import cli
>>> cli()
```

### Commands
1. `load`
2. `unload`
3. `mk-key`
4. `rm-key`
5. `keys`
6. `get`
7. `set`
8. `mk-node`
9. `rm-node`
10. `nodes`
11. `node`
12. `drop-node`
13. `quit`

Most of these are identical to the methods of a `dbNode`, except for a few. `load` and `unload` will load a `dbNode` from the supplied path. `node` 'enters' a node within the current node, setting it in the promp string. `drop-node` drops the current node and moves to its parent node. `quit` exits the CLI interface.
