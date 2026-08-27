'use client';

import React from 'react';
import { Sparkles, GraduationCap, HeartHandshake, Users, Calendar, Award } from 'lucide-react';

export default function AlumniPortal() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-8">
      <header className="flex items-center justify-between border-b border-slate-800 pb-6 mb-8">
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-rose-500 to-amber-600 flex items-center justify-center text-white font-bold">
            <Sparkles className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Alumni & Mentorship Portal</h1>
            <p className="text-xs text-amber-400 font-medium">Alumni: David Miller ('22) | Sr. Software Engineer @ Meta</p>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h2 className="text-base font-bold text-white mb-4">Active Mentorship Matches</h2>
          <div className="space-y-4 text-xs">
            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
              <div>
                <div className="font-semibold text-white">Mentee: Alex Johnson</div>
                <div className="text-slate-400 mt-1">Focus: Systems Programming & Tech Interview Prep</div>
              </div>
              <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 font-semibold border border-emerald-500/20">
                Active Match
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
