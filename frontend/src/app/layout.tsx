import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Agno Multi-Agent Enterprise Workspace",
  description: "Plataforma de alta performance para orquestração de Agentes e Equipes Multiagentes com Agno e FastAPI",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body className="antialiased">{children}</body>
    </html>
  );
}
