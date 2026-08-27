'use client';

import React from 'react';
import { GraduationCap, BookOpen, CheckCircle2, FileText, Briefcase, Award, HeartHandshake } from 'lucide-react';

export default function StudentPortal() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-8">
      <header className="flex items-center justify-between border-b border-slate-800 pb-6 mb-8">
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-600 flex items-center justify-center text-white font-bold">
            <GraduationCap className="h-6 w-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Student Self-Service Portal</h1>
            <p className="text-xs text-emerald-400 font-medium">Student ID: STU-84920 | Program: Computer Science B.S.</p>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <div className="text-xs font-medium text-slate-400">Current Cumulative GPA</div>
          <div className="text-3xl font-extrabold text-white mt-2">3.84 / 4.0</div>
          <div className="text-xs text-emerald-400 mt-2">Academic Standing: Dean's List</div>
        </div>
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <div className="text-xs font-medium text-slate-400">Degree Credits Earned</div>
          <div className="text-3xl font-extrabold text-white mt-2">48 / 120</div>
          <div className="text-xs text-slate-400 mt-2">Expected Graduation: Spring 2028</div>
        </div>
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <div className="text-xs font-medium text-slate-400">Support & Mentorship</div>
          <div className="text-3xl font-extrabold text-emerald-400 mt-2">1 Advisor</div>
          <div className="text-xs text-slate-400 mt-2">Assigned Mentor: Dr. Emily Watson</div>
        </div>
      </div>

      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
        <h2 className="text-lg font-bold text-white mb-4">My Timeline & Milestone Roadmap</h2>
        <div className="space-y-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <CheckCircle2 className="h-5 w-5 text-emerald-400" />
              <div>
                <div className="font-semibold text-white">Fall 2026 Course Registration</div>
                <div className="text-slate-400">CS-101 Data Structures, CS-102 Algorithms, MATH-201 Linear Algebra</div>
              </div>
            </div>
            <span className="text-emerald-400 font-semibold">Completed</span>
          </div>
        </div>
      </div>
    </div>
  );
}
