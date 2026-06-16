import ChatWithTable from "@/components/ChatWithTable"
import { Routes, Route } from "react-router-dom"
import { SidebarProvider } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/AppSidebar"
import type { Conversation, SavedReport } from "@/lib/chat"
import { useState, useEffect, useCallback } from "react"
import { get_conversation_list, get_saved_reports_list, delete_saved_report } from "@/lib/chat"
import { useAuth } from "@/context/AuthContext"
import SavedReportView from "@/components/SavedReportView"
import { useNavigate } from "react-router-dom"

export default function Home() {
  const { token } = useAuth()
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [nextUrl, setNextUrl] = useState<string | null>(null)
  const [isLoadingMore, setIsLoadingMore] = useState(false)

  const [savedReports, setSavedReports] = useState<SavedReport[]>([])
  const [nextReportUrl, setNextReportUrl] = useState<string | null>(null)
  const [isLoadingMoreReports, setIsLoadingMoreReports] = useState(false)
  const navigate = useNavigate()

  async function handleDeleteReport(id: number) {
    if (!token) return;
    try {
      await delete_saved_report(token, id.toString());
      setSavedReports(prev => prev.filter(r => r.id !== id));
      navigate('/'); // Go back home if currently viewing the deleted report
    } catch (e) {
      console.error("Failed to delete report", e);
    }
  }

  function handleUpdateReportTitle(id: number, title: string) {
    setSavedReports(prev => prev.map(r => r.id === id ? { ...r, title } : r));
  }


  function updateConversationTitle(id: number, title: string) {
    setConversations(prev => {
      const exists = prev.some(conv => conv.id === id);
      if (exists) {
        return prev.map(conv =>
          conv.id === id ? { ...conv, title } : conv
        );
      } else {
        return [{ id, title }, ...prev];
      }
    });
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

  const getSavedReportsWrapper = async () => {
    if (!token) return;
    try {
      const data = await get_saved_reports_list(token);
      if (data.results) {
        setSavedReports(data.results);
        setNextReportUrl(data.next);
      } else {
        setSavedReports(data);
        setNextReportUrl(null);
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

  const loadMoreReports = useCallback(async () => {
    if (!token || !nextReportUrl || isLoadingMoreReports) return;
    setIsLoadingMoreReports(true);
    try {
      const data = await get_saved_reports_list(token, nextReportUrl);
      if (data.results) {
        setSavedReports(prev => [...prev, ...data.results]);
        setNextReportUrl(data.next);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoadingMoreReports(false);
    }
  }, [token, nextReportUrl, isLoadingMoreReports]);

  useEffect(() => {
    if (!token) {
      throw Error("Unauthenticated user trying to find conversations")
    }
    getConvoWrapper();
    getSavedReportsWrapper();
  }, [])



  return (
    <SidebarProvider>
      <AppSidebar
        conversations={conversations}
        onLoadMore={loadMoreConversations}
        hasMore={!!nextUrl}
        isLoadingMore={isLoadingMore}
        savedReports={savedReports}
        onLoadMoreReports={loadMoreReports}
        hasMoreReports={!!nextReportUrl}
        isLoadingMoreReports={isLoadingMoreReports}
        onDeleteReport={handleDeleteReport}
      />
      <div className="flex flex-col h-screen w-full overflow-hidden bg-background relative">
        <main className="flex-1 overflow-hidden relative">
          <Routes>
            <Route path="/" element={<ChatWithTable updateConversationTitle={updateConversationTitle} />} />
            <Route path="/:conversationId"
              element={<ChatWithTable updateConversationTitle={updateConversationTitle} />} />
            <Route path="/report/:reportId" element={
              <SavedReportView
                savedReports={savedReports}
                onUpdateReportTitle={handleUpdateReportTitle}
              />
            } />
          </Routes>
        </main>
      </div>
    </SidebarProvider>
  )
}
