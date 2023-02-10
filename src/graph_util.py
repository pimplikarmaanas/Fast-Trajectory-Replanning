class cell:
    def __init__(self):
        self.blocked = False

    def __str__(self):
        return str(self.blocked)

class graph:
    def __init__(self, len):
        self.graph = []
        for i in range(len):
            self.graph.append([])
            for j in range(len):
                self.graph[i].append(cell())
    
    def __str__(self):
        res = ""
        for i in range(len(self.graph)):
            for j in range(len(self.graph[i])):
                res += f"|{self.graph[i][j]}| "
            res += "\n"
        return res