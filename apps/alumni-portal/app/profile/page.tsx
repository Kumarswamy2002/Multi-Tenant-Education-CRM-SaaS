"use client";

import React, { useState, useEffect } from "react";

export default function ProfilePage() {
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [dataList, setDataList] = useState([
    { id: "REC-101", name: "Engineering Department Review", status: "Active", date: "2026-08-27", score: "94%" },
    { id: "REC-102", name: "Tuition Invoicing Run Q3", status: "Completed", date: "2026-08-26", score: "100%" },
    { id: "REC-103", name: "Campus Placement Drive Microsoft", status: "Scheduled", date: "2026-08-30", score: "88%" },
    { id: "REC-104", name: "AI Retention Intervention Task", status: "Pending", date: "2026-08-28", score: "76%" },
  ]);

  return (
    <div className="p-8 space-y-6 bg-slate-900 min-h-screen text-slate-100 font-sans">
      <div className="flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-500">
            Alumni Network & Giving Portal - User Profile & Account Settings
          </h1>
          <p className="text-slate-400 text-sm mt-1">Multi-Tenant Education Enterprise Operating Hub</p>
        </div>
        <div className="flex gap-3">
          <button className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 rounded-lg text-sm font-semibold transition-all shadow-lg shadow-indigo-600/30">
            + New Action
          </button>
          <button className="px-4 py-2 bg-slate-800 hover:bg-slate-700 rounded-lg text-sm font-medium border border-slate-700">
            Export Data
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-slate-800/80 border border-slate-700/60 p-5 rounded-xl shadow-sm">
          <p className="text-xs uppercase font-medium text-slate-400 tracking-wider">Total Active Entities</p>
          <p className="text-2xl font-bold text-white mt-2">4,892</p>
          <span className="text-xs text-emerald-400 mt-1 inline-block">+14.2% from last term</span>
        </div>
        <div className="bg-slate-800/80 border border-slate-700/60 p-5 rounded-xl shadow-sm">
          <p className="text-xs uppercase font-medium text-slate-400 tracking-wider">Operational Health</p>
          <p className="text-2xl font-bold text-emerald-400 mt-2">99.98%</p>
          <span className="text-xs text-slate-400 mt-1 inline-block">Real-time sync</span>
        </div>
        <div className="bg-slate-800/80 border border-slate-700/60 p-5 rounded-xl shadow-sm">
          <p className="text-xs uppercase font-medium text-slate-400 tracking-wider">Pending Approvals</p>
          <p className="text-2xl font-bold text-amber-400 mt-2">24</p>
          <span className="text-xs text-amber-300 mt-1 inline-block">Requires review</span>
        </div>
        <div className="bg-slate-800/80 border border-slate-700/60 p-5 rounded-xl shadow-sm">
          <p className="text-xs uppercase font-medium text-slate-400 tracking-wider">AI Predictive Accuracy</p>
          <p className="text-2xl font-bold text-blue-400 mt-2">96.4%</p>
          <span className="text-xs text-blue-300 mt-1 inline-block">Heuristic calibration</span>
        </div>
      </div>

      <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl overflow-hidden shadow-lg">
        <div className="p-4 border-b border-slate-700 flex justify-between items-center">
          <input
            type="text"
            placeholder="Search records, IDs, tags..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-slate-200 text-sm rounded-lg px-4 py-2 w-80 focus:outline-none focus:border-indigo-500"
          />
          <div className="flex gap-2">
            <span className="text-xs text-slate-400 bg-slate-900 px-3 py-1.5 rounded border border-slate-800">Showing 4 of 4 items</span>
          </div>
        </div>

        <table className="w-full text-left text-sm text-slate-300">
          <thead className="bg-slate-900/80 text-xs uppercase text-slate-400 border-b border-slate-700">
            <tr>
              <th className="p-4 font-semibold">Record ID</th>
              <th className="p-4 font-semibold">Description / Entity</th>
              <th className="p-4 font-semibold">Status</th>
              <th className="p-4 font-semibold">Effective Date</th>
              <th className="p-4 font-semibold">Confidence / Score</th>
              <th className="p-4 font-semibold text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700/50">
            {dataList.map((item) => (
              <tr key={item.id} className="hover:bg-slate-700/30 transition-colors">
                <td className="p-4 font-mono text-xs text-indigo-400 font-semibold">{item.id}</td>
                <td className="p-4 font-medium text-white">{item.name}</td>
                <td className="p-4">
                  <span className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
                    item.status === "Active" ? "bg-emerald-900/60 text-emerald-300 border border-emerald-700" :
                    item.status === "Completed" ? "bg-blue-900/60 text-blue-300 border border-blue-700" :
                    item.status === "Scheduled" ? "bg-purple-900/60 text-purple-300 border border-purple-700" :
                    "bg-amber-900/60 text-amber-300 border border-amber-700"
                  }`}>
                    {item.status}
                  </span>
                </td>
                <td className="p-4 text-slate-400">{item.date}</td>
                <td className="p-4 text-indigo-300 font-semibold">{item.score}</td>
                <td className="p-4 text-right">
                  <button className="text-xs text-indigo-400 hover:text-indigo-300 font-medium mr-3">View</button>
                  <button className="text-xs text-slate-400 hover:text-slate-200">Edit</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
