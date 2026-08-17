import { useEffect, useState, useRef } from "react";
import { useParams } from "react-router-dom";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/context/AuthContext";
import { get_saved_report_data, get_saved_report_details, update_saved_report_title, type SavedReport } from "@/lib/chat";
import { Pencil, Check, X } from "lucide-react";
import ScheduleReportDialog from "@/components/ScheduleReportDialog";

type TableRow = Record<string, any>;

type SavedReportViewProps = {
  savedReports?: SavedReport[];
  onUpdateReportTitle?: (id: number, title: string) => void;
};

export default function SavedReportView({ savedReports = [], onUpdateReportTitle }: SavedReportViewProps) {
  const { reportId } = useParams();
  const { token } = useAuth();
  const [tableData, setTableData] = useState<TableRow[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [title, setTitle] = useState<string>("Loading Title...");
  const [isEditingTitle, setIsEditingTitle] = useState(false);
  const [editTitleValue, setEditTitleValue] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const fetchReport = async () => {
      if (!token || !reportId) return;
      setIsLoading(true);
      setError(null);
      
      try {
        const parsedId = parseInt(reportId, 10);
        let foundTitle = savedReports.find(r => r.id === parsedId)?.title;
        
        if (foundTitle) {
          setTitle(foundTitle);
        } else {
          // If navigated directly, fetch details to get the title
          try {
            const details = await get_saved_report_details(token, reportId);
            setTitle(details.title);
          } catch (e) {
             console.error("Could not fetch title", e);
             setTitle(`Report #${reportId}`);
          }
        }

        const reportData = await get_saved_report_data(token, reportId, "1");
        setTableData(reportData["data"]);
      } catch (err) {
        console.error(err);
        setError("Failed to load report data.");
      } finally {
        setIsLoading(false);
      }
    };
    fetchReport();
  }, [token, reportId, savedReports]);

  useEffect(() => {
    if (isEditingTitle && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isEditingTitle]);

  const handleSaveTitle = async () => {
    if (!token || !reportId || !editTitleValue.trim() || editTitleValue === title) {
      setIsEditingTitle(false);
      return;
    }

    try {
      await update_saved_report_title(token, reportId, editTitleValue);
      setTitle(editTitleValue);
      if (onUpdateReportTitle) {
        onUpdateReportTitle(parseInt(reportId, 10), editTitleValue);
      }
    } catch (e) {
      console.error("Failed to update title", e);
    } finally {
      setIsEditingTitle(false);
    }
  };

  const columns =
    Array.isArray(tableData) && tableData.length > 0
      ? Object.keys(tableData[0])
      : [];

  return (
    <div className="h-full p-4 overflow-hidden">
      <Card className="h-full flex flex-col">
        <CardContent className="p-4 flex-1 overflow-auto">
          <div className="flex items-center mb-4 min-h-[40px]">
            {isEditingTitle ? (
              <div className="flex items-center gap-2 max-w-sm w-full">
                <Input
                  ref={inputRef}
                  value={editTitleValue}
                  onChange={(e) => setEditTitleValue(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") handleSaveTitle();
                    if (e.key === "Escape") setIsEditingTitle(false);
                  }}
                  className="flex-1"
                />
                <button onClick={handleSaveTitle} className="p-2 hover:bg-muted rounded-md text-green-600">
                  <Check className="h-4 w-4" />
                </button>
                <button onClick={() => setIsEditingTitle(false)} className="p-2 hover:bg-muted rounded-md text-destructive">
                  <X className="h-4 w-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2 group cursor-pointer" onClick={() => {
                setEditTitleValue(title);
                setIsEditingTitle(true);
              }}>
                <h2 className="text-xl font-bold tracking-tight">{title}</h2>
                <button className="opacity-0 group-hover:opacity-100 transition-opacity p-2 hover:bg-muted rounded-md text-muted-foreground">
                  <Pencil className="h-4 w-4" />
                </button>
              </div>
            )}

            {reportId && !isEditingTitle && (
              <div className="ml-auto">
                <ScheduleReportDialog reportId={parseInt(reportId, 10)} reportTitle={title} />
              </div>
            )}
          </div>

          {isLoading ? (
            <div className="text-sm text-muted-foreground">Loading report...</div>
          ) : error ? (
            <div className="text-sm text-destructive">{error}</div>
          ) : (
            <div className="rounded-md border">
              <table className="w-full text-sm">
                <thead className="bg-muted/50">
                  <tr className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
                    {columns.map((col) => (
                      <th
                        key={col}
                        className="h-10 px-4 text-left align-middle font-medium text-muted-foreground whitespace-nowrap"
                      >
                        {col}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {Array.isArray(tableData) && tableData.length > 0 ? (
                    tableData.map((row, i) => (
                      <tr
                        key={i}
                        className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
                      >
                        {columns.map((col) => (
                          <td
                            key={col}
                            className="p-4 align-middle whitespace-nowrap"
                          >
                            {String(row[col] ?? "")}
                          </td>
                        ))}
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td
                        colSpan={columns.length || 1}
                        className="h-24 text-center align-middle text-muted-foreground"
                      >
                        No data available in this report.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
