import { AuthProvider, useAuth } from "@/context/AuthContext"
import { ThemeProvider } from "@/context/ThemeContext"
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Home from "@/components/Home"
import LoginForm from "@/components/LoginForm"
import RegisterForm from "@/components/RegisterForm"
import { TooltipProvider } from "@/components/ui/tooltip"

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { token } = useAuth();
  if (!token) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

export default function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
      <TooltipProvider>
        <AuthProvider>
          <BrowserRouter>
            <Routes>
              <Route path="/login" element={<LoginForm />} />
              <Route path="/register" element={<RegisterForm />} />
              <Route path="/*" element={
                <ProtectedRoute>
                  <Home />
                </ProtectedRoute>
              } />
            </Routes>
          </BrowserRouter>
        </AuthProvider>
      </TooltipProvider>
    </ThemeProvider>
  )
}
