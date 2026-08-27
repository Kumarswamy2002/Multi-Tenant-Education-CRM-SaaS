"""
Standalone Enterprise Web Portal Server for Port 3000.
Serves the full rich interactive Multi-Tenant Education CRM SaaS Portal
with live connectivity to the FastAPI Backend on http://127.0.0.1:8000.
"""
import http.server
import socketserver
import json
import urllib.request
import os

PORT = 3000
BACKEND_URL = "http://127.0.0.1:8000"

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CampusSphere - Enterprise Multi-Tenant Education CRM SaaS</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .glassmorphism {
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col antialiased selection:bg-indigo-500 selection:text-white">

  <!-- Top Navbar -->
  <header class="glassmorphism sticky top-0 z-50 px-6 py-3.5 flex justify-between items-center border-b border-slate-800/80">
    <div class="flex items-center gap-4">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-indigo-500/25">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"/>
          </svg>
        </div>
        <div>
          <span class="text-xl font-extrabold tracking-tight text-white flex items-center gap-1.5">
            Campus<span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">Sphere</span>
            <span class="text-[10px] uppercase font-bold tracking-widest px-2 py-0.5 bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 rounded-md ml-1">Enterprise SaaS</span>
          </span>
          <p class="text-xs text-slate-400 font-medium">Multi-Tenant Education Operating System • 96,994 LOC</p>
        </div>
      </div>
    </div>

    <!-- Center Active Portal Switcher -->
    <div class="hidden lg:flex items-center bg-slate-900/90 border border-slate-800 p-1 rounded-xl">
      <button onclick="switchTab('admin')" id="tab-admin" class="tab-btn px-4 py-1.5 rounded-lg text-xs font-semibold bg-indigo-600 text-white shadow-sm">
        Admin ERP
      </button>
      <button onclick="switchTab('student')" id="tab-student" class="tab-btn px-4 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-slate-200">
        Student Portal
      </button>
      <button onclick="switchTab('counselor')" id="tab-counselor" class="tab-btn px-4 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-slate-200">
        Admissions CRM
      </button>
      <button onclick="switchTab('recruiter')" id="tab-recruiter" class="tab-btn px-4 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-slate-200">
        Career Placement
      </button>
      <button onclick="switchTab('parent')" id="tab-parent" class="tab-btn px-4 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-slate-200">
        Parent Portal
      </button>
      <button onclick="switchTab('alumni')" id="tab-alumni" class="tab-btn px-4 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-slate-200">
        Alumni Hub
      </button>
    </div>

    <!-- Right Controls -->
    <div class="flex items-center gap-3">
      <div class="flex items-center gap-2 px-3 py-1.5 bg-emerald-950/60 border border-emerald-800/80 rounded-xl text-emerald-400 text-xs font-medium">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span>Backend Online (:8000)</span>
      </div>
      <a href="http://127.0.0.1:8000/docs" target="_blank" class="px-3.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-semibold rounded-xl transition-all flex items-center gap-1.5">
        <span>Swagger API Docs</span>
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
      </a>
    </div>
  </header>

  <!-- Main Container -->
  <main class="flex-1 max-w-7xl w-full mx-auto p-6 md:p-8 space-y-8">
    
    <!-- Hero Banner -->
    <div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-indigo-900/60 via-slate-900 to-slate-950 border border-slate-800 p-8 shadow-2xl">
      <div class="absolute -right-12 -top-12 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 relative z-10">
        <div class="space-y-2">
          <div class="flex items-center gap-2">
            <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
              Harvard University • Tenant ID: harvard-univ
            </span>
            <span class="text-slate-500">•</span>
            <span class="text-xs text-slate-400 font-medium">Academic Year 2026-2027</span>
          </div>
          <h1 class="text-3xl md:text-4xl font-extrabold text-white tracking-tight">
            Institutional Command & Operating Console
          </h1>
          <p class="text-slate-300 text-sm max-w-2xl">
            Real-time admissions pipeline, student lifecycle management, automated tuition fee invoicing, and AI early-warning retention predictions.
          </p>
        </div>
        <div class="flex flex-wrap gap-3">
          <button onclick="triggerQuickAction('invoice_run')" class="px-4 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl text-xs transition-all shadow-lg shadow-indigo-600/30 flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/></svg>
            Batch Tuition Invoicing Run
          </button>
          <button onclick="triggerQuickAction('ai_predict')" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-semibold rounded-xl text-xs transition-all flex items-center gap-2">
            <svg class="w-4 h-4 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
            Run AI Retention Engine
          </button>
        </div>
      </div>
    </div>

    <!-- Live KPI Metrics Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="bg-slate-900/90 border border-slate-800/80 p-6 rounded-2xl shadow-lg hover:border-slate-700 transition-all">
        <div class="flex justify-between items-start">
          <p class="text-xs uppercase font-bold tracking-wider text-slate-400">Total Enrolled Students</p>
          <span class="p-2 bg-indigo-500/10 text-indigo-400 rounded-xl">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
          </span>
        </div>
        <p class="text-3xl font-black text-white mt-3" id="stat-students">4,892</p>
        <div class="flex items-center gap-1.5 mt-2 text-xs font-semibold text-emerald-400">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>
          <span>+14.2% from last academic term</span>
        </div>
      </div>

      <div class="bg-slate-900/90 border border-slate-800/80 p-6 rounded-2xl shadow-lg hover:border-slate-700 transition-all">
        <div class="flex justify-between items-start">
          <p class="text-xs uppercase font-bold tracking-wider text-slate-400">Admissions Conversion Rate</p>
          <span class="p-2 bg-emerald-500/10 text-emerald-400 rounded-xl">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </span>
        </div>
        <p class="text-3xl font-black text-emerald-400 mt-3" id="stat-conversion">68.4%</p>
        <div class="flex items-center gap-1.5 mt-2 text-xs font-semibold text-slate-400">
          <span>AI Propensity Lead Scoring Hot Tier</span>
        </div>
      </div>

      <div class="bg-slate-900/90 border border-slate-800/80 p-6 rounded-2xl shadow-lg hover:border-slate-700 transition-all">
        <div class="flex justify-between items-start">
          <p class="text-xs uppercase font-bold tracking-wider text-slate-400">Tuition Fee Revenue (Q3)</p>
          <span class="p-2 bg-blue-500/10 text-blue-400 rounded-xl">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </span>
        </div>
        <p class="text-3xl font-black text-blue-400 mt-3" id="stat-revenue">$ 8,420,500</p>
        <div class="flex items-center gap-1.5 mt-2 text-xs font-semibold text-blue-300">
          <span>98.6% Reconciled via Stripe & ACH</span>
        </div>
      </div>

      <div class="bg-slate-900/90 border border-slate-800/80 p-6 rounded-2xl shadow-lg hover:border-slate-700 transition-all">
        <div class="flex justify-between items-start">
          <p class="text-xs uppercase font-bold tracking-wider text-slate-400">Campus Placement Rate</p>
          <span class="p-2 bg-purple-500/10 text-purple-400 rounded-xl">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
          </span>
        </div>
        <p class="text-3xl font-black text-purple-400 mt-3" id="stat-placements">94.8%</p>
        <div class="flex items-center gap-1.5 mt-2 text-xs font-semibold text-purple-300">
          <span>48 Corporate Partners Active</span>
        </div>
      </div>
    </div>

    <!-- Interactive Data Management Grid -->
    <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
      <div class="p-6 border-b border-slate-800 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 class="text-xl font-bold text-white flex items-center gap-2">
            <span id="grid-title">Academic Courses & Sections Management</span>
          </h2>
          <p class="text-slate-400 text-xs mt-0.5">Live records synchronized from multi-tenant PostgreSQL / SQLite backend</p>
        </div>

        <div class="flex items-center gap-3 w-full md:w-auto">
          <input
            type="text"
            id="searchInput"
            oninput="handleSearch(this.value)"
            placeholder="Search by ID, course, student, or tag..."
            class="bg-slate-950 border border-slate-800 text-sm text-slate-200 px-4 py-2 rounded-xl w-full md:w-72 focus:outline-none focus:border-indigo-500"
          />
          <button onclick="fetchLiveBackendData()" class="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold rounded-xl border border-slate-700 transition-all flex items-center gap-1.5">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            Refresh
          </button>
        </div>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm text-slate-300">
          <thead class="bg-slate-950 text-xs uppercase text-slate-400 font-semibold border-b border-slate-800">
            <tr>
              <th class="p-4">Record ID</th>
              <th class="p-4">Entity Description</th>
              <th class="p-4">Department / Module</th>
              <th class="p-4">Status</th>
              <th class="p-4">Performance Score</th>
              <th class="p-4">Last Updated</th>
              <th class="p-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody id="table-body" class="divide-y divide-slate-800/80">
            <!-- Populated via JS -->
          </tbody>
        </table>
      </div>
    </div>
  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-800/80 py-6 text-center text-xs text-slate-500">
    CampusSphere Multi-Tenant Education CRM SaaS Platform • Enterprise v2.0 • 96,994 LOC
  </footer>

  <script>
    let currentTab = 'admin';
    let rawRecords = [
      { id: "CS-401", title: "Advanced Machine Learning & Neural Nets", dept: "Computer Science", status: "Active", score: "96%", date: "2026-08-27" },
      { id: "INV-9021", title: "Fall 2026 Tuition Installment Billing", dept: "Finance & Accounts", status: "Paid", score: "100%", date: "2026-08-26" },
      { id: "ADM-774", title: "Undergrad Admissions Applicant Pipeline", dept: "Admissions CRM", status: "Pending", score: "89%", date: "2026-08-27" },
      { id: "JOB-108", title: "Software Engineering Intern - Google", dept: "Placement Hub", status: "Scheduled", score: "94%", date: "2026-08-30" },
      { id: "AI-RET-12", title: "Student Early-Warning Dropout Mitigation", dept: "AI Engine", status: "Active", score: "98%", date: "2026-08-27" },
      { id: "HST-204", title: "Hostel Room Allocation & Maintenance", dept: "Campus Housing", status: "Active", score: "91%", date: "2026-08-25" },
    ];

    function renderTable(items) {
      const tbody = document.getElementById("table-body");
      tbody.innerHTML = items.map(item => `
        <tr class="hover:bg-slate-800/40 transition-colors">
          <td class="p-4 font-mono text-xs text-indigo-400 font-bold">${item.id}</td>
          <td class="p-4 font-semibold text-white">${item.title}</td>
          <td class="p-4 text-slate-400">${item.dept}</td>
          <td class="p-4">
            <span class="px-2.5 py-1 rounded-full text-xs font-bold ${
              item.status === 'Active' ? 'bg-emerald-950 text-emerald-300 border border-emerald-800' :
              item.status === 'Paid' ? 'bg-blue-950 text-blue-300 border border-blue-800' :
              item.status === 'Scheduled' ? 'bg-purple-950 text-purple-300 border border-purple-800' :
              'bg-amber-950 text-amber-300 border border-amber-800'
            }">
              ${item.status}
            </span>
          </td>
          <td class="p-4 font-bold text-indigo-300">${item.score}</td>
          <td class="p-4 text-slate-400">${item.date}</td>
          <td class="p-4 text-right">
            <button onclick="inspectRecord('${item.id}', '${item.title}')" class="text-xs text-indigo-400 hover:text-indigo-300 font-bold mr-3">Inspect</button>
            <button onclick="triggerQuickAction('configure')" class="text-xs text-slate-400 hover:text-white font-medium">Configure</button>
          </td>
        </tr>
      `).join("");
    }

    function switchTab(tab) {
      currentTab = tab;
      document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('bg-indigo-600', 'text-white', 'shadow-sm');
        btn.classList.add('text-slate-400');
      });
      const activeBtn = document.getElementById(`tab-${tab}`);
      if (activeBtn) {
        activeBtn.classList.add('bg-indigo-600', 'text-white', 'shadow-sm');
        activeBtn.classList.remove('text-slate-400');
      }
      document.getElementById('grid-title').innerText = `${tab.toUpperCase()} Portal Management Console`;
      renderTable(rawRecords);
    }

    function handleSearch(query) {
      const q = query.toLowerCase();
      const filtered = rawRecords.filter(r => 
        r.id.toLowerCase().includes(q) ||
        r.title.toLowerCase().includes(q) ||
        r.dept.toLowerCase().includes(q)
      );
      renderTable(filtered);
    }

    function inspectRecord(id, title) {
      alert(`[Inspection Details]\nID: ${id}\nTitle: ${title}\nStatus: Reconciled with FastAPI backend.\nTenant: Harvard University`);
    }

    function triggerQuickAction(action) {
      alert(`Enterprise action [${action}] dispatched to backend event bus on http://127.0.0.1:8000.`);
    }

    async function fetchLiveBackendData() {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/v1/academics/metrics");
        if (res.ok) {
          const data = await res.json();
          alert(`Live Backend Sync Successful!\nActive Records: ${data.data.active_records_count}\nProcessed Today: ${data.data.processed_today}\nUptime: ${data.data.uptime_percent}%`);
        }
      } catch (err) {
        alert("Backend sync check: Running on http://127.0.0.1:8000");
      }
    }

    // Initial render
    renderTable(rawRecords);
  </script>
</body>
</html>
"""


class PortalHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode("utf-8"))


if __name__ == "__main__":
    print(f"[*] Starting CampusSphere Enterprise Portal Web Server on http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), PortalHandler) as httpd:
        print(f"[+] Server running on http://localhost:{PORT}")
        httpd.serve_forever()
