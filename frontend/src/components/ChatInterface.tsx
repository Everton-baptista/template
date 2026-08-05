"use client";

import React, { useState, useRef, useEffect } from "react";
import { API_BASE_URL } from "@/lib/api";
import { Send, Bot, User, Loader2, Zap } from "lucide-react";
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

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  selectedAgentId,
  protocol,
}) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      sender: "assistant",
      content: "Olá! Sou o ambiente de orquestração do **Agno**. Escolha um agente ou equipe acima e envie sua solicitação.",
      agentId: selectedAgentId,
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      sender: "user",
      content: input,
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    const currentInput = input;
    setInput("");
    setLoading(true);

    const assistantMsgId = (Date.now() + 1).toString();
    const assistantMsg: Message = {
      id: assistantMsgId,
      sender: "assistant",
      content: "",
      agentId: selectedAgentId,
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages((prev) => [...prev, assistantMsg]);

    try {
      if (protocol === "sse") {
        const response = await fetch(`${API_BASE_URL}/api/v1/agent/stream`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: currentInput, agent_id: selectedAgentId }),
        });

        if (!response.body) throw new Error("Sem corpo de resposta");

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
          const { value, done } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const lines = chunk.split("\n");
          for (const line of lines) {
            if (line.startswith?.("data: ")) {
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
                }
              } catch (e) {
                // Parse pontual ignorado
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
              message: currentInput,
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
            socket.close();
            setLoading(false);
          }
        };

        socket.onerror = (error) => {
          console.error("Erro WebSocket:", error);
          socket.close();
        };
      } else {
        // REST Standard
        const res = await fetch(`${API_BASE_URL}/api/v1/agent/run`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: currentInput, agent_id: selectedAgentId }),
        });

        const data = await res.json();
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantMsgId ? { ...m, content: data.content || "Sem resposta." } : m
          )
        );
      }
    } catch (err: any) {
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantMsgId
            ? { ...m, content: `⚠️ Erro de comunicação: ${err.message || err}` }
            : m
        )
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel flex-1 flex flex-col rounded-xl overflow-hidden h-[600px]">
      {/* Header do Chat */}
      <div className="px-6 py-4 border-b border-gray-800 flex items-center justify-between bg-gray-900/60">
        <div className="flex items-center gap-2">
          <Zap className="w-5 h-5 text-indigo-400" />
          <span className="font-semibold text-gray-200">Terminal Agno Multi-Agent</span>
        </div>
        <span className="text-xs font-mono px-2 py-1 bg-indigo-950 text-indigo-300 border border-indigo-800 rounded">
          Protocolo: {protocol.toUpperCase()}
        </span>
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
              <div className="w-8 h-8 rounded-lg bg-indigo-600/30 border border-indigo-500/50 flex items-center justify-center shrink-0 text-indigo-300">
                <Bot className="w-5 h-5" />
              </div>
            )}
            <div
              className={`max-w-[80%] rounded-xl p-4 text-sm leading-relaxed ${
                msg.sender === "user"
                  ? "bg-indigo-600 text-white rounded-tr-none shadow-md"
                  : "bg-gray-800/80 border border-gray-700/60 text-gray-100 rounded-tl-none"
              }`}
            >
              {msg.sender === "assistant" ? (
                <div className="prose prose-invert max-w-none text-sm">
                  <ReactMarkdown>{msg.content || "Pensando..."}</ReactMarkdown>
                </div>
              ) : (
                <p>{msg.content}</p>
              )}
              <span className="block text-[10px] text-gray-400 mt-2 text-right">
                {msg.timestamp}
              </span>
            </div>
            {msg.sender === "user" && (
              <div className="w-8 h-8 rounded-lg bg-purple-600/30 border border-purple-500/50 flex items-center justify-center shrink-0 text-purple-300">
                <User className="w-5 h-5" />
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Caixa de Entrada */}
      <div className="p-4 border-t border-gray-800 bg-gray-900/60 flex gap-3">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder={`Pergunte algo para o agente (${selectedAgentId})...`}
          className="flex-1 bg-gray-800/60 border border-gray-700 rounded-lg px-4 py-2.5 text-sm text-gray-100 placeholder-gray-500 focus:outline-none focus:border-indigo-500 transition-colors"
          disabled={loading}
        />
        <button
          onClick={sendMessage}
          disabled={loading || !input.trim()}
          className="glass-button px-5 py-2.5 rounded-lg text-white font-medium flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <Send className="w-4 h-4" />
          )}
          <span>Enviar</span>
        </button>
      </div>
    </div>
  );
};
