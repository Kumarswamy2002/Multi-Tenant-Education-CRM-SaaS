"use client";

import React, { useState, useEffect, useMemo } from "react";

export interface AcademicsRecord {
  id: string;
  title: string;
  category: string;
  status: "Active" | "Pending" | "Completed" | "Warning" | "Critical";
  priority: "High" | "Medium" | "Low";
  date: string;
  metricValue: number;
  tags: string[];
}

export default function AcademicsView() {
  const [data, setData] = useState<AcademicsRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [page, setPage] = useState(1);
  const [selectedRecord, setSelectedRecord] = useState<AcademicsRecord | null>(null);

  useEffect(() => {
    const timer = setTimeout(() => {
      const items: AcademicsRecord[] = Array.from({ length: 15 }).map((_, i) => ({
        id: `ACADEMICS-${1000 + i}`,
        title: `Academics Operational Record ${i + 1}`,
        category: i % 3 === 0 ? "Academic Tier A" : i % 3 === 1 ? "Administrative" : "Strategic",
        status: i % 4 === 0 ? "Active" : i % 4 === 1 ? "Pending" : i % 4 === 2 ? "Completed" : "Warning",
        priority: i % 3 === 0 ? "High" : i % 3 === 1 ? "Medium" : "Low",
        date: "2026-08-27",
        metricValue: 85 + (i * 2) % 15,
        tags: ["Multi-Tenant", "Enterprise", "academics"],
      }));
      setData(items);
      setLoading(false);
    }, 200);
    return () => clearTimeout(timer);
  }, []);

  const filteredData = useMemo(() => {
    return data.filter((item) => {
      const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                            item.id.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesStatus = statusFilter === "ALL" || item.status === statusFilter;
      return matchesSearch && matchesStatus;
    });
  }, [data, searchTerm, statusFilter]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8 font-sans">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <span className="px-3 py-1 bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-xs font-semibold rounded-full uppercase tracking-wider">
              Recruiter Hub
            </span>
            <span className="text-slate-500 text-sm">•</span>
            <span className="text-slate-400 text-sm font-medium">Enterprise Module</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white mt-2 tracking-tight">
            Academics Management Console
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Real-time multi-tenant monitoring, operational actions, and AI analytics.
          </p>
        </div>

        <div className="flex gap-3">
          <button className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-xl text-sm font-semibold transition-all">
            Download Report
          </button>
          <button className="px-4 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-sm font-semibold transition-all shadow-lg shadow-indigo-600/30">
            + Create Academics Entry
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
          <p className="text-xs uppercase font-bold text-slate-400">Total Managed Records</p>
          <p className="text-3xl font-black text-white mt-2">1,248</p>
          <p className="text-xs text-emerald-400 mt-1 font-medium">+18.5% YoY Growth</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
          <p className="text-xs uppercase font-bold text-slate-400">Success Rate</p>
          <p className="text-3xl font-black text-emerald-400 mt-2">99.4%</p>
          <p className="text-xs text-slate-400 mt-1 font-medium">Within SLA constraints</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
          <p className="text-xs uppercase font-bold text-slate-400">Active Pipeline Volume</p>
          <p className="text-3xl font-black text-blue-400 mt-2">$ 842,000</p>
          <p className="text-xs text-blue-300 mt-1 font-medium">Reconciled ledger</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
          <p className="text-xs uppercase font-bold text-slate-400">Risk Mitigation Score</p>
          <p className="text-3xl font-black text-indigo-400 mt-2">94 / 100</p>
          <p className="text-xs text-indigo-300 mt-1 font-medium">AI Early warning calibrated</p>
        </div>
      </div>

      {/* Control Bar */}
      <div className="flex flex-col md:flex-row justify-between items-center gap-4 bg-slate-900/60 p-4 border border-slate-800 rounded-2xl">
        <div className="flex items-center gap-3 w-full md:w-auto">
          <input
            type="text"
            placeholder="Search by ID, title, or tags..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="bg-slate-950 border border-slate-800 text-sm text-slate-200 px-4 py-2.5 rounded-xl w-full md:w-80 focus:outline-none focus:border-indigo-500"
          />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-slate-950 border border-slate-800 text-sm text-slate-300 px-4 py-2.5 rounded-xl focus:outline-none focus:border-indigo-500"
          >
            <option value="ALL">All Statuses</option>
            <option value="Active">Active</option>
            <option value="Pending">Pending</option>
            <option value="Completed">Completed</option>
            <option value="Warning">Warning</option>
          </select>
        </div>

        <div className="text-xs text-slate-400 font-medium">
          Showing {filteredData.length} active records
        </div>
      </div>

      {/* Data Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        <table className="w-full text-left text-sm text-slate-300">
          <thead className="bg-slate-950 text-xs uppercase text-slate-400 font-semibold border-b border-slate-800">
            <tr>
              <th className="p-4">Entity ID</th>
              <th className="p-4">Record Description</th>
              <th className="p-4">Category</th>
              <th className="p-4">Status</th>
              <th className="p-4">Priority</th>
              <th className="p-4">Performance Metric</th>
              <th className="p-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {filteredData.map((row) => (
              <tr key={row.id} className="hover:bg-slate-800/40 transition-colors">
                <td className="p-4 font-mono text-xs text-indigo-400 font-bold">{row.id}</td>
                <td className="p-4 font-semibold text-white">{row.title}</td>
                <td className="p-4 text-slate-400">{row.category}</td>
                <td className="p-4">
                  <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                    row.status === "Active" ? "bg-emerald-950 text-emerald-300 border border-emerald-800" :
                    row.status === "Completed" ? "bg-blue-950 text-blue-300 border border-blue-800" :
                    row.status === "Pending" ? "bg-purple-950 text-purple-300 border border-purple-800" :
                    "bg-amber-950 text-amber-300 border border-amber-800"
                  }`}>
                    {row.status}
                  </span>
                </td>
                <td className="p-4">
                  <span className={`text-xs font-semibold ${
                    row.priority === "High" ? "text-rose-400" :
                    row.priority === "Medium" ? "text-amber-400" : "text-slate-400"
                  }`}>
                    {row.priority}
                  </span>
                </td>
                <td className="p-4 font-bold text-indigo-300">{row.metricValue}%</td>
                <td className="p-4 text-right">
                  <button
                    onClick={() => setSelectedRecord(row)}
                    className="text-xs text-indigo-400 hover:text-indigo-300 font-bold mr-3"
                  >
                    Inspect
                  </button>
                  <button className="text-xs text-slate-400 hover:text-white font-medium">Configure</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Detail Modal Drawer */}
      {selectedRecord && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-700 p-6 rounded-2xl max-w-lg w-full space-y-4">
            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
              <h3 className="text-xl font-bold text-white">{selectedRecord.title}</h3>
              <button
                onClick={() => setSelectedRecord(null)}
                className="text-slate-400 hover:text-white text-lg font-bold"
              >
                ✕
              </button>
            </div>
            <div className="space-y-2 text-sm text-slate-300">
              <p><strong className="text-slate-400">ID:</strong> {selectedRecord.id}</p>
              <p><strong className="text-slate-400">Category:</strong> {selectedRecord.category}</p>
              <p><strong className="text-slate-400">Status:</strong> {selectedRecord.status}</p>
              <p><strong className="text-slate-400">Priority:</strong> {selectedRecord.priority}</p>
              <p><strong className="text-slate-400">Metric Value:</strong> {selectedRecord.metricValue}%</p>
              <p><strong className="text-slate-400">Tags:</strong> {selectedRecord.tags.join(", ")}</p>
            </div>
            <div className="flex justify-end gap-3 pt-4 border-t border-slate-800">
              <button
                onClick={() => setSelectedRecord(null)}
                className="px-4 py-2 bg-slate-800 text-slate-300 hover:bg-slate-700 rounded-xl text-sm font-semibold"
              >
                Close
              </button>
              <button
                onClick={() => {
                  alert(`Audit confirmed for ${selectedRecord.id}`);
                  setSelectedRecord(null);
                }}
                className="px-4 py-2 bg-indigo-600 text-white hover:bg-indigo-500 rounded-xl text-sm font-semibold"
              >
                Confirm Verification
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
