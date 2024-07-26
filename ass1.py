from collections import defaultdict, deque

class TaskScheduler:
    def __init__(self, tasks, dependencies):
        self.tasks = tasks
        self.dependencies = dependencies
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
        self.build_graph()

    def build_graph(self):
        for task in self.tasks:
            self.in_degree[task] = 0
        
        for u, v in self.dependencies:
            self.graph[u].append(v)
            self.in_degree[v] += 1

    def topological_sort(self):
        zero_in_degree = deque([task for task in self.tasks if self.in_degree[task] == 0])
        topo_order = []
        
        while zero_in_degree:
            node = zero_in_degree.popleft()
            topo_order.append(node)
            for neighbor in self.graph[node]:
                self.in_degree[neighbor] -= 1
                if self.in_degree[neighbor] == 0:
                    zero_in_degree.append(neighbor)
        
        if len(topo_order) == len(self.tasks):
            return topo_order
        else:
            raise ValueError("Graph has a cycle, topological sort not possible.")

    def calculate_earliest_times(self):
        EST = {task: 0 for task in self.tasks}
        EFT = {task: 0 for task in self.tasks}
        
        topo_order = self.topological_sort()
        
        for task in topo_order:
            EFT[task] = EST[task] + self.tasks[task]
            for neighbor in self.graph[task]:
                EST[neighbor] = max(EST[neighbor], EFT[task])
        
        return EST, EFT

    def calculate_latest_times(self, max_eft):
        LFT = {task: float('inf') for task in self.tasks}
        LST = {task: float('inf') for task in self.tasks}
        
        topo_order = self.topological_sort()[::-1]
        
        for task in topo_order:
            if not self.graph[task]:
                LFT[task] = max_eft
                LST[task] = max_eft - self.tasks[task]
            for neighbor in self.graph[task]:
                LFT[task] = min(LFT[task], LST[neighbor])
                LST[task] = LFT[task] - self.tasks[task]
        
        return LFT, LST

    def get_project_completion_times(self):
        EST, EFT = self.calculate_earliest_times()
        max_eft = max(EFT.values())
        LFT, LST = self.calculate_latest_times(max_eft)
        
        return max_eft, max(LFT.values())

if __name__ == "__main__":
    tasks = {
        'T_START': 0,
        'T1': 3,
        'T2': 2,
        'T3': 1,
        'T4': 4,
        'T5': 2
    }
    dependencies = [
        ('T_START', 'T1'),
        ('T_START', 'T2'),
        ('T1', 'T3'),
        ('T2', 'T3'),
        ('T3', 'T4'),
        ('T3', 'T5')
    ]
    
    scheduler = TaskScheduler(tasks, dependencies)
    earliest_completion, latest_completion = scheduler.get_project_completion_times()
    
    print(f"Earliest time all the tasks will be completed: {earliest_completion}")
    print(f"Latest time all the tasks will be completed: {latest_completion}")
