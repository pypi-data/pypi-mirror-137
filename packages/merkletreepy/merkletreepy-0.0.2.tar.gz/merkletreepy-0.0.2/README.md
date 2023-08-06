# merkletreepy

Python port of merkletreejs. Currently unstable.

## Installation

```
pip install merkletreepy
```

## Usage

```py
from merkletreepy import MerkleTree
import Web3

def hash_function(x):
    return Web3.keccak(text=x).hex()

leaves = [hash_function(leaf) for leaf in "abc"]
tree = MerkleTree(leaves, sha256)
root = tree.get_root()
leaf = sha256("a")
bad_leaf = sha256("x")
proof = tree.get_proof(leaf)
tree.verify(proof, leaf, root)      # returns True
tree.verify(proof, bad_leaf, root)  # returns False
```
