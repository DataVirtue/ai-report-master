from ai.handlers.open_router_handler import OpenRouterHandler


class SqlGenerator:
    base_prompt = """
    You are an expert PostgreSQL SQL generator.

    Given a user question and database schema context, generate a SQL query.

    Rules:
        - Return ONLY the SQL query
        - Do NOT explain anything
        - Do NOT include markdown
        - Do NOT describe tables
        - Only output valid SQL

    User question:
    """
    base_prompt = """
            You are a SQL generation engine.

            Your task is to convert the user question into SQL using the provided database schema.

            Follow these steps STRICTLY:

            Step 1: Understand the question
            - Identify the main entity
            - Identify metrics
            - Identify filters
            - Identify grouping

            Step 2: Identify tables
            - Fact tables
            - Dimension tables

            Step 3: Determine joins
            - Use foreign key relationships only

            Step 4: Aggregation rules
            - If multiple fact tables are used, aggregate them separately before joining

            Step 5: Generate SQL

            Return output in this format:

            PLAN:
            - main_table:
            - fact_tables:
            - dimension_tables:
            - joins:
            - aggregations:
            - filters:
            - grouping:

            SQL:
            <final SQL query>
                """

    def __init__(self) -> None:
        self.handler = OpenRouterHandler()

    def get_sql(self, context):
        prompt = f"""
            {self.base_prompt}

        Schema context:
        {str(context)}

        SQL:
        """
        return self.handler.get_response(prompt, llm_model="openai/o4-mini")
