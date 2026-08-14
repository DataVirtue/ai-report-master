from ai.report_engine.loader import get_engine


class ReportGenerationService:
    def __init__(self) -> None:
        self.report_engine = get_engine()

    def get_report(self, query, page_no):
        return self.report_engine.run_sql_with_pagination(query, page_no)
