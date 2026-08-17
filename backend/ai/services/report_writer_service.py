import pandas as pd
from enum import Enum
import io


class SupportedFileType(Enum):
    CSV = "CSV"


class ReportWriter:
    def generate_file(self, data, file_type: SupportedFileType):
        if file_type is SupportedFileType.CSV:
            return self.generate_csv_file(data)

    def generate_csv_file(self, data):
        buffer = io.BytesIO()
        df = pd.DataFrame(data)
        df.to_csv(buffer, index=False)
        return buffer.getvalue()
