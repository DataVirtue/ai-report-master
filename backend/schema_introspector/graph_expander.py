class GraphExpander:
    def __init__(self, relationship_graph) -> None:
        self.relationship_graph = relationship_graph

    def expand_graph(self, retrieved_tables, depth=1):
        expanded = set()
        queue = [table["table_name"] for table in retrieved_tables]
        expanded.update(queue)

        for _ in range(depth):
            next_queue = []
            for table in queue:
                if table not in self.relationship_graph:
                    continue
                neighbors = (
                    self.relationship_graph[table]["incoming"]
                    + self.relationship_graph[table]["outgoing"]
                )
                for neighbor in neighbors:
                    if neighbor not in expanded:
                        expanded.add(neighbor)
                        next_queue.append(neighbor)

            queue = next_queue

        return list(expanded)
