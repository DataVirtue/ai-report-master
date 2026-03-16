from typing import Dict
import logging
import json


class DocStringGenerator:
    base_query = """
        You are a database documentation generator used for semantic search.

        Your job is to generate a rich docstring for each table so that a vector search
        system can easily retrieve the correct table for natural language questions.

        Rules:
        1. Only use information from the provided schema.
        2. Do NOT invent columns or relationships.
        3. Include searchable business keywords.
        4. Mention relationships to other tables.
        5. Highlight important columns like ids, amounts, dates, and foreign keys.
        6. Explain the purpose of the table in business terms.
        7. Keep each docstring between 80–150 words.
        8. Do not skip tables.
        9. Do not add extra tables.
        10. If information is missing, still generate a best-effort docstring.

        Docstring structure:

        Table: <table_name>

        Purpose:
        Explain what the table represents in business terms.

        Key Columns:
        Important columns and their meaning.

        Relationships:
        Foreign key relationships with other tables.

        Typical Queries:
        Examples of questions this table helps answer.

        Keywords:
        Comma separated search keywords (customer, invoice, payment, inventory, etc.)

       Return ONLY valid JSON.

        Format:
        {
            "table_name": "docstring"
        }

        Schema:
        """

    def __init__(self, handler):
        self.handler = handler()

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

    def generate_doc_strings(self, schema_dict: Dict):
        results = {}

        def chunk_dict(data, size=20):
            for i in range(0, len(data), size):
                yield {table["table_name"]: table for table in data[i : i + size]}

        for chunk in chunk_dict(schema_dict, 20):
            query = self.base_query + str(chunk)

            response = self.handler.get_response(query)

            try:
                cleaned_json = self.clean_llm_json(response)
                parsed = json.loads(cleaned_json)
                results.update(parsed)

            except Exception as e:
                logging.error(f"Bad LLM response{e}")
                logging.debug(response)

        return results

    # def generate_doc_strings(self, schema_dict: Dict):
    #     query = self.query + str(schema_dict)
    #
    #     response = self.handler.get_response(query)
    #     try:
    #         return_dict = ast.literal_eval(response)
    #         return return_dict
    #     except (ValueError, SyntaxError) as e:
    #         logging.debug(response)
    #         logging.error(f"Incorrect LLM response{e}")
    #         return {}
