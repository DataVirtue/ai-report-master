import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
const API_BASE_URL = import.meta.env.VITE_API_URL
import { useAuth } from "@/context/AuthContext"

export default function LoginForm() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { login } = useAuth()

  const handleLogin = async (formData: FormData) => {
    setLoading(true)
    setError(null)

    const username = formData.get("username")
    const password = formData.get("password")

    try {
      const res = await fetch(API_BASE_URL + "/users/api/token/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      })

      const data = await res.json()

      if (!res.ok) {
        throw new Error(data.detail || "Login failed")
      }
      login(data.access)

      alert("Login successful 🚀")
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-[calc(100vh-100px)] items-center justify-center p-4 relative overflow-hidden bg-zinc-50 dark:bg-zinc-950 transition-colors duration-300">
      
      <Card className="w-[400px] glass-card border-none rounded-2xl overflow-hidden relative z-10 transition-all duration-500 hover:shadow-cyan-600/10">
        <CardHeader className="space-y-1 pb-8">
          <CardTitle className="text-4xl font-extrabold tracking-tight text-center text-cyan-600 dark:text-cyan-400">
            Welcome Back
          </CardTitle>
          <p className="text-center text-sm text-foreground/60 mt-2">
            Enter your credentials to continue
          </p>
        </CardHeader>

        <CardContent>
          <form
            action={async (formData) => {
              await handleLogin(formData)
            }}
            className="space-y-5"
          >
            <div className="space-y-2 group">
              <Label htmlFor="username" className="text-sm font-medium text-foreground/80 group-focus-within:text-cyan-600 transition-colors">Username</Label>
              <Input 
                name="username" 
                placeholder="Enter username" 
                required 
                className="rounded-xl bg-white/50 dark:bg-zinc-900/50 border-zinc-200 dark:border-zinc-800 focus-visible:ring-cyan-500 focus-visible:ring-offset-0 transition-all shadow-sm h-11"
              />
            </div>

            <div className="space-y-2 group">
              <Label htmlFor="password" className="text-sm font-medium text-foreground/80 group-focus-within:text-cyan-600 transition-colors">Password</Label>
              <Input
                name="password"
                type="password"
                placeholder="••••••••"
                required
                className="rounded-xl bg-white/50 dark:bg-zinc-900/50 border-zinc-200 dark:border-zinc-800 focus-visible:ring-cyan-500 focus-visible:ring-offset-0 transition-all shadow-sm h-11"
              />
            </div>

            {error && (
              <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-xl">
                <p className="text-sm text-red-600 dark:text-red-400 text-center font-medium">{error}</p>
              </div>
            )}

            <Button 
              type="submit" 
              className="w-full h-11 bg-cyan-600 hover:bg-cyan-700 text-white dark:bg-cyan-600 dark:hover:bg-cyan-500 rounded-xl shadow-md transition-all duration-300 transform hover:-translate-y-0.5 active:translate-y-0 text-md font-semibold mt-6" 
              disabled={loading}
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <span className="h-4 w-4 rounded-full border-2 border-white border-t-transparent animate-spin"></span>
                  Logging in...
                </span>
              ) : "Sign In"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
