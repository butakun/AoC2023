class SearchVisualLogger:
    def __init__(self, f, grid):
        self.f = f
        self.grid = grid
    
    def dimensions(self, idim, jdim):
        print(f"0,DIMENSIONS,{idim},{jdim}", file=self.f)

    def inspecting(self, i, u):
        w = self.grid[u[0], u[1]]
        print(f"{i},INSPECT,{u[0]},{u[1]},{w}", file=self.f)

    def goal_reached(self, i, u, came_from, d):
        self.found_better(i, u, came_from, d)
        print(f"{i},GOAL,{u[0]},{u[1]},{d}", file=self.f)

    def found_better(self, i, u, came_from, d):
        v = u
        path = [v]
        while True:
            prev = came_from[v]
            if prev is None:
                break
            path.append(prev)
            v = prev
        path = [(u[0], u[1]) for u in path]  # it's reversed
        path_str = " ".join([f"{u[0]} {u[1]}" for u in path])
        print(f"{i},BETTER,{u[0]},{u[1]},{d},{path_str}", file=self.f)
