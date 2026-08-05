"use client";

import { useEffect, useState } from "react";
import { fetchAgents, AgentInfo } from "@/lib/api";
import { AgentSelector } from "@/components/AgentSelector";
import { ChatInterface } from "@/components/ChatInterface";
import { Layers, Activity, Sparkles } from "lucide-react";

export default function Home() {
  const [agents, setAgents] = useState<AgentInfo[]>([]);
  const [selectedAgentId, setSelectedAgentId] = useState<string>("router");
  const [protocol, setProtocol] = useState<"sse" | "websocket" | "rest">("sse");

  useEffect(() => {
    fetchAgents().then((data) => {
      setAgents(data);
      if (data.length > 0) {
        setSelectedAgentId(data[0].id);
      }
    });
  }, []);

  return (
    <main className="max-w-7xl mx-auto p-4 md:p-8 min-h-screen flex flex-col gap-6">
      {/* Header Clean */}
      <header className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 glass-card p-6 rounded-2xl">
        <div className="flex items-center gap-3.5">
          <div className="p-3 bg-indigo-500/10 border border-indigo-500/20 rounded-2xl text-indigo-400">
            <Layers className="w-7 h-7" />
          </div>
          <div>
            <div className="flex items-center gap-2.5 flex-wrap">
              <h1 className="text-xl md:text-2xl font-bold tracking-tight text-slate-100">
                Agno Multi-Agent Studio
              </h1>
              <span className="text-[11px] px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono font-medium flex items-center gap-1">
                <Sparkles className="w-3 h-3" /> Clean Architecture
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Plataforma de IA com Agentes e Equipes Multiagentes orquestrada por Agno & FastAPI.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs text-slate-400 font-mono bg-slate-900/80 px-4 py-2 rounded-xl border border-slate-800/80 self-start sm:self-auto">
          <Activity className="w-4 h-4 text-emerald-400 animate-pulse" />
          <span>Sistema Conectado</span>
        </div>
      </header>

      {/* Seletor de Agentes */}
      <AgentSelector
        agents={agents}
        selectedAgentId={selectedAgentId}
        onSelectAgent={setSelectedAgentId}
        protocol={protocol}
        onProtocolChange={setProtocol}
      />

      {/* Interface de Chat Principal */}
      <ChatInterface
        selectedAgentId={selectedAgentId}
        protocol={protocol}
      />
    </main>
  );
}

