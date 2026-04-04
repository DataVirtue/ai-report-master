from ai.report_engine import ReportEngine


class ReportGenerationService:
    def __init__(self) -> None:
        self.report_engine = ReportEngine()

    def get_report(self, query):
        return self.report_engine.get_report_data(query, top_k=10)
