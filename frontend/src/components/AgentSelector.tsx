"use client";

import React, { useState } from "react";
import { AgentInfo } from "@/lib/api";
import { Users, Bot, Cpu, Sparkles, Filter } from "lucide-react";

interface AgentSelectorProps {
  agents: AgentInfo[];
  selectedAgentId: string;
  onSelectAgent: (id: string) => void;
  protocol: "sse" | "websocket" | "rest";
  onProtocolChange: (proto: "sse" | "websocket" | "rest") => void;
}

export const AgentSelector: React.FC<AgentSelectorProps> = ({
  agents,
  selectedAgentId,
  onSelectAgent,
  protocol,
  onProtocolChange,
}) => {
  const [filter, setFilter] = useState<"all" | "single_agent" | "multi_agent_team">("all");

  const filteredAgents = agents.filter((agent) => {
    if (filter === "all") return true;
    return agent.type === filter;
  });

  return (
    <div className="glass-card rounded-2xl p-5 flex flex-col gap-4">
      {/* Top Header & Filter Tabs */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 border-b border-slate-800/80 pb-4">
        <div className="flex items-center gap-2">
          <div className="p-2 bg-indigo-500/10 border border-indigo-500/20 rounded-lg text-indigo-400">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-slate-200">Seleção de Agente</h2>
            <p className="text-xs text-slate-400">Escolha o assistente ou equipe multiagente ideal</p>
          </div>
        </div>

        {/* Filter buttons */}
        <div className="flex items-center gap-1.5 bg-slate-900/80 p-1 rounded-xl border border-slate-800/80 text-xs">
          <button
            onClick={() => setFilter("all")}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all ${
              filter === "all"
                ? "bg-indigo-600 text-white shadow-sm"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Todos ({agents.length})
          </button>
          <button
            onClick={() => setFilter("single_agent")}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all flex items-center gap-1.5 ${
              filter === "single_agent"
                ? "bg-indigo-600 text-white shadow-sm"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <Bot className="w-3.5 h-3.5" />
            Agentes
          </button>
          <button
            onClick={() => setFilter("multi_agent_team")}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all flex items-center gap-1.5 ${
              filter === "multi_agent_team"
                ? "bg-indigo-600 text-white shadow-sm"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <Users className="w-3.5 h-3.5" />
            Equipes
          </button>
        </div>
      </div>

      {/* Agents Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {filteredAgents.map((agent) => {
          const isSelected = agent.id === selectedAgentId;
          const isTeam = agent.type === "multi_agent_team";
          return (
            <button
              key={agent.id}
              onClick={() => onSelectAgent(agent.id)}
              className={`group relative p-4 rounded-xl text-left transition-all duration-200 flex flex-col justify-between border ${
                isSelected
                  ? "bg-indigo-950/40 border-indigo-500/80 shadow-lg shadow-indigo-500/10"
                  : "bg-slate-900/40 border-slate-800/60 hover:bg-slate-800/40 hover:border-slate-700/80"
              }`}
            >
              <div className="flex items-start justify-between gap-2 mb-2">
                <div className="flex items-center gap-2.5">
                  <div
                    className={`p-2 rounded-lg ${
                      isTeam
                        ? "bg-purple-500/10 text-purple-400 border border-purple-500/20"
                        : "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20"
                    }`}
                  >
                    {isTeam ? <Users className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                  </div>
                  <span className="font-semibold text-sm text-slate-100 group-hover:text-white transition-colors">
                    {agent.name}
                  </span>
                </div>
                <span
                  className={`text-[10px] px-2 py-0.5 rounded-full font-mono uppercase tracking-wider ${
                    isTeam
                      ? "bg-purple-950/80 text-purple-300 border border-purple-800/50"
                      : "bg-cyan-950/80 text-cyan-300 border border-cyan-800/50"
                  }`}
                >
                  {isTeam ? "Equipe" : "Agente"}
                </span>
              </div>

              <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed font-normal">
                {agent.description}
              </p>
            </button>
          );
        })}
      </div>

      {/* Protocol Selector Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-2 border-t border-slate-800/80 pt-3 text-xs text-slate-400">
        <span className="flex items-center gap-2 font-medium text-slate-300">
          <Cpu className="w-4 h-4 text-indigo-400" /> Protocolo de Comunicação FastAPI:
        </span>
        <div className="flex bg-slate-900/80 p-1 rounded-xl border border-slate-800/80">
          {(["sse", "websocket", "rest"] as const).map((proto) => (
            <button
              key={proto}
              onClick={() => onProtocolChange(proto)}
              className={`px-3 py-1 rounded-lg uppercase font-mono font-bold text-[11px] transition-all ${
                protocol === proto
                  ? "bg-indigo-600 text-white shadow-sm"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {proto}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

