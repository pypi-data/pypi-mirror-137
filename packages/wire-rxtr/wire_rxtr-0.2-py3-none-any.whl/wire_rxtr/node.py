import typing


class RadixNode(object):
    def __init__(self, path: str = None, handler=None, methods: dict = None, dependencies = []):
        self.path: str = path
        self.methods: dict = {}
        self.children: list = []
        self.dependencies: dict = {}
        self.indices = str()
        self.size: int = 0

        self.addMethods(methods, handler, dependencies)

    def __repr__(self):
        return ('<RadixTreeNode path: {}, methods: {}, indices: {}, children: '
                '{}, dependencies: {}>'.format(self.path, self.methods, self.indices,
                                               self.children, self.dependencies))

    def addMethods(self, methods: typing.Union[list, str, set, tuple], handler, dependencies: typing.Union[list, str, set, tuple]):
        if not methods:
            return

        if not isinstance(methods, (list, tuple, set)):
            methods = [methods]
        if not isinstance(dependencies, (list, tuple, set)):
            dependencies = [dependencies]

        for method in methods:
            if method in self.methods and self.methods[method] != handler:
                raise KeyError(
                    '{} conflicts with existed handler '
                    '{}'.format(handler, self.methods[method]))

            self.methods[method.lower()] = handler
            self.dependencies[method.lower()] = dependencies

    def bisect(self, target: int) -> int:
        low, high = 0, self.size
        while low < high:
            mid = low + high >> 1
            if self.indices[mid] < target:
                low = mid + 1
            else:
                high = mid
        return low

    def insertChild(self, index: int, child: "RadixNode"):
        pos = self.bisect(index)
        self.indices = self.indices[:pos] + index + self.indices[pos:]
        self.children.insert(pos, child)
        self.size += 1

        return child

    def getChild(self, index):
        for i, char in enumerate(self.indices):
            if char == index:
                return self.children[i]
