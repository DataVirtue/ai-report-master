from ai.report_engine.loader import get_engine
from ai.services.report_writer_service import ReportWriter


class ReportGenerationService:
    def __init__(self) -> None:
        self.report_engine = get_engine()
        self.report_writer = ReportWriter()

    def get_report(self, query, page_no):
        return self.report_engine.run_sql_with_pagination(query, page_no)

    def get_report_csv(self, query):
        res = self.report_engine.run_sql(query)
        data = res.get("data")
        status = res.get("status")
        reason = res.get("error")
        if status == "Error":
            raise ValueError(reason)
        return self.report_writer.generate_csv_file(data=data)
