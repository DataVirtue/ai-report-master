import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Label } from "@/components/ui/label"

const API_BASE_URL = import.meta.env.VITE_API_URL

export default function RegisterForm({ onLoginClick }: { onLoginClick: () => void }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const handleRegister = async (formData: FormData) => {
    setLoading(true)
    setError(null)
    setSuccess(false)

    const username = formData.get("username")
    const email = formData.get("email")
    const password = formData.get("password")

    try {
      const res = await fetch(API_BASE_URL + "/users/api/register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
      })

      const data = await res.json()

      if (!res.ok) {
        if (typeof data === 'object' && data !== null) {
          const errorMessages = Object.entries(data)
            .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
            .join(' | ')
          throw new Error(errorMessages || "Registration failed")
        }
        throw new Error(data.detail || "Registration failed")
      }

      setSuccess(true)
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
          <CardTitle>Register</CardTitle>
          {success && <CardDescription className="text-green-500">User created successfully! You can now login.</CardDescription>}
        </CardHeader>

        <CardContent>
          <form
            action={async (formData) => {
              await handleRegister(formData)
            }}
            className="space-y-4"
          >
            <div className="space-y-2">
              <Label htmlFor="username">Username</Label>
              <Input name="username" placeholder="Enter username" required />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input name="email" type="email" placeholder="Enter email" required />
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

            <Button type="submit" className="w-full" disabled={loading || success}>
              {loading ? "Registering..." : success ? "Registered!" : "Register"}
            </Button>
          </form>
          
          <div className="mt-4 text-center text-sm">
             Already have an account?{" "}
             <button type="button" onClick={onLoginClick} className="text-primary hover:underline">
               Login
             </button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
