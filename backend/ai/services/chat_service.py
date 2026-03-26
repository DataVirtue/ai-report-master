from ai.handlers import OpenRouterHandler
from .report_generation_service import ReportGenerationService
from ai.agents import SQLAgent
import json
import logging


class ChatService:
    system_prompt = """
        You are a report assitant 
        when the user asks to generate report clarify the requirement as necessary 
        and when you are ready generate a 
        proper prompt for an ai sql engine to generate the relevant report output format:
        Assume the user is not technical and relevant schema details will be provided to the sql engine

    """

    def __init__(
        self, handler=OpenRouterHandler, model="openrouter/hunter-alpha"
    ) -> None:
        self.handler = handler()
        self.model = model
        self.report_service = ReportGenerationService()
        self.sql_agent = SQLAgent(self.report_service.report_engine)
        self.tools = self.sql_agent.get_tools()

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
        return f"data: {json.dumps({'type': type_, 'data': data})}\n\n"

    def stream_messages(self, messages):
        messages.append({"role": "system", "content": self.system_prompt})

        yield self._event("status", "Understanding request...")

        # First LLM call
        response = self.handler.get_response_with_message_list(
            messages, self.model, tools=self.tools
        )

        yield self._event("status", "Analyzing...")

        while True:
            # 🔹 TOOL CALL HANDLING
            if "tool_calls" in response:
                yield self._event("status", "Fetching schema...")

                for call in response["tool_calls"]:
                    tool_result = self.sql_agent.handle_tool_call(call)

                    messages.append(
                        {
                            "role": "tool",
                            "tool_name": call["function"]["name"],
                            "content": json.dumps(tool_result),
                        }
                    )

                yield self._event("status", "Generating SQL...")

                # Call LLM again with tool results
                response = self.handler.get_response_with_message_list(
                    messages, self.model, tools=self.tools
                )

                continue

            # 🔹 FINAL RESPONSE
            content = response.get("content")

            if content:
                yield self._event("message", content)

            break
