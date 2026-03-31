import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="🪞 Mind Insight", layout="wide")

# ================= ENGINE =================
def engine_completo(respostas):
    df = pd.DataFrame(list(respostas.items()), columns=['Q', 'Score'])

    blocos = {
        'Aberto_Experiencia': (1,15), 'Consciencioso': (16,27),
        'Extroversao': (28,37), 'Amavel': (38,49),
        'Neuroticismo': (50,61), 'Dinheiro_Seguranca': (62,71),
        'Dinheiro_Abundancia': (72,80)
    }

    medias = {k: round(df[(df['Q']>=i) & (df['Q']<=f)]['Score'].mean(),2)
              for k,(i,f) in blocos.items()}

    def cat(s): return "🟢 ALTO" if s>=4 else "🟡 MÉDIO" if s>=3 else "🔴 BAIXO"
    categorias = {k: cat(v) for k,v in medias.items()}

    # prioridade desempate
    prioridade = {
        'Consciencioso':1,'Aberto_Experiencia':2,'Extroversao':3,
        'Amavel':4,'Dinheiro_Abundancia':5,'Dinheiro_Seguranca':6,'Neuroticismo':7
    }

    dominante = sorted(medias.items(), key=lambda x:(-x[1], prioridade[x[0]]))[0][0]

    # estabilizador só se menor isolado
    if list(medias.values()).count(min(medias.values())) == 1 and medias['Neuroticismo'] == min(medias.values()):
        perfil = "🛡️ ESTABILIZADOR"
        plano = "1. Meditação diária\n2. Gratidão\n3. Revisão semanal"
    else:
        mapa = {
            'Consciencioso':"👑 EXECUTOR",
            'Aberto_Experiencia':"🚀 VISIONÁRIO",
            'Extroversao':"⭐ LÍDER",
            'Amavel':"🤝 CONSTRUTOR",
            'Dinheiro_Abundancia':"💰 FLUXO",
            'Dinheiro_Seguranca':"🏦 GUARDIÃO"
        }

        planos = {
            "EXECUTOR":"1. Automatize renda\n2. Contrate assistente\n3. Escale serviço",
            "VISIONÁRIO":"1. Protótipos semanais\n2. Mentores\n3. Teste mercado",
            "LÍDER":"1. Delegue\n2. Monte equipe\n3. Autoridade",
            "CONSTRUTOR":"1. Relacionamentos\n2. Parcerias\n3. Networking",
            "FLUXO":"1. Investir\n2. Mentoria\n3. Networking",
            "GUARDIÃO":"1. Diversificar\n2. Estudar ativos\n3. Renda passiva"
        }

        perfil = mapa[dominante]
        plano = planos[perfil.split()[1]]

    estabilidade = round(5 - medias['Neuroticismo'],2)
    potencial = round((medias['Dinheiro_Abundancia']+medias['Dinheiro_Seguranca'])/2,2)

    return {
        'medias':medias,
        'categorias':categorias,
        'perfil':perfil,
        'dominante':dominante,
        'plano':plano,
        'estabilidade':estabilidade,
        'potencial':potencial
    }

# ================= QUESTIONS =================
questions = {i:f"Pergunta {i}" for i in range(1,81)}

# ================= SESSION =================
if "q" not in st.session_state:
    st.session_state.q = 1
if "res" not in st.session_state:
    st.session_state.res = {}
if "email" not in st.session_state:
    st.session_state.email = ""

# ================= UI =================
st.title("🪞 Mind Insight")

if st.session_state.q == 1:
    st.session_state.email = st.text_input("Email")
    if st.button("Iniciar"):
        st.session_state.q = 2
        st.rerun()

elif st.session_state.q <= 81:
    q = st.session_state.q-1
    st.subheader(f"Pergunta {q}/80")
    val = st.radio("Resposta", [1,2,3,4,5], horizontal=True)

    if st.button("Próxima"):
        st.session_state.res[q]=val
        st.session_state.q +=1
        st.rerun()

else:
    resultado = engine_completo(st.session_state.res)

    st.success("Resultado pronto")

    st.metric("Perfil", resultado['perfil'])
    st.metric("Estabilidade", resultado['estabilidade'])
    st.metric("Financeiro", resultado['potencial'])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=list(resultado['medias'].values()),
        theta=list(resultado['medias'].keys()),
        fill='toself'
    ))
    st.plotly_chart(fig)

    st.write(resultado['plano'])
