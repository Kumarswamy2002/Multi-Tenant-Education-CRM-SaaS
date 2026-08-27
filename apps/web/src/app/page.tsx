'use client';

import React, { useState } from 'react';
import { 
  Building2, Users, Target, FileText, UserCheck, HeartHandshake, 
  Briefcase, GraduationCap, ArrowRight, Shield, Activity, Sparkles, CheckCircle2
} from 'lucide-react';

export default function LandingPage() {
  const [activeTab, setActiveTab] = useState<'overview' | 'lifecycle' | 'architecture'>('overview');

  const lifecycleSteps = [
    { title: 'Prospect', desc: 'Inbound leads, campaigns & scoring', icon: Target, color: 'text-blue-500 bg-blue-50' },
    { title: 'Counseling', desc: 'Interviews, interest mapping & recommendations', icon: Users, color: 'text-indigo-500 bg-indigo-50' },
    { title: 'Application', desc: 'Dynamic forms & document verification', icon: FileText, color: 'text-purple-500 bg-purple-50' },
    { title: 'Admission', desc: 'Eligibility rules, offer letters & seat allocation', icon: UserCheck, color: 'text-amber-500 bg-amber-50' },
    { title: 'Student 360', desc: 'Academic progress, engagement & unified timeline', icon: GraduationCap, color: 'text-emerald-500 bg-emerald-50' },
    { title: 'Student Success', desc: 'Risk indicators & advisor interventions', icon: HeartHandshake, color: 'text-teal-500 bg-teal-50' },
    { title: 'Career', desc: 'Skill matrix, resumes & recruitment offers', icon: Briefcase, color: 'text-cyan-500 bg-cyan-50' },
    { title: 'Alumni', desc: 'Mentorship, networking & institutional giving', icon: Sparkles, color: 'text-rose-500 bg-rose-50' }
  ];

  return (
    <div className="min-h-screen flex flex-col bg-slate-900 text-white font-sans selection:bg-sky-500 selection:text-white">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/20">
              <Building2 className="h-6 w-6 text-white" />
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                CampusSphere
              </span>
              <span className="ml-2 text-xs font-semibold px-2 py-0.5 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20">
                Enterprise SaaS
              </span>
            </div>
          </div>

          <nav className="hidden md:flex items-center space-x-8 text-sm font-medium text-slate-300">
            <button onClick={() => setActiveTab('overview')} className={`hover:text-white transition ${activeTab === 'overview' ? 'text-sky-400 font-semibold' : ''}`}>Overview</button>
            <button onClick={() => setActiveTab('lifecycle')} className={`hover:text-white transition ${activeTab === 'lifecycle' ? 'text-sky-400 font-semibold' : ''}`}>Learner Lifecycle</button>
            <button onClick={() => setActiveTab('architecture')} className={`hover:text-white transition ${activeTab === 'architecture' ? 'text-sky-400 font-semibold' : ''}`}>Architecture</button>
          </nav>

          <div className="flex items-center space-x-4">
            <a href="/login" className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-white transition">
              Sign In
            </a>
            <a href="/dashboard" className="px-5 py-2.5 text-sm font-semibold rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 transition shadow-lg shadow-sky-500/25 flex items-center space-x-2">
              <span>Admin Workspace</span>
              <ArrowRight className="h-4 w-4" />
            </a>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative pt-20 pb-16 overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-sky-900/30 via-slate-900 to-slate-950 pointer-events-none"></div>
        <div className="max-w-7xl mx-auto px-6 relative z-10 text-center">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-slate-800/80 border border-slate-700 text-xs font-medium text-sky-400 mb-8">
            <Activity className="h-3.5 w-3.5" />
            <span>Multi-Tenant Education Relationship Management Platform</span>
          </div>

          <h1 className="text-5xl md:text-6xl font-extrabold text-white tracking-tight leading-tight max-w-4xl mx-auto">
            Unified 360° Relationship View Across the <span className="bg-gradient-to-r from-sky-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">Complete Education Lifecycle</span>
          </h1>

          <p className="mt-6 text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
            CampusSphere CRM connects prospective leads, admissions counseling, applications, active student success, career placements, and alumni engagement into a single multi-tenant SaaS platform.
          </p>

          <div className="mt-10 flex items-center justify-center space-x-4">
            <a href="/dashboard" className="px-8 py-4 text-base font-semibold rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 transition shadow-xl shadow-sky-500/25 flex items-center space-x-3">
              <span>Launch Admin Dashboard</span>
              <ArrowRight className="h-5 w-5" />
            </a>
            <a href="/docs" className="px-8 py-4 text-base font-semibold rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition">
              Explore API Docs
            </a>
          </div>

          {/* Quick Metrics */}
          <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            <div className="p-6 rounded-2xl bg-slate-800/50 border border-slate-800 text-center">
              <div className="text-3xl font-extrabold text-white">70,000+</div>
              <div className="text-xs text-slate-400 mt-1 uppercase font-semibold">Lines of Code</div>
            </div>
            <div className="p-6 rounded-2xl bg-slate-800/50 border border-slate-800 text-center">
              <div className="text-3xl font-extrabold text-sky-400">100%</div>
              <div className="text-xs text-slate-400 mt-1 uppercase font-semibold">Tenant Data Isolation</div>
            </div>
            <div className="p-6 rounded-2xl bg-slate-800/50 border border-slate-800 text-center">
              <div className="text-3xl font-extrabold text-indigo-400">12</div>
              <div className="text-xs text-slate-400 mt-1 uppercase font-semibold">Non-Duplication Rules</div>
            </div>
            <div className="p-6 rounded-2xl bg-slate-800/50 border border-slate-800 text-center">
              <div className="text-3xl font-extrabold text-emerald-400">10</div>
              <div className="text-xs text-slate-400 mt-1 uppercase font-semibold">Phased Modules</div>
            </div>
          </div>
        </div>
      </section>

      {/* Lifecycle Section */}
      <section className="py-16 bg-slate-950 border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl font-bold text-white">The Connected Learner Timeline</h2>
            <p className="text-slate-400 mt-3">From prospect capture to alumni giving — managed in one centralized relationship graph.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {lifecycleSteps.map((step, idx) => {
              const Icon = step.icon;
              return (
                <div key={idx} className="p-6 rounded-2xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition group">
                  <div className={`h-12 w-12 rounded-xl flex items-center justify-center mb-4 ${step.color}`}>
                    <Icon className="h-6 w-6" />
                  </div>
                  <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Step 0{idx + 1}</div>
                  <h3 className="text-lg font-bold text-white mt-1 group-hover:text-sky-400 transition">{step.title}</h3>
                  <p className="text-sm text-slate-400 mt-2 leading-relaxed">{step.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-800 bg-slate-950 py-8">
        <div className="max-w-7xl mx-auto px-6 text-center text-xs text-slate-500">
          <p>© 2026 CampusSphere CRM. Multi-Tenant Education SaaS Architecture.</p>
        </div>
      </footer>
    </div>
  );
}
