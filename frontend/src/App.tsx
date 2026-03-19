import { AuthProvider } from "@/context/AuthContext"
import Home from "@/components/Home"
export default function App() {

  return (
    <AuthProvider>
      <Home />
    </AuthProvider>
  )
}
