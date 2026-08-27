'use client';

import React, { useState } from 'react';
import { 
  Building2, Users, Target, FileText, UserCheck, HeartHandshake, 
  Briefcase, GraduationCap, ArrowRight, Shield, Activity, Plus, Search, Filter, CheckCircle2, Clock
} from 'lucide-react';

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<'overview' | 'leads' | 'admissions' | 'students' | 'cases'>('overview');

  return (
    <div className="min-h-screen flex bg-slate-900 text-slate-100 font-sans">
      {/* Sidebar Navigation */}
      <aside className="w-64 border-r border-slate-800 bg-slate-950 p-6 flex flex-col justify-between">
        <div>
          <div className="flex items-center space-x-3 mb-10">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/20">
              <Building2 className="h-6 w-6 text-white" />
            </div>
            <div>
              <span className="text-lg font-bold text-white tracking-tight">CampusSphere</span>
              <span className="block text-xs text-sky-400 font-medium">Harvard University</span>
            </div>
          </div>

          <nav className="space-y-2 text-sm font-medium">
            <button
              onClick={() => setActiveTab('overview')}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition ${activeTab === 'overview' ? 'bg-sky-500/10 text-sky-400 font-semibold border border-sky-500/20' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'}`}
            >
              <Activity className="h-4 w-4" />
              <span>Executive 360</span>
            </button>
            <button
              onClick={() => setActiveTab('leads')}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition ${activeTab === 'leads' ? 'bg-sky-500/10 text-sky-400 font-semibold border border-sky-500/20' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'}`}
            >
              <Target className="h-4 w-4" />
              <span>Lead CRM</span>
            </button>
            <button
              onClick={() => setActiveTab('admissions')}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition ${activeTab === 'admissions' ? 'bg-sky-500/10 text-sky-400 font-semibold border border-sky-500/20' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'}`}
            >
              <FileText className="h-4 w-4" />
              <span>Admissions Pipeline</span>
            </button>
            <button
              onClick={() => setActiveTab('students')}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition ${activeTab === 'students' ? 'bg-sky-500/10 text-sky-400 font-semibold border border-sky-500/20' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'}`}
            >
              <GraduationCap className="h-4 w-4" />
              <span>Student 360</span>
            </button>
            <button
              onClick={() => setActiveTab('cases')}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition ${activeTab === 'cases' ? 'bg-sky-500/10 text-sky-400 font-semibold border border-sky-500/20' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'}`}
            >
              <HeartHandshake className="h-4 w-4" />
              <span>Support Cases</span>
            </button>
          </nav>
        </div>

        <div className="border-t border-slate-800 pt-6">
          <div className="flex items-center space-x-3">
            <div className="h-9 w-9 rounded-full bg-slate-800 flex items-center justify-center font-bold text-sky-400 text-sm">
              AD
            </div>
            <div>
              <div className="text-sm font-semibold text-white">Institution Admin</div>
              <div className="text-xs text-slate-500">admin@harvard.edu</div>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 p-8 overflow-y-auto">
        <header className="flex items-center justify-between mb-8 pb-6 border-b border-slate-800">
          <div>
            <h1 className="text-2xl font-bold text-white capitalize">{activeTab} Workspace</h1>
            <p className="text-xs text-slate-400 mt-1">Tenant ID: harvard-univ-tenant-001 | Multi-Tenant Data Context Active</p>
          </div>

          <div className="flex items-center space-x-4">
            <div className="relative">
              <Search className="h-4 w-4 absolute left-3 top-3 text-slate-500" />
              <input
                type="text"
                placeholder="Global Search (Students, Leads, Cases)..."
                className="pl-9 pr-4 py-2 text-xs rounded-xl bg-slate-800 border border-slate-700 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-500 w-72 transition"
              />
            </div>
            <button className="px-4 py-2 text-xs font-semibold rounded-xl bg-sky-500 hover:bg-sky-400 text-white transition flex items-center space-x-2">
              <Plus className="h-3.5 w-3.5" />
              <span>New Record</span>
            </button>
          </div>
        </header>

        {/* Overview Widgets */}
        {activeTab === 'overview' && (
          <div className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="p-6 rounded-2xl bg-slate-950 border border-slate-800">
                <div className="flex items-center justify-between text-slate-400 text-xs font-medium">
                  <span>Total Active Leads</span>
                  <Target className="h-4 w-4 text-sky-400" />
                </div>
                <div className="text-3xl font-extrabold text-white mt-2">1,248</div>
                <div className="text-xs text-emerald-400 mt-2 flex items-center space-x-1">
                  <span>+18.4% this month</span>
                </div>
              </div>

              <div className="p-6 rounded-2xl bg-slate-950 border border-slate-800">
                <div className="flex items-center justify-between text-slate-400 text-xs font-medium">
                  <span>Submitted Applications</span>
                  <FileText className="h-4 w-4 text-indigo-400" />
                </div>
                <div className="text-3xl font-extrabold text-white mt-2">482</div>
                <div className="text-xs text-emerald-400 mt-2 flex items-center space-x-1">
                  <span>84 pending verification</span>
                </div>
              </div>

              <div className="p-6 rounded-2xl bg-slate-950 border border-slate-800">
                <div className="flex items-center justify-between text-slate-400 text-xs font-medium">
                  <span>Active Enrolled Students</span>
                  <GraduationCap className="h-4 w-4 text-emerald-400" />
                </div>
                <div className="text-3xl font-extrabold text-white mt-2">3,890</div>
                <div className="text-xs text-slate-400 mt-2">Across 14 Departments</div>
              </div>

              <div className="p-6 rounded-2xl bg-slate-950 border border-slate-800">
                <div className="flex items-center justify-between text-slate-400 text-xs font-medium">
                  <span>Open Support Tickets</span>
                  <HeartHandshake className="h-4 w-4 text-rose-400" />
                </div>
                <div className="text-3xl font-extrabold text-white mt-2">23</div>
                <div className="text-xs text-rose-400 mt-2">2 high priority cases</div>
              </div>
            </div>

            {/* Recent CRM Timeline Events */}
            <div className="p-6 rounded-2xl bg-slate-950 border border-slate-800">
              <h2 className="text-lg font-bold text-white mb-4">Live Institutional Timeline</h2>
              <div className="space-y-4">
                <div className="flex items-start space-x-4 p-4 rounded-xl bg-slate-900 border border-slate-800">
                  <div className="h-8 w-8 rounded-full bg-emerald-500/10 text-emerald-400 flex items-center justify-center text-xs font-bold mt-0.5">
                    <CheckCircle2 className="h-4 w-4" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-semibold text-white">Enrollment Completed: Alex Johnson</span>
                      <span className="text-xs text-slate-500">10 mins ago</span>
                    </div>
                    <p className="text-xs text-slate-400 mt-1">Applicant converted to Student ID STU-84920. Program: B.S. Computer Science.</p>
                  </div>
                </div>

                <div className="flex items-start space-x-4 p-4 rounded-xl bg-slate-900 border border-slate-800">
                  <div className="h-8 w-8 rounded-full bg-sky-500/10 text-sky-400 flex items-center justify-center text-xs font-bold mt-0.5">
                    <Clock className="h-4 w-4" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-semibold text-white">Counseling Session Recorded: Sarah Connor</span>
                      <span className="text-xs text-slate-500">45 mins ago</span>
                    </div>
                    <p className="text-xs text-slate-400 mt-1">Counselor recommended M.S. Data Science program. Academic background verified.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab !== 'overview' && (
          <div className="p-12 text-center rounded-2xl bg-slate-950 border border-slate-800 text-slate-400">
            <h3 className="text-lg font-semibold text-white capitalize">{activeTab} Workspace Active</h3>
            <p className="text-xs text-slate-500 mt-2">Connected live to FastAPI backend services & tenant context contextvar.</p>
          </div>
        )}
      </main>
    </div>
  );
}
