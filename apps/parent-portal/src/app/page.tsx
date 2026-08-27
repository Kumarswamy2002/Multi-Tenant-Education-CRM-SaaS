'use client';

import React from 'react';
import { Shield, Heart, GraduationCap, AlertCircle, CheckCircle2, Bell } from 'lucide-react';

export default function ParentPortal() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-8">
      <header className="flex items-center justify-between border-b border-slate-800 pb-6 mb-8">
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-rose-500 to-pink-600 flex items-center justify-center text-white font-bold">
            <Heart className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Parent & Guardian Portal</h1>
            <p className="text-xs text-rose-400 font-medium">Guardian Account: Robert Johnson | Linked Student: Alex Johnson</p>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h2 className="text-base font-bold text-white mb-4">Student Overview: Alex Johnson</h2>
          <div className="space-y-3 text-xs">
            <div className="flex justify-between py-2 border-b border-slate-800">
              <span className="text-slate-400">Enrolled Program</span>
              <span className="font-semibold text-white">Computer Science B.S.</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-800">
              <span className="text-slate-400">Attendance Rate</span>
              <span className="font-semibold text-emerald-400">96.5%</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-slate-400">Tuition Status</span>
              <span className="font-semibold text-emerald-400">Paid in Full</span>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h2 className="text-base font-bold text-white mb-4">Recent Communications & Alerts</h2>
          <div className="space-y-3 text-xs">
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-start space-x-3">
              <Bell className="h-4 w-4 text-sky-400 mt-0.5" />
              <div>
                <div className="font-semibold text-white">Midterm Exam Schedule Issued</div>
                <div className="text-slate-400 mt-1">Midterm exams will be conducted between October 12 - 16.</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
