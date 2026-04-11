import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import type { Message } from "@/lib/chat";
import { useAuth } from "@/context/AuthContext"


type TableRow = Record<string, any>;


const API_BASE_URL = import.meta.env.VITE_API_URL


export default function ChatWithTable() {

  const { token } = useAuth()
  const [messages, setMessages] = useState<Message[]>([
    { role: "user", content: "hello" },
    { role: "assistant", content: "hi" }
  ]);
  const [input, setInput] = useState<string>("");
  const [tableData, setTableData] = useState<TableRow[]>([]);
  const [status, setStatus] = useState<string>("");

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { role: "user", content: input };

    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);

    setInput("");
    setStatus("Starting...");


    try {

      const response = await fetch(`${API_BASE_URL}/ai/api/chat/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ messages: updatedMessages }),
      });
      const reader = response.body?.getReader();
      if (!reader) throw new Error("No response body");

      const decoder = new TextDecoder();
      let buffer = "";


      while (true) {
        const { done, value } = await reader?.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split("\n\n");

        // The last part might be incomplete, so we keep it in the buffer
        buffer = parts.pop() || "";

        for (const part of parts) {
          if (part.startsWith("data: ")) {
            const jsonStr = part.replace(/^data:\s*/, "");
            const data = JSON.parse(jsonStr);

            // 🔹 STATUS UPDATES
            if (data.type === "status") {
              setStatus(data.data);
            }

            // 🔹 FINAL MESSAGE
            if (data.type === "message") {
              setMessages((prev) => [
                ...prev,
                { role: "assistant", content: data.data },
              ]);
              setStatus("")
              break;
            }

            // 🔹 TABLE DATA / ERROR
            if (data.type === "data") {
              if (Array.isArray(data.data.rows)) {
                setTableData(data.data.rows);
              }
              setStatus(data.data.error || "");
            }
          }
        }
      }
    } catch (err) {
      console.error(err);
      setStatus("Something went wrong");
    }
  };
  const columns =
    Array.isArray(tableData) && tableData.length > 0
      ? Object.keys(tableData[0])
      : [];
  return (
    <div className="grid grid-cols-10 gap-4 h-full px-4 pb-4">
      {/* Chat Section */}
      <Card className="col-span-3 flex flex-col min-h-0 ">
        <CardContent className="flex flex-col h-full p-4 min-h-0">
          <ScrollArea className="flex-1 mb-4 h-0">
            <div className="space-y-3">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`p-2 rounded-xl max-w-xs ${msg.role === "user"
                    ? "bg-blue-500 text-white ml-auto"
                    : "bg-muted text-foreground"
                    }`}
                >
                  {msg.content}
                </div>
              ))}
            </div>
          </ScrollArea>

          <div className="flex gap-2">
            {status && (
              <div className="text-sm text-gray-500 mb-2">
                {status}
              </div>
            )}
            <Input
              value={input}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setInput(e.target.value)
              }
              placeholder="Type a message..."
              onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => {
                if (e.key === "Enter") handleSend();
              }}
            />
            <Button onClick={handleSend}>Send</Button>
          </div>
        </CardContent>
      </Card>

      {/* Table Section */}

      <Card className="col-span-7 flex flex-col">


        <CardContent className="p-4 overflow-auto">
          <h2 className="text-lg font-semibold mb-3">Live Data</h2>
          <table className="w-full text-sm border">
            <thead>
              <tr className="border-b">
                {columns.map((col) => (
                  <th key={col} className="text-left p-2">
                    {col}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody>
              {Array.isArray(tableData) &&
                tableData.map((row, i) => (
                  <tr key={i} className="border-b">
                    {columns.map((col) => (
                      <td key={col} className="p-2">
                        {String(row[col] ?? "")}
                      </td>
                    ))}
                  </tr>
                ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
}



