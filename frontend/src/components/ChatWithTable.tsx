import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import type { Message } from "@/lib/chat";
import Navbar from "./Navbar";
import { ArrowUpDown, Sparkles, Send, FileText, TrendingUp, Users } from "lucide-react";

type TableRow = Record<string, any>;

const API_BASE_URL = import.meta.env.VITE_API_URL

export default function ChatWithTable() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [tableData, setTableData] = useState<TableRow[]>([]);
  const [status, setStatus] = useState<string>("");

  const suggestedPrompts = [
    { title: "Revenue Analysis", desc: "Show revenue trends by region this year", icon: TrendingUp },
    { title: "Customer Overview", desc: "Top 10 paying customers by LTV", icon: Users },
    { title: "Weekly Report", desc: "Summarize weekly signups and active users", icon: FileText },
    { title: "Anomaly Detection", desc: "Find any anomalies in the payment logs", icon: Sparkles },
  ];

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage: Message = { role: "user", content: input };

    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);

    setInput("");
    setStatus("Starting...");

    const eventSource = new EventSource(
      `${API_BASE_URL}/ai/api/chat?messages=${encodeURIComponent(JSON.stringify(updatedMessages))}`
    );

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);

      // 🔹 STATUS UPDATES
      if (data.type === "status") {
        setStatus(data.data);
      }

      // 🔹 FINAL MESSAGE
      if (data.type === "message") {
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: data.data,
          },
        ]);

        setStatus("");
        eventSource.close();
      }

      // 🔹 OPTIONAL: TABLE DATA
      if (data.type === "data") {

        console.log(data.data.rows)
        if (Array.isArray(data.data.rows)) {
          setTableData(data.data.rows);
        } else {
          console.warn("Invalid rows:", data.data.rows);
        }
        setStatus(data.data.error);
      }
    };

    eventSource.onerror = () => {
      eventSource.close();
      setStatus("Something went wrong");
    };
  };
  // Helper to format numbers in table elegantly
  const formatCellValue = (val: any) => {
    if (typeof val === "number") {
      return new Intl.NumberFormat('en-US').format(val);
    }
    return String(val ?? "");
  };

  const columns =
    Array.isArray(tableData) && tableData.length > 0
      ? Object.keys(tableData[0])
      : [];

  return (
    <div className="min-h-screen flex flex-col bg-zinc-50 dark:bg-zinc-950 font-sans">
      <Navbar />
      
      {/* Main SaaS Layout */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-8 p-6 lg:p-10 flex-1 min-h-0 max-w-[1600px] mx-auto w-full">

        {/* --- Left Panel: Query Interface (33%) --- */}
        <div className="col-span-1 md:col-span-5 lg:col-span-4 flex flex-col min-h-[600px]">
          <div className="mb-4">
            <h1 className="text-2xl font-semibold tracking-tight text-foreground">Query Assistant</h1>
            <p className="text-sm text-foreground/60 mt-1">Ask questions in plain English to extract data.</p>
          </div>
          
          <Card className="flex flex-col flex-1 min-h-0 glass-card border-none rounded-2xl shadow-sm">
            <CardContent className="flex flex-col h-full p-0 min-h-0">
              
              <ScrollArea className="flex-1 px-5 py-4 h-0">
                {messages.length === 0 ? (
                  <div className="flex flex-col justify-center h-full space-y-8 animate-in fade-in duration-700 py-10">
                    <div className="text-center space-y-2">
                       <div className="w-12 h-12 bg-indigo-100 dark:bg-indigo-900/30 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-indigo-200 dark:border-indigo-800/50">
                         <Sparkles className="w-6 h-6 text-indigo-600 dark:text-indigo-400" />
                       </div>
                       <h3 className="text-lg font-medium tracking-tight">How can I help you?</h3>
                       <p className="text-sm text-foreground/50 max-w-[250px] mx-auto">Get started by selecting a prompt below or typing your own query.</p>
                    </div>

                    <div className="grid grid-cols-1 gap-3">
                      {suggestedPrompts.map((p, i) => (
                        <button
                          key={i}
                          onClick={() => {
                            setInput(p.desc);
                          }}
                          className="flex items-start gap-3 p-4 rounded-xl border border-zinc-200 dark:border-zinc-800/60 bg-white/50 dark:bg-zinc-900/30 hover:bg-zinc-100 dark:hover:bg-zinc-800/80 hover:border-cyan-500/30 transition-all duration-300 text-left group active:scale-[0.98]"
                        >
                          <p.icon className="w-5 h-5 text-zinc-400 group-hover:text-cyan-500 mt-0.5 shrink-0 transition-colors" />
                          <div>
                            <p className="text-sm font-medium text-foreground">{p.title}</p>
                            <p className="text-xs text-foreground/50 mt-1">{p.desc}</p>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="space-y-6 pb-4">
                {messages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"} animate-in slide-in-from-bottom-2 fade-in duration-500`}
                  >
                    {msg.role === "assistant" && (
                      <div className="flex gap-2 items-center mb-1.5 ml-1">
                        <Sparkles className="w-3.5 h-3.5 text-indigo-500" />
                        <span className="text-xs font-semibold text-foreground/60 tracking-wider uppercase">QuerySense</span>
                      </div>
                    )}
                    <div
                      className={`px-4 py-3 rounded-2xl max-w-[90%] text-[14px] leading-relaxed font-medium ${msg.role === "user"
                        ? "bg-cyan-600 text-white rounded-br-sm shadow-sm"
                        : "bg-transparent text-foreground/90 border-l-2 border-indigo-500/50 rounded-none pl-4 py-1"
                        }`}
                    >
                      {msg.content}
                    </div>
                  </div>
                ))}
                
                {status && status === "Starting..." && (
                   <div className="flex flex-col items-start animate-in fade-in duration-300 mt-4">
                      <div className="flex gap-2 items-center mb-1.5 ml-1">
                        <Sparkles className="w-3.5 h-3.5 text-indigo-500 animate-pulse" />
                        <span className="text-xs font-semibold text-foreground/60 tracking-wider uppercase">Processing Query</span>
                      </div>
                      <div className="border-l-2 border-indigo-500/30 pl-4 py-2 flex items-center gap-1.5 opacity-70">
                        <div className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-bounce"></div>
                        <div className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-bounce" style={{ animationDelay: "150ms" }}></div>
                        <div className="w-1.5 h-1.5 rounded-full bg-indigo-600 animate-bounce" style={{ animationDelay: "300ms" }}></div>
                      </div>
                   </div>
                )}
                
                {status && status !== "Starting..." && status !== "" && (
                   <div className="flex justify-center my-4 animate-in fade-in zoom-in-95">
                     <span className="text-xs bg-red-500/10 text-red-600 dark:text-red-400 px-3 py-1.5 rounded-md font-medium border border-red-500/20">
                       {status}
                     </span>
                   </div>
                )}
              </div>
            )}
          </ScrollArea>

            <div className="p-4 bg-white/40 dark:bg-zinc-950/40 border-t border-zinc-200 dark:border-zinc-800">
              <div className="relative group">
                <Input
                  value={input}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    setInput(e.target.value)
                  }
                  placeholder="Ask anything about your data..."
                  className="w-full bg-white dark:bg-zinc-900 border-zinc-300 dark:border-zinc-700 focus-visible:ring-cyan-500 focus-visible:border-cyan-500 shadow-sm pl-4 pr-12 h-12 text-[14px] rounded-xl transition-all"
                  onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => {
                    if (e.key === "Enter") handleSend();
                  }}
                />
                <Button 
                  onClick={handleSend}
                  size="icon"
                  className="absolute right-1.5 top-1.5 h-9 w-9 rounded-lg bg-cyan-600 hover:bg-cyan-700 text-white shadow-sm transition-all active:scale-95"
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
        </div>

        {/* --- Right Panel: Data Presentation (66%) --- */}
        <div className="col-span-1 md:col-span-7 lg:col-span-8 flex flex-col min-h-0">
          <Card className="flex flex-col h-full glass-card border-[0.5px] border-zinc-200 dark:border-zinc-800/80 rounded-2xl overflow-hidden shadow-sm">
            <CardContent className="p-0 flex flex-col flex-1 min-h-0">
              
              {/* Header */}
              <div className="px-6 py-4 bg-white/80 dark:bg-zinc-900/80 backdrop-blur-md z-10 border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-semibold text-foreground tracking-tight">Query Results</h2>
                  <p className="text-xs text-foreground/50 mt-0.5 font-medium">Auto-generated via QuerySense</p>
                </div>
                {tableData.length > 0 && (
                  <div className="text-xs font-semibold px-2.5 py-1 rounded-md bg-zinc-100 dark:bg-zinc-800 text-foreground/70 border border-zinc-200 dark:border-zinc-700">
                    {tableData.length} records
                  </div>
                )}
              </div>
              
              {/* Table Data area */}
              <div className="flex-1 overflow-auto bg-white/30 dark:bg-black/10">
                <table className="w-full text-left border-collapse text-sm">
                  <thead className="sticky top-0 bg-zinc-50 dark:bg-zinc-900/95 backdrop-blur shadow-sm z-10">
                    <tr>
                      {columns.map((col) => (
                        <th key={col} className="px-6 py-3 border-b border-zinc-200 dark:border-zinc-800 font-semibold text-foreground/70 uppercase tracking-wider text-[11px] group cursor-default select-none">
                          <div className="flex items-center gap-1.5">
                            {col}
                            <ArrowUpDown className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity text-foreground/40" />
                          </div>
                        </th>
                      ))}
                    </tr>
                  </thead>

                  <tbody className="divide-y divide-zinc-200 dark:divide-zinc-800/60 font-medium">
                    {Array.isArray(tableData) && tableData.length > 0 ? (
                      tableData.map((row, i) => (
                        <tr key={i} className="hover:bg-zinc-50 dark:hover:bg-zinc-800/40 even:bg-white/20 dark:even:bg-zinc-900/20 transition-colors group">
                          {columns.map((col) => (
                            <td key={col} className="px-6 py-3.5 text-foreground/80 whitespace-nowrap group-hover:text-foreground">
                              {formatCellValue(row[col])}
                            </td>
                          ))}
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan={columns.length || 1} className="py-24 text-center">
                           <div className="flex flex-col items-center justify-center opacity-60">
                             <FileText className="w-10 h-10 text-zinc-400 dark:text-zinc-600 mb-3" />
                             <p className="text-sm font-medium text-foreground">No data to display</p>
                             <p className="text-xs text-foreground/60 mt-1">Run a prompt to generate insights.</p>
                           </div>
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}



