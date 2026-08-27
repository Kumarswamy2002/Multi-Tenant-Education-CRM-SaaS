'use client';

import React from 'react';
import { Briefcase, Building, Plus, Users, FileText, CheckCircle2 } from 'lucide-react';

export default function EmployerPortal() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-8">
      <header className="flex items-center justify-between border-b border-slate-800 pb-6 mb-8">
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-white font-bold">
            <Briefcase className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Employer Recruitment Portal</h1>
            <p className="text-xs text-cyan-400 font-medium">Organization: Google Inc. | Recruiter: Tech Recruitment Team</p>
          </div>
        </div>

        <button className="px-4 py-2 text-xs font-semibold rounded-xl bg-cyan-500 hover:bg-cyan-400 text-white transition flex items-center space-x-2">
          <Plus className="h-3.5 w-3.5" />
          <span>Post Campus Opportunity</span>
        </button>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h2 className="text-base font-bold text-white mb-4">Active Campus Postings</h2>
          <div className="space-y-4 text-xs">
            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
              <div>
                <div className="font-semibold text-white">Software Engineer Intern - Summer 2027</div>
                <div className="text-slate-400 mt-1">Location: Mountain View, CA | Full-Time Internship</div>
              </div>
              <span className="px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-400 font-semibold border border-cyan-500/20">
                42 Applicants
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
