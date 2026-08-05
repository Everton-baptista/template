import os
import json
import httpx
import streamlit as st

st.set_page_config(
    page_title="Agno Multi-Agent Playground",
    page_icon="🤖",
    layout="wide"
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("🤖 Agno Multi-Agent Enterprise Playground")
st.caption("Interface rápida de prototipagem para interagir com Agentes e Equipes Multiagentes em tempo real.")

# Sidebar - Configurações
st.sidebar.header("⚙️ Configurações")

# Carrega agentes disponíveis
try:
    with httpx.Client(timeout=5.0) as client:
        response = client.get(f"{BACKEND_URL}/api/v1/agents")
        agents_data = response.json().get("agents", [])
        agent_options = {a["name"]: a["id"] for a in agents_data}
except Exception as e:
    st.sidebar.error(f"Erro ao conectar ao Backend ({BACKEND_URL}): {e}")
    agent_options = {"Roteador Inteligente": "router"}

selected_agent_name = st.sidebar.selectbox("Selecione o Agente / Equipe", list(agent_options.keys()))
selected_agent_id = agent_options[selected_agent_name]

use_streaming = st.sidebar.toggle("Habilitar Streaming (SSE)", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Status dos Serviços")
try:
    with httpx.Client(timeout=3.0) as client:
        h = client.get(f"{BACKEND_URL}/api/v1/health").json()
        st.sidebar.success(f"Backend API: {h['status'].upper()} (v{h['version']})")
except Exception:
    st.sidebar.error("Backend API: Indisponível")

# Chat Container
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite sua instrução para a equipe de agentes..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        if use_streaming:
            try:
                with httpx.stream(
                    "POST",
                    f"{BACKEND_URL}/api/v1/agent/stream",
                    json={"message": prompt, "agent_id": selected_agent_id},
                    timeout=60.0
                ) as response:
                    for line in response.iter_lines():
                        if line.startswith("data: "):
                            raw_data = line[6:]
                            try:
                                payload = json.loads(raw_data)
                                if "delta" in payload:
                                    full_response += payload["delta"]
                                    message_placeholder.markdown(full_response + "▌")
                            except json.JSONDecodeError:
                                pass
                message_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"Erro ao receber streaming: {e}")
        else:
            try:
                res = httpx.post(
                    f"{BACKEND_URL}/api/v1/agent/run",
                    json={"message": prompt, "agent_id": selected_agent_id},
                    timeout=60.0
                )
                if res.status_code == 200:
                    full_response = res.json().get("content", "")
                    message_placeholder.markdown(full_response)
                else:
                    st.error(f"Erro na API: {res.text}")
            except Exception as e:
                st.error(f"Erro na requisição REST: {e}")

        if full_response:
            st.session_state.messages.append({"role": "assistant", "content": full_response})
