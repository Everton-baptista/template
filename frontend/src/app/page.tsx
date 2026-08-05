"use client";

import { useEffect, useState } from "react";
import { fetchAgents, AgentInfo } from "@/lib/api";
import { AgentSelector } from "@/components/AgentSelector";
import { ChatInterface } from "@/components/ChatInterface";
import { Layers, Activity } from "lucide-react";

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
      {/* Header Superior */}
      <header className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-panel p-6 rounded-2xl">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-indigo-600/20 border border-indigo-500/40 rounded-xl text-indigo-400">
            <Layers className="w-8 h-8" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
              Agno Multi-Agent Studio
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800 font-mono font-medium">
                Enterprise Template
              </span>
            </h1>
            <p className="text-xs text-gray-400 mt-1">
              Plataforma para Agentes e Multiagentes alimentada por Agno, FastAPI e Next.js.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 text-xs text-gray-400 font-mono bg-gray-900/80 px-3.5 py-2 rounded-lg border border-gray-800">
          <Activity className="w-4 h-4 text-emerald-400 animate-pulse" />
          <span>Status do Sistema: Pronto</span>
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
