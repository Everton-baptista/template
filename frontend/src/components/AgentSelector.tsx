"use client";

import React from "react";
import { AgentInfo } from "@/lib/api";
import { Users, Bot, Sparkles, Cpu } from "lucide-react";

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
  return (
    <div className="glass-panel p-4 rounded-xl flex flex-col gap-4">
      <div className="flex items-center gap-2 text-indigo-400 font-semibold text-sm">
        <Sparkles className="w-4 h-4" />
        <span>SELEÇÃO DE AGENTE / EQUIPE</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {agents.map((agent) => {
          const isSelected = agent.id === selectedAgentId;
          const isTeam = agent.type === "multi_agent_team";
          return (
            <button
              key={agent.id}
              onClick={() => onSelectAgent(agent.id)}
              className={`p-3 rounded-lg text-left transition-all duration-200 flex flex-col justify-between ${
                isSelected
                  ? "bg-indigo-600/30 border-2 border-indigo-500 shadow-lg shadow-indigo-500/20"
                  : "bg-gray-800/40 border border-gray-700/50 hover:bg-gray-800/80"
              }`}
            >
              <div className="flex items-center justify-between gap-2 mb-1">
                <span className="font-semibold text-sm text-gray-100 flex items-center gap-1.5">
                  {isTeam ? (
                    <Users className="w-4 h-4 text-purple-400" />
                  ) : (
                    <Bot className="w-4 h-4 text-cyan-400" />
                  )}
                  {agent.name}
                </span>
                <span
                  className={`text-[10px] px-2 py-0.5 rounded-full font-mono uppercase tracking-wider ${
                    isTeam
                      ? "bg-purple-950 text-purple-300 border border-purple-800"
                      : "bg-cyan-950 text-cyan-300 border border-cyan-800"
                  }`}
                >
                  {isTeam ? "Multiagente" : "Agente"}
                </span>
              </div>
              <p className="text-xs text-gray-400 line-clamp-2">{agent.description}</p>
            </button>
          );
        })}
      </div>

      <div className="flex items-center justify-between border-t border-gray-800 pt-3 text-xs text-gray-400">
        <span className="flex items-center gap-1.5 font-medium text-gray-300">
          <Cpu className="w-4 h-4 text-indigo-400" /> Protocolo de Comunicação FastAPI:
        </span>
        <div className="flex gap-2">
          {(["sse", "websocket", "rest"] as const).map((proto) => (
            <button
              key={proto}
              onClick={() => onProtocolChange(proto)}
              className={`px-2.5 py-1 rounded-md uppercase font-mono font-bold transition-colors ${
                protocol === proto
                  ? "bg-indigo-600 text-white shadow-sm"
                  : "bg-gray-800 text-gray-400 hover:text-gray-200"
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
