import hashlib

class Node:
    def __init__(self, node_id, m):
        self.node_id = node_id
        self.m = m
        self.successor = self
        self.predecessor = None
        self.finger_table = [None] * m

    def find_successor(self, key):
        if self.node_id < key <= self.successor.node_id:
            return self.successor
        elif self.node_id > self.successor.node_id and (key > self.node_id or key <= self.successor.node_id):
            return self.successor
        else:
            return self.successor.find_successor(key)

    def join(self, existing_node):
        if existing_node:
            self.successor = existing_node.find_successor(self.node_id)
            self.predecessor = self.successor.predecessor
            self.successor.predecessor = self
            if self.predecessor:
                self.predecessor.successor = self

    def update_finger_table(self, nodes):
        for i in range(self.m):
            start = (self.node_id + 2**i) % (2**self.m)
            self.finger_table[i] = self.find_successor(start)

    def __repr__(self):
        return f"Node({self.node_id})"


def hash_function(value, m):
    return int(hashlib.sha1(value.encode()).hexdigest(), 16) % (2**m)


def test_chord():
    # Test case configuration
    m = 6  # 2^6 = 64 possible IDs
    nodes = []

    # Create nodes
    for name in ["NodeA", "NodeB", "NodeC", "NodeD"]:
        node_id = hash_function(name, m)
        new_node = Node(node_id, m)
        if nodes:
            new_node.join(nodes[0])
        nodes.append(new_node)

    # Sort nodes by ID
    nodes.sort(key=lambda x: x.node_id)
    for i, node in enumerate(nodes):
        node.successor = nodes[(i + 1) % len(nodes)]
        node.predecessor = nodes[i - 1]

    # Update finger tables
    for node in nodes:
        node.update_finger_table(nodes)

    # Print network structure
    print("Network structure:")
    for node in nodes:
        print(f"Node {node.node_id} -> Successor: {node.successor.node_id}, Predecessor: {node.predecessor.node_id}")

    # Key lookup test
    print("\nKey lookup results:")
    keys = [10, 24, 30, 54]
    for key in keys:
        result = nodes[0].find_successor(key)
        print(f"Key {key} is managed by Node {result.node_id}")

    # Assertions for correctness
    assert nodes[0].find_successor(10).node_id == nodes[1].node_id, "Test failed for key 10"
    assert nodes[0].find_successor(24).node_id == nodes[2].node_id, "Test failed for key 24"
    assert nodes[0].find_successor(30).node_id == nodes[2].node_id, "Test failed for key 30"
    assert nodes[0].find_successor(54).node_id == nodes[3].node_id, "Test failed for key 54"
    print("\nAll test cases passed!")

if __name__ == "__main__":
    test_chord()
