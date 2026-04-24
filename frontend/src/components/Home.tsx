import ChatWithTable from "@/components/ChatWithTable"
import { Routes, Route } from "react-router-dom"
import { SidebarProvider } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/AppSidebar"

export default function Home() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <div className="flex flex-col h-screen w-full overflow-hidden bg-background relative">
        <main className="flex-1 overflow-hidden relative">
          <Routes>
            <Route path="/" element={<ChatWithTable />} />
            <Route path="/:conversationId" element={<ChatWithTable />} />
          </Routes>
        </main>
      </div>
    </SidebarProvider>
  )
}
