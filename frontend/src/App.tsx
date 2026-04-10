import { AuthProvider } from "@/context/AuthContext"
import { ThemeProvider } from "@/context/ThemeContext"
import Home from "@/components/Home"

export default function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
      <AuthProvider>
        <Home />
      </AuthProvider>
    </ThemeProvider>
  )
}
