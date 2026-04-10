import { useAuth } from "@/context/AuthContext"
import { Button } from "@/components/ui/button"
import { ModeToggle } from "@/components/ModeToggle"

export default function Navbar() {
  const { logout } = useAuth()

  return (
    <nav className="flex items-center justify-between p-4 bg-background border-b mb-4">
      <div className="font-bold text-xl text-primary">QuerySense</div>
      <div className="flex items-center gap-2">
        <ModeToggle />
        <Button variant="outline" onClick={logout}>
          Logout
        </Button>
      </div>
    </nav>
  )
}
