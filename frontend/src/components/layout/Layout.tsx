import { Outlet, Link, useLocation } from 'react-router-dom'
import { cn } from '@/utils/cn'
import { Film, Settings } from 'lucide-react'

export function Layout() {
  const location = useLocation()

  const navItems = [
    { href: '/projects', label: '项目', icon: Film },
    { href: '/settings', label: '设置', icon: Settings },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-8">
              <Link to="/" className="flex items-center gap-2 font-semibold text-lg">
                <Film className="w-6 h-6 text-primary" />
                <span>ShortPlay</span>
              </Link>
              <nav className="flex gap-1">
                {navItems.map((item) => {
                  const isActive = location.pathname.startsWith(item.href)
                  return (
                    <Link
                      key={item.href}
                      to={item.href}
                      className={cn(
                        'flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                        isActive
                          ? 'bg-primary text-primary-foreground'
                          : 'text-muted-foreground hover:bg-gray-100'
                      )}
                    >
                      <item.icon className="w-4 h-4" />
                      {item.label}
                    </Link>
                  )
                })}
              </nav>
            </div>
          </div>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  )
}
