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
questions = {
    1: "Gosto de experimentar novas ideias e atividades.",
    2: "Sou organizado e planejo minhas tarefas com antecedência.",
    3: "Me sinto energizado em grupos grandes de pessoas.",
    4: "Sou compassivo e priorizo as necessidades dos outros.",
    5: "Fico ansioso em situações de incerteza.",
    6: "Prefiro rotinas previsíveis a mudanças inesperadas.",
    7: "Tenho facilidade para me concentrar em uma tarefa por horas.",
    8: "Evito conflitos para manter a harmonia.",
    9: "Sou criativo e penso fora da caixa.",
    10: "Me irrito facilmente com erros alheios.",
    11: "Gosto de ser o centro das atenções.",
    12: "Sou disciplinado com prazos e compromissos.",
    13: "Me preocupo excessivamente com o futuro.",
    14: "Valorizo a lealdade acima de tudo nas relações.",
    15: "Busco conhecimento por prazer, não por obrigação.",
    16: "Tomo decisões rápidas baseadas em intuição.",
    17: "Analiso todos os detalhes antes de agir.",
    18: "Sou direto e falo o que penso, mesmo que incomode.",
    19: "Prefiro trabalhar sozinho a em equipe.",
    20: "Adapto meu comportamento conforme o ambiente.",
    21: "Sou persistente mesmo diante de fracassos.",
    22: "Evito riscos desnecessários.",
    23: "Expresso emoções abertamente.",
    24: "Planejo conversas importantes com antecedência.",
    25: "Sou flexível com mudanças de planos.",
    26: "Priorizo eficiência acima de relações.",
    27: "Aprendo mais observando do que fazendo.",
    28: "Em crises, mantenho a calma e foco na solução.",
    29: "Fico paralisado quando algo dá errado.",
    30: "Sob estresse, busco apoio de outros.",
    31: "Reajo com raiva quando provocado.",
    32: "Transformo pressão em motivação.",
    33: "Evito confrontos diretos em tensões.",
    34: "Recupero equilíbrio emocional rapidamente.",
    35: "Culpo os outros por meus erros.",
    36: "Aumento a produtividade sob prazos apertados.",
    37: "Fico ansioso com críticas.",
    38: "Tenho facilidade para aprender novas habilidades técnicas.",
    39: "Sou bom em liderar grupos para resultados.",
    40: "Resolvo problemas matemáticos ou lógicos intuitivamente.",
    41: "Crio conteúdo persuasivo (escrita, vídeo).",
    42: "Organizo espaços e rotinas de forma eficiente.",
    43: "Negocio bem preços e acordos.",
    44: "Sou criativo em soluções cotidianas.",
    45: "Gerencio múltiplas tarefas sem perder o foco.",
    46: "Inspiro confiança em negociações.",
    47: "Identifico oportunidades de negócio rapidamente.",
    48: "Ensino ou explico conceitos complexos com clareza.",
    49: "Melhoro processos existentes de forma inovadora.",
    50: "Meu valor depende da aprovação dos outros.",
    51: "Me sinto confortável em papéis de liderança.",
    52: "Priorizo família acima de carreira.",
    53: "Construo redes de contatos facilmente.",
    54: "Sou influenciado por normas do meu grupo social.",
    55: "Defendo minhas opiniões em debates públicos.",
    56: "Valorizo tradições culturais da minha família.",
    57: "Me adapto bem a culturas diferentes.",
    58: "Sou generoso com tempo e recursos.",
    59: "Competição me motiva mais que colaboração.",
    60: "Meu papel social ideal é de cuidador.",
    61: "Questiono normas sociais estabelecidas.",
    62: "Estou satisfeito com minha vida atual.",
    63: "Sei exatamente o que quero mudar nos próximos 6 meses.",
    64: "Minhas ações diárias me aproximam dos meus objetivos.",
    65: "Sinto que desperdiço potencial.",
    66: "Tenho clareza sobre minha identidade principal.",
    67: "Me comparo frequentemente com outros.",
    68: "Estou em uma fase de crescimento.",
    69: "Visualizo meu 'eu ideal' com detalhes.",
    70: "Falta de recursos me impede de avançar.",
    71: "Sou proativo em buscar mudanças.",
    72: "Dinheiro é fonte de segurança emocional para mim.",
    73: "Gosto de exibir bens para impressionar.",
    74: "Planejo finanças com 5+ anos de visão.",
    75: "Perdas financeiras me afetam por semanas.",
    76: "Sou generoso e dou sem esperar retorno.",
    77: "Prefiro guardar para emergências que investir.",
    78: "Meu trabalho é valorizado financeiramente.",
    79: "Dinheiro 'circula' naturalmente na minha vida.",
    80: "Gastei impulsivamente nos últimos 6 meses."
}

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
    q = st.session_state.q - 1
    st.subheader(f"Pergunta {q}/80")
    st.markdown(f"**{questions[q]}**")

    val = st.radio(
        "Resposta",
        [
            "1 - Discordo totalmente",
            "2 - Discordo",
            "3 - Neutro",
            "4 - Concordo",
            "5 - Concordo totalmente"
        ],
        horizontal=True
    )

    if st.button("Próxima"):
        score = int(val.split(" - ")[0])
        st.session_state.res[q] = score
        st.session_state.q += 1
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
