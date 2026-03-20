
import LoginForm from "@/components/LoginForm"
import { useAuth } from "@/context/AuthContext"
import ChatWithTable from "@/components/ChatWithTable"

export default function Home() {
  const { token } = useAuth()
  if (!token) {
    return (
      <LoginForm />
    )
  }
  return (
    <ChatWithTable />
  )
}
