import { useState } from "react"
import LoginForm from "@/components/LoginForm"
import RegisterForm from "@/components/RegisterForm"
import Navbar from "@/components/Navbar"
import { useAuth } from "@/context/AuthContext"
import ChatWithTable from "@/components/ChatWithTable"

export default function Home() {
  const { token } = useAuth()
  const [isRegistering, setIsRegistering] = useState(false)

  if (!token) {
    if (isRegistering) {
      return <RegisterForm onLoginClick={() => setIsRegistering(false)} />
    }
    return (
      <LoginForm onRegisterClick={() => setIsRegistering(true)} />
    )
  }
  return (
    <div className="flex flex-col h-screen overflow-hidden bg-muted/20">
      <Navbar />
      <main className="flex-1 overflow-hidden">
        <ChatWithTable />
      </main>
    </div>
  )
}
