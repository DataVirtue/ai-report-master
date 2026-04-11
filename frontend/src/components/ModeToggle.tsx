import { Moon, Sun, Monitor } from "lucide-react"

import { Button } from "@/components/ui/button"
import { useTheme } from "@/context/ThemeContext"

export function ModeToggle() {
  const { theme, setTheme } = useTheme()

  const toggleTheme = () => {
    if (theme === "light") {
      setTheme("dark")
    } else if (theme === "dark") {
      setTheme("system")
    } else {
      setTheme("light")
    }
  }

  return (
    <Button variant="outline" size="icon" onClick={toggleTheme} className="w-10 h-10 relative">
      <Sun 
        className={`absolute h-[1.2rem] w-[1.2rem] transition-all duration-300 ${theme === 'light' ? 'rotate-0 scale-100' : 'rotate-90 scale-0'}`} 
      />
      <Moon 
        className={`absolute h-[1.2rem] w-[1.2rem] transition-all duration-300 ${theme === 'dark' ? 'rotate-0 scale-100' : 'rotate-90 scale-0'}`} 
      />
      <Monitor 
        className={`absolute h-[1.2rem] w-[1.2rem] transition-all duration-300 ${theme === 'system' ? 'rotate-0 scale-100' : 'rotate-90 scale-0'}`} 
      />
      <span className="sr-only">Toggle theme</span>
    </Button>
  )
}
