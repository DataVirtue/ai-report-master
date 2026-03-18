from typing import Dict, List


class RelationshipGraphBuilder:
    def build_graph(self, schema_data: List) -> Dict:
        relationship_graph = {}
        incoming_dict = {}
        allowed_table_set = set([entry["table_name"] for entry in schema_data])
        for table in schema_data:
            relationships = table["relationships"]
            current_table_name = table["table_name"]
            relationship_graph[current_table_name] = {"incoming": [], "outgoing": []}
            outgoing = set()
            for relation in relationships:
                related_table = relation["table_name"]
                if related_table not in allowed_table_set:
                    continue  # skip fk to tables filtered out
                outgoing.add(related_table)
                # while iterating also populate incoming_dict to avoid n2 search
                incoming_dict.setdefault(related_table, []).append(current_table_name)
            relationship_graph[current_table_name]["outgoing"] = list(outgoing)

        for table_name, incoming_list in incoming_dict.items():
            relationship_graph[table_name]["incoming"] = incoming_list

        return relationship_graph
