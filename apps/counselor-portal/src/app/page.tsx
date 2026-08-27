'use client';

import React, { useState } from 'react';
import { Users, PhoneCall, Calendar, Target, CheckCircle2, Clock, Star, MessageSquare } from 'lucide-react';

export default function CounselorWorkspace() {
  const [assignedLeads] = useState([
    { id: '1', name: 'Alex Johnson', program: 'Computer Science B.S.', score: 85, stage: 'Counseling Scheduled', date: 'Today, 2:00 PM' },
    { id: '2', name: 'Sarah Connor', program: 'Data Science M.S.', score: 92, stage: 'Application Review', date: 'Tomorrow, 10:00 AM' },
    { id: '3', name: 'Michael Scott', program: 'Business Admin MBA', score: 68, stage: 'Initial Inquiry', date: 'Aug 29, 4:00 PM' }
  ]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-8">
      <header className="flex items-center justify-between border-b border-slate-800 pb-6 mb-8">
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold">
            <Users className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Admissions Counselor Portal</h1>
            <p className="text-xs text-indigo-400 font-medium">Counselor ID: CNS-8821 | Active Lead Queue: 12</p>
          </div>
        </div>

        <div className="flex items-center space-x-4 text-xs">
          <span className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300">
            Assigned Capacity: <strong className="text-white">12 / 100</strong>
          </span>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Lead Queue */}
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-base font-bold text-white mb-4">Assigned Prospect Leads</h2>
          {assignedLeads.map((lead) => (
            <div key={lead.id} className="p-6 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-between hover:border-slate-700 transition">
              <div>
                <div className="flex items-center space-x-3">
                  <span className="text-lg font-bold text-white">{lead.name}</span>
                  <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-semibold border border-emerald-500/20">
                    Fit Score: {lead.score}
                  </span>
                </div>
                <div className="text-xs text-slate-400 mt-1">Target Program: {lead.program}</div>
                <div className="text-xs text-slate-500 mt-2 flex items-center space-x-4">
                  <span><Clock className="h-3 w-3 inline mr-1" />{lead.date}</span>
                  <span><Target className="h-3 w-3 inline mr-1" />{lead.stage}</span>
                </div>
              </div>

              <button className="px-4 py-2 text-xs font-semibold rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white transition flex items-center space-x-2">
                <PhoneCall className="h-3.5 w-3.5" />
                <span>Log Session</span>
              </button>
            </div>
          ))}
        </div>

        {/* Counseling Notes Quick Form */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 h-fit">
          <h2 className="text-base font-bold text-white mb-4">Log Session Notes</h2>
          <div className="space-y-4 text-xs">
            <div>
              <label className="block text-slate-400 mb-1">Select Prospect</label>
              <select className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-200">
                <option>Alex Johnson (Computer Science B.S.)</option>
                <option>Sarah Connor (Data Science M.S.)</option>
              </select>
            </div>
            <div>
              <label className="block text-slate-400 mb-1">Academic Notes</label>
              <textarea rows={3} placeholder="Record student academic background and career goals..." className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-slate-200 focus:outline-none focus:border-indigo-500"></textarea>
            </div>
            <button className="w-full py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-semibold shadow-lg shadow-indigo-500/20">
              Submit Session Record
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
