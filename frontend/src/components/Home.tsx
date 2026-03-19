
import LoginForm from "@/components/LoginForm"
import { useAuth } from "@/context/AuthContext"
export default function Home() {
  const { token } = useAuth()
  if (!token) {
    return (
      <LoginForm />
    )
  }
  return (
    <h1>Hello</h1>
  )
}
