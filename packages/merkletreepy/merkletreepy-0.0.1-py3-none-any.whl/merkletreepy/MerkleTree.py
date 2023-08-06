from typing import List, Any, Callable, Dict, Optional


class MerkleTree:
    def __init__(self, leaves: List[Any], hash_function: Callable) -> None:
        self.hash_function = hash_function
        self.leaves = leaves
        self._process_leaves()

    @staticmethod
    def to_hex(value):
        return "0x" + value

    def _process_leaves(self) -> None:
        self.layers = [self.leaves]
        self._create_hashes(self.leaves)

    def _create_hashes(self, nodes: List[Any]) -> None:
        while len(nodes) > 1:
            n = len(nodes)
            layer_index = len(self.layers)
            self.layers.append([])
            for i in range(0, n, 2):
                if n == i + 1 and n % 2 == 1:
                    self.layers[layer_index].append(nodes[i])
                    continue
                left = nodes[i]
                right = left if i + 1 == n else nodes[i + 1]
                combined = self.to_hex(left + right)
                hash = self.hash_function(combined)
                self.layers[layer_index].append(hash)
            nodes = self.layers[layer_index]

    def get_root(self) -> List[Any]:
        try:
            return self.layers[-1][0]
        except IndexError:
            return []

    def get_proof(self, leaf: str, index: Optional[int] = None) -> List[Dict[str, Any]]:
        proof = []
        if not index:
            try:
                index = self.leaves.index(leaf)
            except ValueError:
                return []

        for layer in self.layers:
            is_right_node = index % 2
            pair_index = index - 1 if is_right_node else index + 1
            if pair_index < len(layer):
                proof.append(
                    {
                        "position": "left" if is_right_node else "right",
                        "data": layer[pair_index],
                    }
                )
            index = index // 2
        return proof

    def get_hex_proof(self, leaf: str, index: int) -> List[str]:
        return [self.to_hex(item) for item in self.get_proof(leaf, index)]

    def verify(self, proof: List[Dict[str, str]], target_node: str, root: str) -> bool:
        hash = target_node
        for node in proof:
            data = node["data"]
            is_left_node = node["position"] == "left"
            buffers = []
            buffers.append(hash)
            if is_left_node:
                buffers.insert(data, 0)
            else:
                buffers.append(data)
            combined = self.to_hex("".join(buffers))
            hash = self.hash_function(combined)
        return hash == root

    def get_depth(self) -> int:
        return len(self.layers) - 1

    def reset_tree(self) -> None:
        self.leaves = []
        self.layers = []
