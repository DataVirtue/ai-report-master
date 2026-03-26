import json


class SQLAgent:
    def __init__(self, report_engine):
        self.report_engine = report_engine

    def get_tools(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_schema_context",
                    "description": "Search and return relevant database schema information based on a query",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "search_query": {
                                "type": "string",
                                "description": "Search query to find relevant tables and columns",
                            },
                            "top_k": {
                                "type": "integer",
                                "description": "Number of results to return",
                                "default": 10,
                            },
                        },
                        "required": ["search_query"],
                    },
                },
            },
        ]

    def handle_tool_call(self, tool_call):
        name = tool_call["function"]["name"]
        args = json.loads(tool_call["function"]["arguments"])

        if name == "get_schema_context":
            return self.report_engine.get_schema_context(**args)
