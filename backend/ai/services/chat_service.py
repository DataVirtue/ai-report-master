from ai.handlers import OpenRouterHandler
from .report_generation_service import ReportGenerationService
from ai.agents import SQLAgent
import json
from decimal import Decimal
import datetime


class ChatService:
    # system_prompt = """
    # You are an AI reporting assistant that helps users generate reports from a database.
    #
    # The user is non-technical. Always keep explanations simple and clear.
    #
    # You have access to the following tools:
    # 1. get_schema_context → to discover relevant tables and columns
    # 2. run_sql → to execute SQL queries and retrieve data
    #
    # WORKFLOW:
    # 1. Understand the user request
    # 2. If requirements are unclear → ask clarifying questions
    # 3. Use get_schema_context to find relevant tables
    # 4. Generate a correct SQL query
    # 5. Call run_sql to execute the query
    # 6. Once results are available:
    # - Summarize insights clearly
    # - Do NOT include raw data in your response
    # - Focus on key findings
    #
    # IMPORTANT RULES:
    # - NEVER assume table or column names → always use get_schema_context first
    # - ALWAYS use tools for database-related questions
    # - NEVER generate fake data
    # - Keep SQL efficient (use LIMIT if needed)
    # - If SQL fails, fix and retry
    #
    # RESPONSE STYLE:
    # - Clear, concise, non-technical
    # - Explain what the data means, not how SQL works
    # """
    system_prompt = """
    You are an AI reporting assistant that helps users generate reports from a database.

    The user is non-technical. Always keep explanations simple and clear.

    You have access to the following tools:
    1. get_schema_context → to discover relevant tables and columns
    2. run_sql → to execute SQL queries and retrieve data

    IMPORTANT CONTEXT:
    - After executing SQL, you will NOT have access to the actual row data.
    - You will ONLY receive metadata such as row_count (number of rows returned).
    - You MUST NOT assume, infer, or invent any values, names, trends, or insights from the data.

    WORKFLOW:
    1. Understand the user request
    2. If requirements are unclear → ask clarifying questions
    3. Use get_schema_context to find relevant tables
    4. Generate a correct SQL query
    5. Call run_sql to execute the query
    6. Once results are available:
    - If only row_count is available:
        • Inform the user how many records were found
        • DO NOT attempt to summarize or infer insights
        • Offer to refine the query (e.g., aggregation, filters)
    - Only provide insights if actual summarized/aggregated data is explicitly available

    STRICT RULES:
    - NEVER generate fake data, names, or statistics
    - NEVER assume what the data contains
    - NEVER describe trends, rankings, or comparisons without actual data
    - If data is not available, clearly say:
    "I don’t have access to the actual data to provide insights."

    SQL RULES:
    - NEVER assume table or column names → always use get_schema_context first
    - ALWAYS use tools for database-related questions
    - Keep SQL efficient (use LIMIT if needed)
    - Prefer aggregation (SUM, COUNT, GROUP BY) when user asks for insights
    - If SQL fails, fix and retry

    RESPONSE STYLE:
    - Clear, concise, non-technical
    - Be honest about limitations
    - Offer helpful next steps (e.g., “Would you like a summary by distributor?”)
    """

    def __init__(
        self, handler=OpenRouterHandler, model="openrouter/hunter-alpha"
    ) -> None:
        self.handler = handler()
        self.model = model
        self.report_service = ReportGenerationService()
        self.sql_agent = SQLAgent(self.report_service.report_engine)
        self.tools = self.sql_agent.get_tools()

    def custom_json_serializer(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    def clean_llm_json(self, text: str) -> str:
        text = text.strip()

        if text.startswith("```"):
            lines = text.split("\n")

            # remove first line ```json
            if lines[0].startswith("```"):
                lines = lines[1:]

            # remove last ```
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]

            text = "\n".join(lines)

        return text.strip()

    def _event(self, type_, data):
        return f"data: {json.dumps({'type': type_, 'data': data}, default=self.custom_json_serializer)}\n\n"

    def stream_messages(self, messages):
        messages.append({"role": "system", "content": self.system_prompt})

        yield self._event("status", "Understanding request...")

        # First LLM call
        response = self.handler.get_response_with_message_list(
            messages, self.model, tools=self.tools
        )
        messages.append(
            {
                "role": "assistant",
                "content": response.get("content"),
                "tool_calls": response.get("tool_calls", []),
            }
        )
        yield self._event("status", "Analyzing...")
        sql_success = False
        current_row_count = 0
        while True:
            # 🔹 TOOL CALL HANDLING
            #

            tool_calls = response.get("tool_calls") or []
            if not tool_calls:
                content = response.get("content")
                if content:
                    yield self._event("message", content)
                return

            if tool_calls:
                yield self._event("status", "Fetching schema...")

                for call in tool_calls:
                    tool_name = call["function"]["name"]
                    tool_result = self.sql_agent.handle_tool_call(call)
                    if tool_name == "run_sql":
                        if isinstance(tool_result, dict) and tool_result.get("error"):
                            yield self._event(
                                "data",
                                {
                                    "rows": [],
                                    "error": tool_result["error"],
                                },
                            )
                        elif isinstance(tool_result, dict):
                            sql_success = True
                            yield self._event(
                                "data",
                                {
                                    "rows": tool_result.get("data"),
                                    "error": None,
                                },
                            )
                        if isinstance(tool_result, dict):
                            data = tool_result.get("data") or []
                            row_count = len(data)
                            current_row_count = row_count
                        elif isinstance(tool_result, list):
                            row_count = len(tool_result)
                            current_row_count = row_count
                        else:
                            row_count = 0

                        messages.append(
                            {
                                "role": "tool",
                                "name": tool_name,
                                "tool_call_id": call["id"],
                                "content": json.dumps(
                                    {
                                        "status": "success",
                                        "row_count": current_row_count,
                                    }
                                ),
                            }
                        )
                    else:
                        messages.append(
                            {
                                "role": "tool",
                                "name": call["function"]["name"],
                                "tool_call_id": call["id"],
                                "content": json.dumps(tool_result),
                            }
                        )
                yield self._event("status", "Fetching data...")
                print(messages)

                # Call LLM again with tool results
                response = self.handler.get_response_with_message_list(
                    messages, self.model, tools=self.tools if not sql_success else []
                )
                messages.append(
                    {
                        "role": "assistant",
                        "content": response.get("content"),
                        "tool_calls": response.get("tool_calls", []),
                    }
                )

                if sql_success:
                    # Force final summarization call WITHOUT tools
                    yield self._event("status", "Summarising response...")

                    messages.append(
                        {
                            "role": "system",
                            "content": "The SQL query has already been executed successfully. Do not call any tools. Provide a clear summary of the results.",
                        }
                    )
                    final_response = self.handler.get_response_with_message_list(
                        messages,
                        self.model,
                        tools=[],  # IMPORTANT: disable tools
                    )

                    content = final_response.get("content")

                    if content:
                        yield self._event("message", content)

                    break
