import { Sidebar, SidebarContent, SidebarFooter, SidebarHeader, SidebarGroup, SidebarGroupContent, SidebarGroupLabel, SidebarMenu, SidebarMenuItem, SidebarMenuButton, SidebarTrigger } from "@/components/ui/sidebar"
import { useAuth } from "@/context/AuthContext"
import { ModeToggle } from "@/components/ModeToggle"
import { MessageSquare, LogOut } from "lucide-react"
import { useNavigate } from "react-router-dom"
import type { Conversation } from "@/lib/chat"

type AppSidebarProps = {
  conversations: Conversation[];

}

export function AppSidebar({ conversations }: AppSidebarProps) {
  const { logout } = useAuth()
  const navigate = useNavigate()
  const conversationElements = conversations.map((convo) => (
    <>
      <SidebarMenuButton tooltip="Go to Chat" onClick={() => navigate(`/${convo.id}`)} className="gap-2 h-10 px-2 group-data-[collapsible=icon]:px-0 group-data-[collapsible=icon]:justify-center">
        <span className="text-sm font-medium" key={convo.id}>{convo.title}</span>
      </SidebarMenuButton>
    </>

  ))

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
                {...conversationElements}
              </SidebarMenuItem>
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
