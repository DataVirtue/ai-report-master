import ChatWithTable from "@/components/ChatWithTable"
import { Routes, Route } from "react-router-dom"
import { SidebarProvider } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/AppSidebar"
import type { Conversation } from "@/lib/chat"
import { useState, useEffect, useCallback } from "react"
import { get_conversation_list } from "@/lib/chat"
import { useAuth } from "@/context/AuthContext"

export default function Home() {
  const { token } = useAuth()
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [nextUrl, setNextUrl] = useState<string | null>(null)
  const [isLoadingMore, setIsLoadingMore] = useState(false)


  function updateConversationTitle(id: number, title: string) {
    setConversations(prev =>
      prev.map(conv =>
        conv.id === id ? { ...conv, title } : conv
      )
    )
  }

  const getConvoWrapper = async () => {
    if (!token) return;
    try {
      const data = await get_conversation_list(token);
      if (data.results) {
        setConversations(data.results);
        setNextUrl(data.next);
      } else {
        setConversations(data);
        setNextUrl(null);
      }
    } catch (e) {
      console.error(e);
    }
  }

  const loadMoreConversations = useCallback(async () => {
    if (!token || !nextUrl || isLoadingMore) return;
    setIsLoadingMore(true);
    try {
      const data = await get_conversation_list(token, nextUrl);
      if (data.results) {
        setConversations(prev => [...prev, ...data.results]);
        setNextUrl(data.next);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoadingMore(false);
    }
  }, [token, nextUrl, isLoadingMore]);

  useEffect(() => {
    if (!token) {
      throw Error("Unauthenticated user trying to find conversations")
    }
    getConvoWrapper();
  }, [])



  return (
    <SidebarProvider>
      <AppSidebar 
        conversations={conversations} 
        onLoadMore={loadMoreConversations}
        hasMore={!!nextUrl}
        isLoadingMore={isLoadingMore}
      />
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
