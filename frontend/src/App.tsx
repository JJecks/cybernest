import { useEffect, useState } from "react"
import axios from "axios"
import {
  BarChart, Bar, XAxis, YAxis, Tooltip,
  ResponsiveContainer, PieChart, Pie, Cell, Legend
} from "recharts"

const API = "http://127.0.0.1:8000/api"
const COLORS = ["#6366f1", "#22d3ee", "#f59e0b", "#10b981", "#ef4444", "#a78bfa"]

interface AppLog {
  id: number
  app_name: string
  window_title: string
  duration_seconds: number
  started_at: string
}

interface PrintLog {
  id: number
  printer_name: string
  document_name: string
  pages: number
  printed_at: string
}

interface BrowserLog {
  id: number
  browser: string
  url: string
  page_title: string
  visited_at: string
}

export default function App() {
  const [appLogs, setAppLogs] = useState<AppLog[]>([])
  const [printLogs, setPrintLogs] = useState<PrintLog[]>([])
  const [browserLogs, setBrowserLogs] = useState<BrowserLog[]>([])
  const [machines, setMachines] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = () => {
      Promise.all([
        axios.get(`${API}/logs/app/list/`),
        axios.get(`${API}/logs/print/list/`),
        axios.get(`${API}/logs/browser/list/`),
        axios.get(`${API}/machines/all/`),
      ]).then(([apps, prints, browsers, macs]) => {
        setAppLogs(apps.data)
        setPrintLogs(prints.data)
        setBrowserLogs(browsers.data)
        setMachines(macs.data)
        setLoading(false)
      })
    }

    fetchData()
    const interval = setInterval(fetchData, 30000)
    return () => clearInterval(interval)
  }, [])

  const appUsageMap: Record<string, number> = {}
  appLogs.forEach(log => {
    appUsageMap[log.app_name] = (appUsageMap[log.app_name] || 0) + log.duration_seconds
  })
  const appChartData = Object.entries(appUsageMap)
    .map(([name, secs]) => ({ name, minutes: Math.round(secs / 60) }))
    .sort((a, b) => b.minutes - a.minutes)
    .slice(0, 8)

  const totalPages = printLogs.reduce((sum, log) => sum + log.pages, 0)

  const browserMap: Record<string, number> = {}
  browserLogs.forEach(log => {
    browserMap[log.browser] = (browserMap[log.browser] || 0) + 1
  })
  const browserChartData = Object.entries(browserMap).map(([name, value]) => ({ name, value }))

  if (loading) return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <p className="text-indigo-400 text-xl animate-pulse">Loading CyberNest...</p>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-indigo-400">🖥️ CyberNest Dashboard</h1>
        <p className="text-gray-400 mt-1">
          Real-time computer usage monitoring
          <span className="ml-2 text-xs text-emerald-400 animate-pulse">● live</span>
        </p>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
          <p className="text-gray-400 text-sm">Total App Sessions</p>
          <p className="text-4xl font-bold text-indigo-400 mt-1">{appLogs.length}</p>
        </div>
        <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
          <p className="text-gray-400 text-sm">Pages Printed</p>
          <p className="text-4xl font-bold text-cyan-400 mt-1">{totalPages}</p>
        </div>
        <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
          <p className="text-gray-400 text-sm">Sites Visited</p>
          <p className="text-4xl font-bold text-emerald-400 mt-1">{browserLogs.length}</p>
        </div>
      </div>

      {/* Connected Machines */}
      <div className="bg-gray-900 rounded-xl p-5 border border-gray-800 mb-8">
        <h2 className="text-lg font-semibold mb-4 text-gray-200">🖥️ Connected PCs</h2>
        <div className="grid grid-cols-4 gap-3">
          {machines.map(m => {
            const lastSeen = m.last_seen ? new Date(m.last_seen) : null
            const isOnline = lastSeen && (Date.now() - lastSeen.getTime()) < 30000
            return (
              <div key={m.id} className="bg-gray-800 rounded-lg p-4 border border-gray-700">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-semibold text-gray-200">{m.name}</span>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${
                    isOnline ? 'bg-emerald-900 text-emerald-400' : 'bg-gray-700 text-gray-500'
                  }`}>
                    {isOnline ? '● Online' : '○ Offline'}
                  </span>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  {lastSeen ? `Last seen: ${lastSeen.toLocaleTimeString()}` : 'Never connected'}
                </p>
              </div>
            )
          })}
          {machines.length === 0 && (
            <p className="text-gray-500 text-sm col-span-4">No PCs registered yet</p>
          )}
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-2 gap-6 mb-8">
        <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
          <h2 className="text-lg font-semibold mb-4 text-gray-200">App Usage (minutes)</h2>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={appChartData}>
              <XAxis dataKey="name" tick={{ fill: "#9ca3af", fontSize: 11 }} />
              <YAxis tick={{ fill: "#9ca3af", fontSize: 11 }} />
              <Tooltip contentStyle={{ background: "#1f2937", border: "none" }} />
              <Bar dataKey="minutes" fill="#6366f1" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
          <h2 className="text-lg font-semibold mb-4 text-gray-200">Browser Usage</h2>
          {browserChartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie data={browserChartData} dataKey="value" nameKey="name"
                  cx="50%" cy="50%" outerRadius={90} label>
                  {browserChartData.map((_, i) => (
                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                  ))}
                </Pie>
                <Legend />
                <Tooltip contentStyle={{ background: "#1f2937", border: "none" }} />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-500 text-sm mt-8 text-center">No browser data yet</p>
          )}
        </div>
      </div>

      {/* Print Logs */}
      <div className="bg-gray-900 rounded-xl p-5 border border-gray-800 mb-6">
        <h2 className="text-lg font-semibold mb-4 text-gray-200">🖨️ Print Jobs</h2>
        {printLogs.length === 0 ? (
          <p className="text-gray-500 text-sm">No print jobs recorded yet</p>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="text-gray-400 border-b border-gray-800">
                <th className="text-left py-2">Document</th>
                <th className="text-left py-2">Printer</th>
                <th className="text-left py-2">Pages</th>
                <th className="text-left py-2">Time</th>
              </tr>
            </thead>
            <tbody>
              {printLogs.slice(0, 10).map(log => (
                <tr key={log.id} className="border-b border-gray-800 hover:bg-gray-800">
                  <td className="py-2 text-gray-300">{log.document_name}</td>
                  <td className="py-2 text-gray-300">{log.printer_name}</td>
                  <td className="py-2 text-cyan-400 font-bold">{log.pages}</td>
                  <td className="py-2 text-gray-500">{new Date(log.printed_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Recent App Activity */}
      <div className="bg-gray-900 rounded-xl p-5 border border-gray-800">
        <h2 className="text-lg font-semibold mb-4 text-gray-200">Recent App Activity</h2>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-gray-400 border-b border-gray-800">
              <th className="text-left py-2">App</th>
              <th className="text-left py-2">Window</th>
              <th className="text-left py-2">Duration</th>
              <th className="text-left py-2">Time</th>
            </tr>
          </thead>
          <tbody>
            {appLogs.slice(0, 10).map(log => (
              <tr key={log.id} className="border-b border-gray-800 hover:bg-gray-800">
                <td className="py-2 text-indigo-400 font-medium">{log.app_name}</td>
                <td className="py-2 text-gray-300 truncate max-w-xs">{log.window_title}</td>
                <td className="py-2 text-gray-300">{log.duration_seconds}s</td>
                <td className="py-2 text-gray-500">{new Date(log.started_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}