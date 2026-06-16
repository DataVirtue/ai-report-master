import { Sidebar, SidebarContent, SidebarFooter, SidebarHeader, SidebarGroup, SidebarGroupContent, SidebarGroupLabel, SidebarMenu, SidebarMenuItem, SidebarMenuButton, SidebarTrigger, SidebarMenuSub, SidebarMenuSubItem, SidebarMenuSubButton } from "@/components/ui/sidebar"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { useAuth } from "@/context/AuthContext"
import { ModeToggle } from "@/components/ModeToggle"
import { MessageSquare, LogOut, Clock, ChevronRight, Loader2, FileText, Trash2 } from "lucide-react"
import { useNavigate } from "react-router-dom"
import { useEffect } from "react"
import { useInView } from "react-intersection-observer"
import type { Conversation } from "@/lib/chat"

type AppSidebarProps = {
  conversations: Conversation[];
  onLoadMore?: () => void;
  hasMore?: boolean;
  isLoadingMore?: boolean;
  savedReports?: any[];
  onLoadMoreReports?: () => void;
  hasMoreReports?: boolean;
  isLoadingMoreReports?: boolean;
  onDeleteReport?: (id: number) => void;
}

export function AppSidebar({ 
  conversations, 
  onLoadMore, 
  hasMore, 
  isLoadingMore,
  savedReports = [],
  onLoadMoreReports,
  hasMoreReports,
  isLoadingMoreReports,
  onDeleteReport
}: AppSidebarProps) {
  const { logout } = useAuth()
  const navigate = useNavigate()
  const { ref, inView } = useInView()
  const { ref: reportsRef, inView: reportsInView } = useInView()

  useEffect(() => {
    if (inView && hasMore && !isLoadingMore && onLoadMore) {
      onLoadMore()
    }
  }, [inView, hasMore, isLoadingMore, onLoadMore])

  useEffect(() => {
    if (reportsInView && hasMoreReports && !isLoadingMoreReports && onLoadMoreReports) {
      onLoadMoreReports()
    }
  }, [reportsInView, hasMoreReports, isLoadingMoreReports, onLoadMoreReports])
  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="h-14 p-4 border-b flex flex-row items-center gap-2">
        <SidebarTrigger className="shrink-0 -ml-2" />
        <span className="font-bold text-xl text-primary truncate group-data-[collapsible=icon]:hidden">
          QuerySense
        </span>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel className="text-xs uppercase tracking-wider text-muted-foreground mt-4 mb-2 group-data-[collapsible=icon]:hidden">Actions</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton tooltip="New Chat" onClick={() => navigate("/")} className="gap-2 h-10 px-2 group-data-[collapsible=icon]:px-0 group-data-[collapsible=icon]:justify-center">
                  <MessageSquare className="h-5 w-5 shrink-0" />
                  <span className="text-sm font-medium">New Chat</span>
                </SidebarMenuButton>
              </SidebarMenuItem>

              {conversations.length > 0 && (
                <Collapsible defaultOpen={false} className="group/collapsible">
                  <SidebarMenuItem>
                    <CollapsibleTrigger asChild>
                      <SidebarMenuButton tooltip="Recent Chats" className="gap-2 h-10 px-2 group-data-[collapsible=icon]:px-0 group-data-[collapsible=icon]:justify-center">
                        <Clock className="h-5 w-5 shrink-0" />
                        <span className="text-sm font-medium group-data-[collapsible=icon]:hidden">Recent Chats</span>
                        <ChevronRight className="ml-auto h-4 w-4 shrink-0 transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90 group-data-[collapsible=icon]:hidden" />
                      </SidebarMenuButton>
                    </CollapsibleTrigger>
                    <CollapsibleContent>
                      <SidebarMenuSub>
                        {conversations.map((convo) => (
                          <SidebarMenuSubItem key={convo.id}>
                            <SidebarMenuSubButton onClick={() => navigate(`/${convo.id}`)} className="cursor-pointer">
                              <span>{convo.title}</span>
                            </SidebarMenuSubButton>
                          </SidebarMenuSubItem>
                        ))}
                        {hasMore && (
                          <div ref={ref} className="py-2 flex justify-center">
                            {isLoadingMore ? <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" /> : <div className="h-4"></div>}
                          </div>
                        )}
                      </SidebarMenuSub>
                    </CollapsibleContent>
                  </SidebarMenuItem>
                </Collapsible>
              )}

              {savedReports.length > 0 && (
                <Collapsible defaultOpen={false} className="group/collapsible">
                  <SidebarMenuItem>
                    <CollapsibleTrigger asChild>
                      <SidebarMenuButton tooltip="Saved Reports" className="gap-2 h-10 px-2 group-data-[collapsible=icon]:px-0 group-data-[collapsible=icon]:justify-center">
                        <FileText className="h-5 w-5 shrink-0" />
                        <span className="text-sm font-medium group-data-[collapsible=icon]:hidden">Saved Reports</span>
                        <ChevronRight className="ml-auto h-4 w-4 shrink-0 transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90 group-data-[collapsible=icon]:hidden" />
                      </SidebarMenuButton>
                    </CollapsibleTrigger>
                    <CollapsibleContent>
                      <SidebarMenuSub>
                        {savedReports.map((report) => (
                          <SidebarMenuSubItem key={report.id}>
                            <SidebarMenuSubButton onClick={() => navigate(`/report/${report.id}`)} className="cursor-pointer flex items-center justify-between group/report-item w-full">
                              <span className="truncate pr-2 flex-1">{report.title}</span>
                              {onDeleteReport && (
                                <button 
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    onDeleteReport(report.id);
                                  }}
                                  className="opacity-0 group-hover/report-item:opacity-100 transition-opacity p-1 hover:bg-destructive/10 hover:text-destructive rounded-md shrink-0"
                                >
                                  <Trash2 className="h-3 w-3" />
                                </button>
                              )}
                            </SidebarMenuSubButton>
                          </SidebarMenuSubItem>
                        ))}
                        {hasMoreReports && (
                          <div ref={reportsRef} className="py-2 flex justify-center">
                            {isLoadingMoreReports ? <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" /> : <div className="h-4"></div>}
                          </div>
                        )}
                      </SidebarMenuSub>
                    </CollapsibleContent>
                  </SidebarMenuItem>
                </Collapsible>
              )}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="p-4 border-t flex flex-col gap-4 group-data-[collapsible=icon]:p-2 group-data-[collapsible=icon]:items-center">
        <div className="flex items-center justify-between w-full px-2 group-data-[collapsible=icon]:px-0 group-data-[collapsible=icon]:justify-center">
          <span className="text-sm font-medium text-muted-foreground group-data-[collapsible=icon]:hidden">Theme</span>
          <ModeToggle />
        </div>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton tooltip="Logout" onClick={logout} className="gap-2 h-10 px-2 group-data-[collapsible=icon]:px-0 group-data-[collapsible=icon]:justify-center text-destructive hover:text-destructive hover:bg-destructive/10 transition-colors">
              <LogOut className="h-5 w-5 shrink-0" />
              <span className="text-sm font-medium">Logout</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  )
}
