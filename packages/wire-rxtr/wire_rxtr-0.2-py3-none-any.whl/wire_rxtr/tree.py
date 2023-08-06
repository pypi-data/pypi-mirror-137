from wire_rxtr.node import RadixNode

class RadixTree(object):
    def __init__(self):
        self.root = RadixNode()

    def __repr__(self):
        return repr(self.root)

    def insert(self, key: str, handler, methods: list = [], dependencies: list = []):
        """Inserts a new route into the routing tree."""
        i, n, root = 0, len(key), self.root
        getPosition = lambda i: n if i == -1 else i

        while i < n:
            conflict, num = [], (key[i] == ':') + (root.indices == ':')

            if (root.indices == '*' or
                    key[i] == '*' and root.indices or
                    num == 1 or
                    num == 2 and key[i + 1:getPosition(
                        key.find('/', i))] != root.getChild(':').path):

                conflict = [key[:i] + p for p in self.traverse(root)]

            if conflict:
                raise Exception('"{}" conflicts with {}'.format(key, conflict))

            child = root.getChild(key[i])

            if child is None:
                pos = getPosition(key.find(':', i))
                if pos == n:
                    pos = getPosition(key.find('*', i))
                    if pos == n:
                        root.insertChild(
                            key[i], RadixNode(key[i:], handler, methods, dependencies))
                        return

                    root = root.insertChild(key[i], RadixNode(key[i:pos]))
                    root.insertChild(
                        '*', RadixNode(key[pos + 1:], handler, methods, dependencies))
                    return

                root = root.insertChild(key[i], RadixNode(key[i:pos]))
                i = getPosition(key.find('/', pos))
                root = root.insertChild(':', RadixNode(key[pos + 1:i]))

                if i == n:
                    root.addMethods(methods, handler, dependencies)
            else:
                root = child
                if key[i] == ':':
                    i += len(root.path) + 1
                    if i == n:
                        root.addMethods(methods, handler, dependencies)
                else:
                    j, m = 0, len(root.path)
                    while i < n and j < m and key[i] == root.path[j]:
                        i += 1
                        j += 1

                    if j < m:
                        child = RadixNode(root.path[j:])
                        child.methods = root.methods
                        child.children = root.children
                        child.indices = root.indices
                        child.size = root.size
                        child.dependencies = dependencies

                        root.path = root.path[:j]
                        root.methods = {}
                        root.children = [child]
                        root.indices = child.path[0]
                        root.size = 1
                        root.dependencies = {}

                    if i == n:
                        root.addMethods(methods, handler, dependencies)

    def get(self, key: str, method: str):
        i, n, root, params, deps = 0, len(key), self.root, {}, {}
        while i < n:
            if root.indices == ':':
                root, pos = root.children[0], key.find('/', i)
                if pos == -1:
                    pos = n
                params[root.path], i = key[i:pos], pos
            elif root.indices == '*':
                root = root.children[0]
                params[root.path] = key[i:]
                break
            else:
                root = root.getChild(key[i])
                if root is None:
                    return False, None, {}

                pos = i + len(root.path)
                if key[i:pos] != root.path:
                    return False, None, {}
                i = pos

        return True, root.methods.get(method.lower(), None), params, root.dependencies[method.lower()]

    def traverse(self, root):
        r = []
        for i, char in enumerate(root.indices):
            child = root.children[i]
            path = '{}{}'.format(
                char if char in [':', '*'] else '', child.path)

            if child.methods and child.indices:
                r.append([path])

            r.append([path + p for p in self.traverse(child) or ['']])
        return sum(r, [])