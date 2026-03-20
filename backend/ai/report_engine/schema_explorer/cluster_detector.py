from typing import Dict
from collections import deque


class ClusterDetector:
    def get_clusters(self, relationship_graph: Dict):
        cluster_list = []
        visited = set()
        queue = deque()
        for table in relationship_graph.keys():
            cluster = []
            if table in visited:
                continue
            queue.append(table)
            while len(queue) > 0:
                current_table = queue.popleft()
                if current_table in visited:
                    continue
                cluster.append(current_table)
                visited.add(current_table)
                next_incoming = relationship_graph[current_table]["incoming"]
                next_outgoing = relationship_graph[current_table]["outgoing"]
                queue.extend(next_incoming)
                queue.extend(next_outgoing)

            cluster_list.append(cluster)

        return cluster_list
