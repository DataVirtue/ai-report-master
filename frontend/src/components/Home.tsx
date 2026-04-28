import ChatWithTable from "@/components/ChatWithTable"
import { Routes, Route } from "react-router-dom"
import { SidebarProvider } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/AppSidebar"
import type { Conversation } from "@/lib/chat"
import { useState, useEffect } from "react"
import { get_conversation_list } from "@/lib/chat"
import { useAuth } from "@/context/AuthContext"

export default function Home() {
  const { token } = useAuth()
  const [conversations, setConversations] = useState<Conversation[]>([])


  function updateConversationTitle(id: number, title: string) {
    setConversations(prev =>
      prev.map(conv =>
        conv.id === id ? { ...conv, title } : conv
      )
    )
  }

  useEffect(() => {
    console.log(conversations)
    if (!token) {
      throw Error("Unauthenticated user trying to find conversations")
    }
    const getConvoWrapper = async () => {
      const allConvos = await get_conversation_list(token);
      setConversations([...allConvos])
      console.log(conversations)
    }
    getConvoWrapper();
    console.log(conversations)
  }, [])



  return (
    <SidebarProvider>
      <AppSidebar conversations={conversations} />
      <div className="flex flex-col h-screen w-full overflow-hidden bg-background relative">
        <main className="flex-1 overflow-hidden relative">
          <Routes>
            <Route path="/" element={<ChatWithTable updateConversationTitle={updateConversationTitle} />} />
            <Route path="/:conversationId"
              element={<ChatWithTable updateConversationTitle={updateConversationTitle} />} />
          </Routes>
        </main>
      </div>
    </SidebarProvider>
  )
}
