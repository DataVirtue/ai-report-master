from .engine import ReportEngine
# report_engine/loader.py

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = ReportEngine()
    return _engine
