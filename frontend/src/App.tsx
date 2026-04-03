import { AuthProvider } from "@/context/AuthContext"
import Home from "@/components/Home"
import { ThemeProvider } from "@/components/theme-provider"

export default function App() {

  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <AuthProvider>
        <Home />
      </AuthProvider>
    </ThemeProvider>
  )
}
