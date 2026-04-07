import { useAuth } from "@/context/AuthContext"
import { Button } from "@/components/ui/button"

export default function Navbar() {
  const { logout } = useAuth()

  return (
    <nav className="flex items-center justify-between p-4 bg-background border-b mb-4">
      <div className="font-bold text-xl text-primary">QuerySense</div>
      <Button variant="outline" onClick={logout}>
        Logout
      </Button>
    </nav>
  )
}
