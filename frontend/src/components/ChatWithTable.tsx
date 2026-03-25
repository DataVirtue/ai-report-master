import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import type { Message } from "@/lib/chat";
import { send_messages } from "@/lib/chat";


type TableRow = {
  id: number;
  query: string;
  result: string;
};

export default function ChatWithTable() {

  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [tableData, setTableData] = useState<TableRow[]>([]);

  const handleSend = async (): Promise<any> => {
    if (!input.trim()) return;

    const userMessage: Message = { role: "user", content: input };

    const newRow: TableRow = {
      id: tableData.length + 1,
      query: input,
      result: "Generated",
    };

    setMessages((prev) => [...prev, userMessage]);
    const res = await send_messages(messages)
    console.log(res)
    const botResponse: Message = {
      role: "assistant",
      content: res.message
    }
    console.log("res data", res.data)
    setMessages((prev) => [...prev, botResponse]);


    setTableData((prev) => [...prev, newRow]);
    setInput("");

  };

  return (
    <div className="grid grid-cols-3 gap-4 h-screen p-4 ">
      {/* Chat Section */}
      <Card className="col-span-2 flex flex-col min-h-0 ">
        <CardContent className="flex flex-col h-full p-4 min-h-0">
          <ScrollArea className="flex-1 mb-4 h-0">
            <div className="space-y-3">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`p-2 rounded-xl max-w-xs ${msg.role === "user"
                    ? "bg-blue-500 text-white ml-auto"
                    : "bg-gray-200"
                    }`}
                >
                  {msg.content}
                </div>
              ))}
            </div>
          </ScrollArea>

          <div className="flex gap-2">
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
      <Card className="flex flex-col">
        <CardContent className="p-4 overflow-auto">
          <h2 className="text-lg font-semibold mb-3">Live Data</h2>
          <table className="w-full text-sm border">
            <thead>
              <tr className="border-b">
                <th className="text-left p-2">#</th>
                <th className="text-left p-2">Query</th>
                <th className="text-left p-2">Result</th>
              </tr>
            </thead>
            <tbody>
              {tableData.map((row) => (
                <tr key={row.id} className="border-b">
                  <td className="p-2">{row.id}</td>
                  <td className="p-2">{row.query}</td>
                  <td className="p-2">{row.result}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
}



