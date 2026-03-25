from ai.handlers import OpenRouterHandler
from .report_generation_service import ReportGenerationService
from ai.services import report_generation_service
import json
import logging


class ChatService:
    system_prompt = """
        You are a report assitant 
        when the user asks to generate report clarify the requirement as necessary 
        and when you are ready generate a 
        proper prompt for an ai sql engine to generate the relevant report output format:
        Assume the user is not technical and relevant schema details will be provided to the sql engine

        {"message": message
        "report_generation_prompt":report_generation_prompt
        }
        SQL PROMPT CAN BE BLANK IF YOU ARE NOT READY 
        DONT KEEP DRILLING THE USER MAKE YOUR BEST ATTEMPT AND WE CAN MODIFY IT FROM THERE
    """

    def __init__(
        self, handler=OpenRouterHandler, model="openrouter/hunter-alpha"
    ) -> None:
        self.handler = handler()
        self.model = model
        self.report_service = ReportGenerationService()

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

    def send_messages(self, messages):
        messages.append({"role": "system", "content": self.system_prompt})
        res = self.handler.get_response_with_message_list(messages, self.model)
        cleaned_json = self.clean_llm_json(res)
        parsed = json.loads(cleaned_json)
        message_response = parsed.get("message")
        report_generation_prompt = parsed.get("report_generation_prompt")
        print("Report Generation Prompt", report_generation_prompt)
        data = ""
        if report_generation_prompt:
            data = self.report_service.get_report(report_generation_prompt)
        return {
            "message": message_response,
            "data": data,
        }
