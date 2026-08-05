"use client";

import React, { useState, useRef, useEffect } from "react";
import { API_BASE_URL } from "@/lib/api";
import { Send, Bot, User, Loader2, Zap, Trash2, Sparkles, Copy, Check } from "lucide-react";
import ReactMarkdown from "react-markdown";

interface Message {
  id: string;
  sender: "user" | "assistant";
  content: string;
  agentId?: string;
  timestamp: string;
}

interface ChatInterfaceProps {
  selectedAgentId: string;
  protocol: "sse" | "websocket" | "rest";
}

const QUICK_PROMPTS = [
  "🔍 Pesquise tendências de IA para 2026",
  "📊 Analise dados financeiros de empresas de tech",
  "💻 Crie uma API REST em Python com FastAPI",
  "📝 Redija um resumo executivo sobre inovação",
];

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  selectedAgentId,
  protocol,
}) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      sender: "assistant",
      content: "Olá! Bem-vindo ao **Agno Multi-Agent Studio**. Selecione um agente ou equipe acima e envie sua solicitação abaixo.",
      agentId: selectedAgentId,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const clearChat = () => {
    setMessages([
      {
        id: "welcome-" + Date.now(),
        sender: "assistant",
        content: `Chat reiniciado para o agente **${selectedAgentId}**. Como posso ajudar?`,
        agentId: selectedAgentId,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      },
    ]);
  };

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleSend = async (textToSend?: string) => {
    const messageText = (textToSend || input).trim();
    if (!messageText || loading) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      sender: "user",
      content: messageText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInput("");
    setLoading(true);

    const assistantMsgId = (Date.now() + 1).toString();
    const assistantMsg: Message = {
      id: assistantMsgId,
      sender: "assistant",
      content: "",
      agentId: selectedAgentId,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, assistantMsg]);

    try {
      if (protocol === "sse") {
        const response = await fetch(`${API_BASE_URL}/api/v1/agent/stream`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: messageText, agent_id: selectedAgentId }),
        });

        if (!response.body) throw new Error("Sem resposta do servidor");

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
          const { value, done } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const lines = chunk.split("\n");
          for (const line of lines) {
            if (line.startsWith("data: ")) {
              try {
                const data = JSON.parse(line.replace("data: ", ""));
                if (data.delta) {
                  setMessages((prev) =>
                    prev.map((m) =>
                      m.id === assistantMsgId
                        ? { ...m, content: m.content + data.delta }
                        : m
                    )
                  );
                } else if (data.error) {
                  setMessages((prev) =>
                    prev.map((m) =>
                      m.id === assistantMsgId
                        ? { ...m, content: `⚠️ Erro: ${data.error}` }
                        : m
                    )
                  );
                }
              } catch (e) {
                // Parse ignorado para partes incompletas
              }
            }
          }
        }
      } else if (protocol === "websocket") {
        const wsUrl = API_BASE_URL.replace(/^http/, "ws") + "/api/v1/ws/chat";
        const socket = new WebSocket(wsUrl);

        socket.onopen = () => {
          socket.send(
            JSON.stringify({
              action: "send_message",
              agent_id: selectedAgentId,
              message: messageText,
            })
          );
        };

        socket.onmessage = (event) => {
          const data = JSON.parse(event.data);
          if (data.event === "delta" && data.delta) {
            setMessages((prev) =>
              prev.map((m) =>
                m.id === assistantMsgId
                  ? { ...m, content: m.content + data.delta }
                  : m
              )
            );
          } else if (data.event === "done" || data.event === "error") {
            if (data.message) {
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantMsgId ? { ...m, content: `⚠️ Erro: ${data.message}` } : m
                )
              );
            }
            socket.close();
            setLoading(false);
          }
        };

        socket.onerror = (error) => {
          console.error("Erro WebSocket:", error);
          socket.close();
          setLoading(false);
        };
      } else {
        // REST Standard
        const res = await fetch(`${API_BASE_URL}/api/v1/agent/run`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: messageText, agent_id: selectedAgentId }),
        });

        const data = await res.json();
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantMsgId ? { ...m, content: data.content || "Sem resposta retornada." } : m
          )
        );
      }
    } catch (err: any) {
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantMsgId
            ? { ...m, content: `⚠️ Erro de Comunicação: ${err.message || err}` }
            : m
        )
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card flex-1 flex flex-col rounded-2xl overflow-hidden min-h-[550px] h-[620px]">
      {/* Header do Chat Clean */}
      <div className="px-6 py-3.5 border-b border-slate-800/80 flex items-center justify-between bg-slate-900/80 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 border border-indigo-500/20 rounded-xl text-indigo-400">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <span className="font-semibold text-sm text-slate-100 block">
              Sessão Ativa: <span className="text-indigo-400 capitalize">{selectedAgentId}</span>
            </span>
            <span className="text-[11px] text-slate-400 font-mono">
              Modo: {protocol.toUpperCase()}
            </span>
          </div>
        </div>

        <button
          onClick={clearChat}
          title="Limpar histórico"
          className="p-2 text-slate-400 hover:text-rose-400 hover:bg-slate-800/60 rounded-xl transition-all"
        >
          <Trash2 className="w-4 h-4" />
        </button>
      </div>

      {/* Lista de Mensagens */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-3 ${
              msg.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            {msg.sender === "assistant" && (
              <div className="w-8 h-8 rounded-xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center shrink-0 text-indigo-400">
                <Bot className="w-4 h-4" />
              </div>
            )}
            <div
              className={`relative group max-w-[82%] rounded-2xl p-4 text-sm leading-relaxed ${
                msg.sender === "user"
                  ? "bg-indigo-600 text-white rounded-tr-none shadow-md shadow-indigo-600/10"
                  : "bg-slate-900/70 border border-slate-800/80 text-slate-200 rounded-tl-none shadow-sm"
              }`}
            >
              {msg.sender === "assistant" ? (
                <div className="prose prose-invert max-w-none text-sm leading-relaxed">
                  <ReactMarkdown>{msg.content || "Processando resposta..."}</ReactMarkdown>
                </div>
              ) : (
                <p className="whitespace-pre-wrap">{msg.content}</p>
              )}

              <div className="flex items-center justify-between gap-4 mt-2.5 pt-2 border-t border-slate-800/40 text-[10px] text-slate-400">
                <span>{msg.timestamp}</span>
                {msg.sender === "assistant" && msg.content && (
                  <button
                    onClick={() => copyToClipboard(msg.content, msg.id)}
                    className="hover:text-slate-200 transition-colors flex items-center gap-1"
                  >
                    {copiedId === msg.id ? (
                      <Check className="w-3 h-3 text-emerald-400" />
                    ) : (
                      <Copy className="w-3 h-3" />
                    )}
                  </button>
                )}
              </div>
            </div>
            {msg.sender === "user" && (
              <div className="w-8 h-8 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center shrink-0 text-slate-300">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompts se houver apenas mensagem inicial */}
      {messages.length <= 1 && (
        <div className="px-6 py-2 flex flex-wrap gap-2">
          {QUICK_PROMPTS.map((promptText, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(promptText)}
              className="text-xs bg-slate-900/80 hover:bg-indigo-950/60 border border-slate-800 hover:border-indigo-500/50 text-slate-300 px-3 py-1.5 rounded-full transition-all flex items-center gap-1.5"
            >
              <Sparkles className="w-3 h-3 text-indigo-400" />
              {promptText}
            </button>
          ))}
        </div>
      )}

      {/* Caixa de Entrada Clean */}
      <div className="p-4 border-t border-slate-800/80 bg-slate-900/80 backdrop-blur-md flex gap-3 items-center">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSend()}
          placeholder={`Digite sua mensagem para ${selectedAgentId}...`}
          className="flex-1 bg-slate-950/60 border border-slate-800 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500/80 transition-colors"
          disabled={loading}
        />
        <button
          onClick={() => handleSend()}
          disabled={loading || !input.trim()}
          className="glass-button px-5 py-3 rounded-xl text-white font-medium flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed text-sm"
        >
          {loading ? (
            <Loader2 className="w-4 h-4 animate-spin text-indigo-400" />
          ) : (
            <Send className="w-4 h-4" />
          )}
          <span className="hidden sm:inline">Enviar</span>
        </button>
      </div>
    </div>
  );
};

