import { ThemeToggle } from "./ThemeToggle";
import { Button } from "./ui/button";
import { Brain } from "lucide-react";

export default function Navbar() {

  return (
    <nav className="sticky top-0 z-50 glass border-b-0 backdrop-blur-xl shadow-sm">
      <div className="flex h-16 items-center justify-between px-6 max-w-7xl mx-auto">

        {/* Logo */}
        <div className="flex items-center gap-2 text-xl font-bold group cursor-pointer">
          <div className="flex items-center justify-center bg-cyan-600 dark:bg-cyan-500 w-8 h-8 rounded-lg shadow-sm group-hover:scale-105 transition-transform duration-300">
            <Brain className="text-white w-5 h-5" />
          </div>
          <span className="text-cyan-700 dark:text-cyan-400 tracking-tight drop-shadow-sm transition-colors">QuerySense</span>
        </div>

        {/* Links */}
        <div className="hidden md:flex items-center gap-2">
          {["Chat", "History", "Reports"].map((item) => (
            <button
              key={item}
              className="px-4 py-2 rounded-xl text-sm font-medium hover:bg-cyan-50 hover:text-cyan-700 dark:hover:bg-cyan-500/10 dark:hover:text-cyan-300 transition-all duration-300"
            >
              {item}
            </button>
          ))}
        </div>

        {/* Right */}
        <div className="flex items-center gap-3">
          <ThemeToggle />
          <Button size="sm" className="rounded-xl bg-cyan-600 hover:bg-cyan-700 text-white dark:bg-cyan-600 dark:hover:bg-cyan-500 shadow-sm transition-all text-sm font-semibold px-4">
            + New Chat
          </Button>
        </div>

      </div>
    </nav>
  )
}
