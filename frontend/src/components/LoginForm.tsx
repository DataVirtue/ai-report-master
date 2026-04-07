import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
const API_BASE_URL = import.meta.env.VITE_API_URL
import { useAuth } from "@/context/AuthContext"

export default function LoginForm({ onRegisterClick }: { onRegisterClick?: () => void }) {
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
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted">
      <Card className="w-[350px] shadow-lg">
        <CardHeader>
          <CardTitle>Login</CardTitle>
        </CardHeader>

        <CardContent>
          <form
            action={async (formData) => {
              await handleLogin(formData)
            }}
            className="space-y-4"
          >
            <div className="space-y-2">
              <Label htmlFor="username">Username</Label>
              <Input name="username" placeholder="Enter username" required />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                name="password"
                type="password"
                placeholder="Enter password"
                required
              />
            </div>

            {error && (
              <p className="text-sm text-red-500">{error}</p>
            )}

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Logging in..." : "Login"}
            </Button>
          </form>

          <div className="mt-4 text-center text-sm">
            Don't have an account?{" "}
            <button type="button" onClick={onRegisterClick} className="text-primary hover:underline">
              Register
            </button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
