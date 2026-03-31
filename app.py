import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import smtplib
from email.message import EmailMessage

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="🪞 Mind Insight",
    page_icon="🪞",
    layout="wide"
)

PRIMARY_COLOR = "#800080"
CARD_A = "#faf5ff"
CARD_B = "#f5f3ff"
BORDER = "#d8b4fe"
TEXT_MUTED = "#5b5563"

# =========================================================
# CSS
# =========================================================
st.markdown(
    f"""
    <style>
    .main {{
        padding-top: 1rem;
    }}
    .block-container {{
        max-width: 1050px;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }}
    .hero {{
        background: linear-gradient(135deg, #fdf4ff 0%, #faf5ff 50%, #f5f3ff 100%);
        border: 1px solid #e9d5ff;
        border-radius: 22px;
        padding: 28px 26px;
        margin-bottom: 24px;
    }}
    .hero h1 {{
        color: {PRIMARY_COLOR};
        margin-bottom: 0.25rem;
    }}
    .hero p {{
        color: {TEXT_MUTED};
        font-size: 1.05rem;
        margin-bottom: 0;
    }}
    .question-card {{
        border-radius: 20px;
        border: 1px solid {BORDER};
        padding: 26px 24px 16px 24px;
        margin-top: 12px;
        margin-bottom: 18px;
    }}
    .question-a {{
        background: {CARD_A};
    }}
    .question-b {{
        background: {CARD_B};
    }}
    .badge {{
        display: inline-block;
        background: {PRIMARY_COLOR};
        color: white;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 0.92rem;
        font-weight: 600;
        margin-bottom: 12px;
    }}
    .question-title {{
        font-size: 1.45rem;
        font-weight: 700;
        color: #241f2a;
        line-height: 1.45;
        margin-top: 6px;
        margin-bottom: 6px;
    }}
    .question-sub {{
        color: {TEXT_MUTED};
        font-size: 0.98rem;
        margin-bottom: 12px;
    }}
    .section-card {{
        background: #ffffff;
        border: 1px solid #ece7f2;
        border-radius: 18px;
        padding: 18px 18px 10px 18px;
        margin-bottom: 16px;
    }}
    .small-muted {{
        color: {TEXT_MUTED};
        font-size: 0.95rem;
    }}
    .kpi {{
        background: #faf5ff;
        border: 1px solid #eadcff;
        border-radius: 18px;
        padding: 12px 14px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# QUESTIONS
# =========================================================
QUESTIONS = {
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

SCALE_OPTIONS = [
    "1 - Discordo totalmente",
    "2 - Discordo",
    "3 - Neutro",
    "4 - Concordo",
    "5 - Concordo totalmente",
]

DISPLAY_LABELS = {
    "Executor": "EXECUTOR",
    "Visionario": "VISIONÁRIO",
    "Lideranca": "LIDERANÇA",
    "Relacionamento": "RELACIONAMENTO",
    "Equilibrado": "EQUILIBRADO",
    "Seguranca": "SEGURANÇA",
    "Crescimento": "CRESCIMENTO",
}

# =========================================================
# HELPERS
# =========================================================
def mean_1_to_5(values):
    return float(np.mean(values)) if values else 3.0

def to_0_100(mean_score):
    return round(((mean_score - 1) / 4) * 100, 1)

def from_answer(ans):
    return float(ans)

def rev(ans):
    return 6 - float(ans)

def avg_answers(respostas, items):
    vals = []
    for item in items:
        if isinstance(item, tuple):
            q, reverse = item
            value = respostas.get(q, 3)
            vals.append(rev(value) if reverse else from_answer(value))
        else:
            vals.append(from_answer(respostas.get(item, 3)))
    return mean_1_to_5(vals)

def level(score):
    if score >= 75:
        return "muito alto"
    if score >= 60:
        return "alto"
    if score >= 40:
        return "moderado"
    return "baixo"

def clamp(x):
    return max(0.0, min(100.0, x))

# =========================================================
# ENGINE V2
# =========================================================
def engine_v2(respostas):
    blocos = {
        "Aberto_Experiencia": list(range(1, 16)),
        "Consciencioso": list(range(16, 28)),
        "Extroversao": list(range(28, 38)),
        "Amavel": list(range(38, 50)),
        "Neuroticismo": list(range(50, 62)),
        "Dinheiro_Seguranca": list(range(62, 72)),
        "Dinheiro_Abundancia": list(range(72, 81)),
    }

    medias_bloco = {
        nome: mean_1_to_5([respostas[i] for i in perguntas])
        for nome, perguntas in blocos.items()
    }
    scores_bloco = {k: to_0_100(v) for k, v in medias_bloco.items()}

    # Sinais complementares com base no conteúdo das perguntas
    disciplina_signal = to_0_100(avg_answers(respostas, [2, 7, 12, 17, 21, 24, 42, 45, 49, 64, 71, 74]))
    criatividade_signal = to_0_100(avg_answers(respostas, [1, 9, 15, 16, 25, 38, 41, 44, 47, 61, 69]))
    sociabilidade_signal = to_0_100(avg_answers(respostas, [3, 11, 23, 30, 53, 55]))
    influencia_signal = to_0_100(avg_answers(respostas, [39, 43, 46, 48, 51, 53, 55]))
    empatia_signal = to_0_100(avg_answers(respostas, [4, 8, 14, 20, 52, 57, 58, 60]))
    pressao_signal = to_0_100(avg_answers(respostas, [5, 10, 13, 29, 31, 35, 37, 50, 65, 67, 70, 75]))
    resiliencia_signal = to_0_100(avg_answers(respostas, [28, 32, 34, 36, (29, True), (31, True), (37, True)]))
    seguranca_fin_signal = to_0_100(avg_answers(respostas, [72, 74, 77, (80, True)]))
    crescimento_fin_signal = to_0_100(avg_answers(respostas, [63, 68, 69, 71, 78, 79, (70, True)]))

    # Dimensões finais exibidas
    executor = clamp((scores_bloco["Consciencioso"] * 0.70) + (disciplina_signal * 0.30))
    visionario = clamp((scores_bloco["Aberto_Experiencia"] * 0.65) + (criatividade_signal * 0.35))
    equilibrado = clamp((100 - scores_bloco["Neuroticismo"]) * 0.70 + (resiliencia_signal * 0.30))
    relacionamento = clamp((scores_bloco["Amavel"] * 0.65) + (empatia_signal * 0.35))
    seguranca = clamp((scores_bloco["Dinheiro_Seguranca"] * 0.70) + (seguranca_fin_signal * 0.30))
    crescimento = clamp((scores_bloco["Dinheiro_Abundancia"] * 0.65) + (crescimento_fin_signal * 0.35))

    # Liderança precisa de combinação real, não só extroversão
    lideranca_base = (
        scores_bloco["Extroversao"] * 0.25
        + influencia_signal * 0.35
        + executor * 0.20
        + equilibrado * 0.20
    )
    lideranca = lideranca_base
    if influencia_signal < 50:
        lideranca -= 10
    if executor < 50:
        lideranca -= 8
    if equilibrado < 45:
        lideranca -= 8
    if sociabilidade_signal < 40 and scores_bloco["Extroversao"] < 50:
        lideranca -= 6
    lideranca = clamp(lideranca)

    capacidades = {
        "Executor": round(executor, 1),
        "Visionario": round(visionario, 1),
        "Lideranca": round(lideranca, 1),
        "Relacionamento": round(relacionamento, 1),
        "Equilibrado": round(equilibrado, 1),
        "Seguranca": round(seguranca, 1),
        "Crescimento": round(crescimento, 1),
    }

    # Principal e secundário: exclui EQUILIBRADO do papel central
    principais = {k: v for k, v in capacidades.items() if k != "Equilibrado"}
    prioridade = {
        "Executor": 1,
        "Visionario": 2,
        "Lideranca": 3,
        "Relacionamento": 4,
        "Crescimento": 5,
        "Seguranca": 6,
    }

    ordenados = sorted(principais.items(), key=lambda x: (-x[1], prioridade[x[0]]))
    principal = ordenados[0][0]
    secundario = ordenados[1][0]

    # Conflitos e leituras
    conflitos = []
    if crescimento >= 60 and seguranca >= 60:
        conflitos.append("Você tende a querer crescer, mas prefere avançar com base sólida e previsibilidade.")
    if executor >= 65 and equilibrado < 45:
        conflitos.append("Você pode funcionar bem por fora e, ainda assim, carregar sobrecarga por dentro.")
    if relacionamento >= 60 and lideranca < 45:
        conflitos.append("Você tende a se conectar bem com pessoas, mas não necessariamente gosta de ocupar espaço de comando.")
    if visionario >= 60 and executor < 45:
        conflitos.append("Você pode ter boas ideias, mas às vezes sente dificuldade em transformar tudo em execução contínua.")
    if seguranca >= 65 and crescimento < 45:
        conflitos.append("A necessidade de proteção pode reduzir movimento, teste e expansão.")
    if lideranca >= 60 and relacionamento < 45:
        conflitos.append("Você pode se posicionar com força, mas correr o risco de soar mais firme do que acolhedor.")

    pontos_atencao = []
    if equilibrado < 40:
        pontos_atencao.append("Sua energia interna pode oscilar mais do que os outros percebem.")
    if executor < 45:
        pontos_atencao.append("Organização e cadência podem variar mais do que o ideal.")
    if seguranca < 40 and crescimento > 60:
        pontos_atencao.append("O desejo de avançar pode superar cautela financeira em alguns momentos.")
    if relacionamento < 40:
        pontos_atencao.append("Você pode priorizar resultado e autonomia acima de calor relacional.")
    if lideranca < 40 and executor >= 60:
        pontos_atencao.append("Você tende a funcionar melhor construindo do que aparecendo.")

    # Textos-base
    base_funcionamento = {
        "Executor": "Você tende a funcionar melhor quando há estrutura, sequência e clareza. Seu padrão natural busca organizar, sustentar e entregar. Você não depende de improviso constante para se mover bem. Quando sabe o que precisa ser feito, tende a ganhar força na constância.",
        "Visionario": "Você tende a funcionar melhor quando há novidade, possibilidade e espaço mental para explorar. Seu padrão se fortalece quando pode conectar ideias, imaginar caminhos e enxergar o que ainda não está pronto. Rotina demais pode fazer sua energia cair.",
        "Lideranca": "Você tende a funcionar melhor quando percebe espaço para influenciar, orientar e dar direção. Sua energia cresce quando existe propósito, decisão e impacto visível. Liderança aqui não significa palco, e sim capacidade de mobilizar e conduzir com firmeza.",
        "Relacionamento": "Você tende a funcionar melhor quando existe vínculo, confiança e cooperação. Seu padrão busca entendimento humano, harmonia e construção de relações consistentes. Você costuma render melhor em ambientes onde pessoas importam de verdade.",
        "Crescimento": "Você tende a funcionar melhor quando sente movimento, expansão e possibilidade concreta de avanço. Seu padrão se anima com progresso, novas oportunidades e percepção de futuro. Quando tudo fica excessivamente estático, sua motivação tende a cair.",
        "Seguranca": "Você tende a funcionar melhor quando existe previsibilidade, base sólida e sensação de proteção. Seu padrão valoriza prudência, reserva e clareza antes de avançar. Você não gosta de sentir que está andando no escuro."
    }

    secundario_text = {
        "Executor": "Além disso, existe em você uma segunda força importante: a capacidade de organizar e transformar intenção em ação consistente.",
        "Visionario": "Além disso, existe em você uma segunda força importante: a capacidade de imaginar possibilidades, conectar ideias e enxergar caminhos não óbvios.",
        "Lideranca": "Além disso, existe em você uma segunda força importante: a tendência de influenciar, orientar e assumir direção quando percebe sentido nisso.",
        "Relacionamento": "Além disso, existe em você uma segunda força importante: a habilidade de criar confiança, acolher e sustentar conexões.",
        "Crescimento": "Além disso, existe em você uma segunda força importante: o impulso de avançar, experimentar e ampliar resultados.",
        "Seguranca": "Além disso, existe em você uma segunda força importante: a capacidade de preservar, proteger e construir base antes de arriscar."
    }

    equilibrio_text = (
        "Por dentro, você tende a reagir com boa estabilidade. Isso não significa ausência de emoção, mas sim uma capacidade maior de voltar ao centro e não ser carregado com tanta facilidade pelo momento."
        if equilibrado >= 65 else
        "Por dentro, você tende a alternar estabilidade e pressão. Em vários contextos você funciona bem, mas pode carregar preocupação silenciosa, autocobrança ou desgaste interno sem mostrar tudo isso por fora."
        if equilibrado >= 45 else
        "Por dentro, você tende a sentir bastante o impacto das situações. Isso pode aparecer como preocupação, ansiedade antecipatória, sensibilidade a crítica ou peso interno acumulado. O desafio aqui não é falta de força, e sim excesso de carga emocional."
    )

    dinheiro_text = (
        "Seu jeito com dinheiro mostra uma combinação de expansão e prudência. Você tende a querer crescer, mas não gosta de crescer sem base. Quando essa combinação está bem ajustada, ela se torna uma vantagem poderosa: você avança sem perder o senso de proteção."
        if crescimento >= 60 and seguranca >= 60 else
        "Seu jeito com dinheiro tende a priorizar segurança. Você valoriza reserva, previsibilidade e proteção emocional ligada a recursos. Seu próximo salto costuma vir quando você consegue crescer sem sentir que está abandonando a base."
        if seguranca > crescimento else
        "Seu jeito com dinheiro tende a priorizar movimento e crescimento. Você se energiza mais com expansão, oportunidade e circulação do que com pura retenção. Seu desafio é garantir que crescimento venha junto com estrutura."
    )

    # Forças
    strengths_bank = []
    if executor >= 60:
        strengths_bank += [
            "Capacidade de manter constância mesmo quando a motivação oscila.",
            "Boa tendência a organizar tarefas, prioridades e compromissos.",
            "Maior chance de transformar intenção em execução concreta."
        ]
    if visionario >= 60:
        strengths_bank += [
            "Facilidade para enxergar possibilidades antes de elas ficarem óbvias.",
            "Capacidade criativa para conectar ideias e imaginar caminhos novos.",
            "Curiosidade intelectual que favorece aprendizado e adaptação."
        ]
    if lideranca >= 60:
        strengths_bank += [
            "Capacidade de influenciar e orientar quando percebe direção clara.",
            "Tendência a assumir responsabilidade em momentos decisivos.",
            "Presença que pode ajudar outras pessoas a ganharem foco."
        ]
    if relacionamento >= 60:
        strengths_bank += [
            "Facilidade para gerar confiança e conexão humana consistente.",
            "Tendência a cooperar sem perder sensibilidade ao outro.",
            "Capacidade de sustentar vínculos com lealdade e presença."
        ]
    if equilibrado >= 60:
        strengths_bank += [
            "Maior estabilidade diante de pressão, crítica e mudança.",
            "Capacidade de recuperar centro emocional com mais facilidade.",
            "Menor tendência a reagir de forma impulsiva a curto prazo."
        ]
    if seguranca >= 60:
        strengths_bank += [
            "Prudência útil para evitar decisões precipitadas.",
            "Maior atenção a base, reserva e proteção antes de avançar.",
            "Capacidade de pensar em sustentabilidade, não só em impulso."
        ]
    if crescimento >= 60:
        strengths_bank += [
            "Impulso natural para buscar expansão, avanço e oportunidade.",
            "Facilidade para perceber movimento e potencial onde outros não enxergam.",
            "Tendência a querer evoluir em vez de permanecer parado."
        ]
    if len(strengths_bank) < 8:
        strengths_bank += [
            "Capacidade de observar contexto antes de agir.",
            "Boa chance de funcionar com autonomia quando há clareza.",
            "Tendência a aprender com experiência e ajustar rota.",
            "Senso prático que ajuda a ligar ideia e realidade."
        ]
    strengths_bank = strengths_bank[:12]

    # Desafios
    challenges_bank = []
    if equilibrado < 45:
        challenges_bank += [
            "Você pode carregar preocupações por mais tempo do que gostaria. Caminho: criar descarregadores emocionais regulares, como escrita, conversa ou revisão semanal.",
            "A crítica pode pesar mais do que aparenta. Caminho: separar feedback pontual de identidade pessoal.",
        ]
    if executor < 50:
        challenges_bank += [
            "Sua execução pode variar conforme contexto, clareza ou energia. Caminho: reduzir complexidade e usar blocos curtos de ação.",
        ]
    if lideranca < 50 and relacionamento >= 60:
        challenges_bank += [
            "Você pode se conectar bem com pessoas, mas evitar exposição ou comando. Caminho: praticar posicionamento em doses pequenas e frequentes.",
        ]
    if seguranca >= 60 and crescimento >= 60:
        challenges_bank += [
            "Pode haver conflito entre querer avançar e precisar se sentir protegido. Caminho: usar testes controlados em vez de tudo ou nada.",
        ]
    if visionario >= 60 and executor < 55:
        challenges_bank += [
            "Ideias podem surgir mais rápido do que a consolidação delas. Caminho: escolher menos frentes e finalizar mais.",
        ]
    if crescimento > 60 and seguranca < 45:
        challenges_bank += [
            "A vontade de avançar pode te levar a subestimar risco ou base. Caminho: criar uma regra mínima de proteção antes de cada passo maior.",
        ]
    if relacionamento < 45:
        challenges_bank += [
            "Você pode priorizar eficiência e autonomia a ponto de parecer distante. Caminho: tornar intenção relacional mais visível no comportamento.",
        ]
    if len(challenges_bank) < 8:
        challenges_bank += [
            "Você pode subutilizar forças que já possui. Caminho: nomear o que funciona e repetir com intenção.",
            "Pode esperar confiança total para agir. Caminho: agir com clareza suficiente, não com certeza absoluta.",
            "Pode carregar sozinho responsabilidades demais. Caminho: redistribuir, pedir apoio ou simplificar decisões."
        ]
    challenges_bank = challenges_bank[:10]

    # Plano de 90 dias
    plan_90 = []
    if principal == "Executor":
        plan_90 += [
            "Mapeie suas 3 prioridades mais importantes e transforme cada uma em rotina semanal visível.",
            "Elimine frentes paralelas que roubam foco sem entregar resultado real.",
            "Escolha um processo da sua vida que hoje depende da sua memória e transforme em sistema."
        ]
    elif principal == "Visionario":
        plan_90 += [
            "Escolha uma única ideia promissora e leve até validação prática antes de abrir novas frentes.",
            "Crie um bloco semanal fixo para registrar ideias e outro bloco separado para executar apenas o que foi escolhido.",
            "Defina critérios objetivos para decidir o que merece continuidade."
        ]
    elif principal == "Lideranca":
        plan_90 += [
            "Assuma uma frente concreta onde você possa orientar, organizar ou dar direção com clareza.",
            "Pratique comunicação curta e direta em contextos reais, não só em intenção.",
            "Garanta que sua influência venha acompanhada de cadência e exemplo."
        ]
    elif principal == "Relacionamento":
        plan_90 += [
            "Fortaleça 5 vínculos que podem sustentar sua vida ou seus projetos nos próximos meses.",
            "Transforme cuidado e conexão em acordos mais claros, para não depender só da boa vontade.",
            "Escolha uma conversa importante que vem sendo adiada e conduza com presença e verdade."
        ]
    elif principal == "Crescimento":
        plan_90 += [
            "Defina uma meta concreta de expansão e quebre em 3 marcos mensais.",
            "Escolha um indicador simples para medir avanço real, não só sensação de movimento.",
            "Conecte crescimento a estrutura, para evitar dispersão ou impulso solto."
        ]
    elif principal == "Seguranca":
        plan_90 += [
            "Reforce sua base: reserva, clareza de prioridades e previsibilidade do essencial.",
            "Escolha um risco pequeno e controlado para provar a si mesmo que proteção não precisa significar imobilidade.",
            "Transforme prudência em estratégia, não em freio automático."
        ]

    if equilibrado < 45:
        plan_90.append("Crie um ritual semanal de descarrego mental: escrever preocupações, revisar o que é real e eliminar ruído.")
    elif equilibrado >= 65:
        plan_90.append("Use sua estabilidade como vantagem consciente: decida sob clareza e não desperdice esse recurso emocional.")

    if seguranca >= 60 and crescimento >= 60:
        plan_90.append("Monte um plano com dois trilhos: um de proteção e outro de expansão, para crescer sem perder paz.")

    principal_text = base_funcionamento[principal]
    secondary_text = secundario_text[secundario]

    retrato_completo = (
        f"No conjunto, você tende a se mover a partir de uma combinação de {DISPLAY_LABELS[principal]} "
        f"com {DISPLAY_LABELS[secundario]}. Isso sugere alguém que não funciona de forma aleatória: existe um padrão relativamente claro na sua forma de pensar, agir e decidir. "
        f"O fator emocional entra como moderador importante, porque seu nível atual de {DISPLAY_LABELS['Equilibrado']} está em {level(equilibrado)}. "
        f"Seu retrato final não aponta para uma pessoa de um único rótulo, mas para uma combinação de forças que, quando bem usadas, podem gerar muita consistência, clareza e crescimento."
    )

    metric_table = pd.DataFrame([
        {"Dimensão": DISPLAY_LABELS["Executor"], "Score": capacidades["Executor"], "Nível": level(capacidades["Executor"])},
        {"Dimensão": DISPLAY_LABELS["Visionario"], "Score": capacidades["Visionario"], "Nível": level(capacidades["Visionario"])},
        {"Dimensão": DISPLAY_LABELS["Lideranca"], "Score": capacidades["Lideranca"], "Nível": level(capacidades["Lideranca"])},
        {"Dimensão": DISPLAY_LABELS["Relacionamento"], "Score": capacidades["Relacionamento"], "Nível": level(capacidades["Relacionamento"])},
        {"Dimensão": DISPLAY_LABELS["Equilibrado"], "Score": capacidades["Equilibrado"], "Nível": level(capacidades["Equilibrado"])},
        {"Dimensão": DISPLAY_LABELS["Seguranca"], "Score": capacidades["Seguranca"], "Nível": level(capacidades["Seguranca"])},
        {"Dimensão": DISPLAY_LABELS["Crescimento"], "Score": capacidades["Crescimento"], "Nível": level(capacidades["Crescimento"])},
    ])

    return {
        "capacidades": capacidades,
        "principal": principal,
        "secundario": secundario,
        "equilibrado": equilibrado,
        "principal_text": principal_text,
        "secondary_text": secondary_text,
        "equilibrio_text": equilibrio_text,
        "dinheiro_text": dinheiro_text,
        "conflitos": conflitos,
        "pontos_atencao": pontos_atencao,
        "strengths": strengths_bank,
        "challenges": challenges_bank,
        "plan_90": plan_90,
        "retrato_completo": retrato_completo,
        "metric_table": metric_table,
    }

# =========================================================
# CHARTS
# =========================================================
def build_radar(result):
    labels = [
        "EXECUTOR", "VISIONÁRIO", "LIDERANÇA",
        "RELACIONAMENTO", "EQUILIBRADO", "SEGURANÇA", "CRESCIMENTO"
    ]
    values = [
        result["capacidades"]["Executor"],
        result["capacidades"]["Visionario"],
        result["capacidades"]["Lideranca"],
        result["capacidades"]["Relacionamento"],
        result["capacidades"]["Equilibrado"],
        result["capacidades"]["Seguranca"],
        result["capacidades"]["Crescimento"],
    ]
    labels_closed = labels + [labels[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=labels_closed,
        fill="toself",
        line=dict(color=PRIMARY_COLOR, width=3)
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=520,
        title="🧭 Mapa das 7 dimensões"
    )
    return fig

def build_3d(result):
    vals = np.array([
        result["capacidades"]["Executor"],
        result["capacidades"]["Visionario"],
        result["capacidades"]["Lideranca"],
        result["capacidades"]["Relacionamento"],
        result["capacidades"]["Equilibrado"],
        result["capacidades"]["Seguranca"],
        result["capacidades"]["Crescimento"],
    ])
    labels = [
        "EXECUTOR", "VISIONÁRIO", "LIDERANÇA",
        "RELACIONAMENTO", "EQUILIBRADO", "SEGURANÇA", "CRESCIMENTO"
    ]
    angles = np.linspace(0, 2 * np.pi, len(vals), endpoint=False)
    x = vals * np.cos(angles)
    y = vals * np.sin(angles)
    z = np.linspace(10, 70, len(vals))

    fig = go.Figure(data=[
        go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="lines+markers+text",
            text=labels,
            textposition="top center",
            marker=dict(
                size=8,
                color=vals,
                colorscale="Purples",
                cmin=0,
                cmax=100,
            ),
            line=dict(width=6, color=PRIMARY_COLOR)
        )
    ])
    fig.update_layout(
        title="🪞 Mapa 3D interpretativo",
        height=540,
        margin=dict(l=0, r=0, t=50, b=0),
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Intensidade"
        )
    )
    return fig

# =========================================================
# EMAIL
# =========================================================
def build_email_html(email, result):
    rows = "".join([
        f"""
        <tr>
            <td style="padding:10px;border:1px solid #ddd;">{row['Dimensão']}</td>
            <td style="padding:10px;border:1px solid #ddd;text-align:center;">{row['Score']}</td>
            <td style="padding:10px;border:1px solid #ddd;text-align:center;">{row['Nível']}</td>
        </tr>
        """
        for _, row in result["metric_table"].iterrows()
    ])

    strengths = "".join([f"<li>{x}</li>" for x in result["strengths"]])
    challenges = "".join([f"<li>{x}</li>" for x in result["challenges"]])
    plan = "".join([f"<li>{x}</li>" for x in result["plan_90"]])

    conflitos_html = "".join([f"<li>{x}</li>" for x in result["conflitos"]]) or "<li>Sem tensões centrais destacadas nesta leitura inicial.</li>"
    atencao_html = "".join([f"<li>{x}</li>" for x in result["pontos_atencao"]]) or "<li>Nenhum ponto adicional de atenção destacado nesta leitura inicial.</li>"

    return f"""
    <html>
    <body style="font-family:Arial, Helvetica, sans-serif; background:#f8f5fb; color:#222; padding:24px;">
        <div style="max-width:900px; margin:auto; background:#ffffff; border:1px solid #eee; border-radius:20px; padding:28px;">
            <h1 style="color:#800080;">🪞 Mind Insight</h1>
            <p>Olá,</p>
            <p>Seu relatório foi gerado com base nas respostas do teste.</p>

            <h2 style="color:#800080;">Como você funciona no dia a dia</h2>
            <p>{result["principal_text"]}</p>

            <h2 style="color:#800080;">O que também é forte em você</h2>
            <p>{result["secondary_text"]}</p>

            <h2 style="color:#800080;">Como você reage por dentro</h2>
            <p>{result["equilibrio_text"]}</p>

            <h2 style="color:#800080;">Seu jeito com dinheiro</h2>
            <p>{result["dinheiro_text"]}</p>

            <h2 style="color:#800080;">Tabela das dimensões</h2>
            <table style="border-collapse:collapse;width:100%;">
                <thead>
                    <tr>
                        <th style="padding:10px;border:1px solid #ddd;background:#f3e8ff;">Dimensão</th>
                        <th style="padding:10px;border:1px solid #ddd;background:#f3e8ff;">Score</th>
                        <th style="padding:10px;border:1px solid #ddd;background:#f3e8ff;">Nível</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>

            <h2 style="color:#800080;">Pontos de atenção</h2>
            <ul>{atencao_html}</ul>

            <h2 style="color:#800080;">Tensões internas</h2>
            <ul>{conflitos_html}</ul>

            <h2 style="color:#800080;">Suas forças</h2>
            <ul>{strengths}</ul>

            <h2 style="color:#800080;">Seus desafios</h2>
            <ul>{challenges}</ul>

            <h2 style="color:#800080;">Plano de 90 dias</h2>
            <ul>{plan}</ul>

            <h2 style="color:#800080;">Seu retrato completo</h2>
            <p>{result["retrato_completo"]}</p>

            <p style="margin-top:24px;color:#666;">Relatório Mind Insight</p>
        </div>
    </body>
    </html>
    """

def send_report(email, result):
    try:
        smtp_user = st.secrets["SMTP_USER"]
        smtp_password = st.secrets["SMTP_PASSWORD"]
        smtp_from = st.secrets["SMTP_FROM"]
    except Exception:
        return False, "Secrets SMTP não configuradas."

    try:
        msg = EmailMessage()
        msg["Subject"] = "🪞 Seu relatório Mind Insight"
        msg["From"] = smtp_from
        msg["To"] = email
        msg.set_content("Seu cliente de email não suporta HTML.")
        msg.add_alternative(build_email_html(email, result), subtype="html")

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        return True, "Relatório enviado com sucesso."
    except Exception as e:
        return False, f"Erro ao enviar email: {e}"

# =========================================================
# SESSION STATE
# =========================================================
if "stage" not in st.session_state:
    st.session_state.stage = "intro"

if "email" not in st.session_state:
    st.session_state.email = ""

if "current_q" not in st.session_state:
    st.session_state.current_q = 1

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "result" not in st.session_state:
    st.session_state.result = None

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.title("🪞 Mind Insight")
    if st.session_state.stage == "quiz":
        progress = (st.session_state.current_q - 1) / 80
        st.progress(progress)
        st.metric("Pergunta atual", f"{st.session_state.current_q}/80")
        st.caption("Escala: 1 = Discordo totalmente | 5 = Concordo totalmente")
    elif st.session_state.stage == "results":
        st.success("Teste concluído")
        st.metric("Respostas", "80/80")

# =========================================================
# INTRO
# =========================================================
if st.session_state.stage == "intro":
    st.markdown(
        """
        <div class="hero">
            <h1>🪞 Mind Insight</h1>
            <p>
                Um web app de autoconhecimento com 80 perguntas, 7 dimensões comportamentais,
                leitura integrada do seu padrão e um plano de evolução de 90 dias.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1.2, 1, 1])
    with c1:
        st.markdown("### O que você vai receber")
        st.markdown(
            """
            - leitura mais profunda da sua forma de funcionar  
            - forças e desafios mais prováveis  
            - mapa das 7 dimensões  
            - plano de 90 dias  
            - opção de envio por email
            """
        )
    with c2:
        st.markdown("### Tempo")
        st.info("⏱ Cerca de 6 a 10 minutos")
    with c3:
        st.markdown("### Privacidade")
        st.info("🔒 Respostas mostradas apenas na sua sessão")

    st.markdown("### 📧 Informe seu email")
    email_value = st.text_input(
        "Email",
        value=st.session_state.email,
        placeholder="seunome@email.com",
    )

    if st.button("🚀 Começar teste", type="primary", use_container_width=True):
        if not email_value or "@" not in email_value:
            st.error("Informe um email válido para continuar.")
        else:
            st.session_state.email = email_value.strip()
            st.session_state.stage = "quiz"
            st.session_state.current_q = 1
            st.session_state.answers = {}
            st.session_state.result = None
            st.rerun()

# =========================================================
# QUIZ
# =========================================================
elif st.session_state.stage == "quiz":
    q = st.session_state.current_q
    card_class = "question-a" if q % 2 == 1 else "question-b"

    st.markdown(
        f"""
        <div class="question-card {card_class}">
            <div class="badge">Pergunta {q} de 80</div>
            <div class="question-title">{QUESTIONS[q]}</div>
            <div class="question-sub">Escolha a alternativa que mais combina com você neste momento.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    previous_answer = st.session_state.answers.get(q)
    radio_index = previous_answer - 1 if previous_answer is not None else None

    selected = st.radio(
        "Sua resposta",
        SCALE_OPTIONS,
        index=radio_index,
        key=f"radio_q_{q}",
        horizontal=True,
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Anterior", use_container_width=True, disabled=(q == 1)):
            if selected:
                st.session_state.answers[q] = int(selected.split(" - ")[0])
            st.session_state.current_q -= 1
            st.rerun()

    with col2:
        next_label = "✅ Finalizar" if q == 80 else "➡️ Próxima"
        if st.button(next_label, type="primary", use_container_width=True):
            if not selected:
                st.warning("Escolha uma resposta antes de continuar.")
            else:
                st.session_state.answers[q] = int(selected.split(" - ")[0])

                if q < 80:
                    st.session_state.current_q += 1
                    st.rerun()
                else:
                    with st.spinner("Analisando seu retrato comportamental..."):
                        st.session_state.result = engine_v2(st.session_state.answers)
                    st.session_state.stage = "results"
                    st.balloons()
                    st.rerun()

# =========================================================
# RESULTS
# =========================================================
elif st.session_state.stage == "results":
    result = st.session_state.result

    st.title("📊 Seu resultado")
    st.markdown("Leitura baseada nas 7 dimensões e na combinação entre seus traços mais fortes.")

    k1, k2, k3 = st.columns(3)
    with k1:
        st.metric("Como você funciona no dia a dia", DISPLAY_LABELS[result["principal"]])
    with k2:
        st.metric("O que também é forte em você", DISPLAY_LABELS[result["secundario"]])
    with k3:
        st.metric("Como você reage por dentro", f'{DISPLAY_LABELS["Equilibrado"]} • {level(result["equilibrado"])}')

    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(build_radar(result), use_container_width=True)
    with c2:
        st.plotly_chart(build_3d(result), use_container_width=True)

    st.markdown("### 🧠 Como você funciona no dia a dia")
    st.markdown(result["principal_text"])

    st.markdown("### 💡 O que também é forte em você")
    st.markdown(result["secondary_text"])

    st.markdown("### 🧘 Como você reage por dentro")
    st.markdown(result["equilibrio_text"])

    st.markdown("### 💰 Seu jeito com dinheiro")
    st.markdown(result["dinheiro_text"])

    if result["pontos_atencao"]:
        st.markdown("### ⚠️ Pontos de atenção")
        for item in result["pontos_atencao"]:
            st.markdown(f"- {item}")

    if result["conflitos"]:
        st.markdown("### 🔄 Tensões internas detectadas")
        for item in result["conflitos"]:
            st.markdown(f"- {item}")

    st.markdown("### 💪 Suas forças")
    for item in result["strengths"]:
        st.markdown(f"- {item}")

    st.markdown("### 🚧 Seus desafios")
    for item in result["challenges"]:
        st.markdown(f"- {item}")

    st.markdown("### 🚀 Plano de 90 dias")
    for item in result["plan_90"]:
        st.markdown(f"- {item}")

    st.markdown("### 🪞 Seu retrato completo")
    st.markdown(result["retrato_completo"])

    st.markdown("### 📋 Tabela das 7 dimensões")
    st.dataframe(result["metric_table"], use_container_width=True, hide_index=True)

    st.markdown("---")
    col_send, col_restart = st.columns(2)

    with col_send:
        if st.button("📧 Enviar relatório por email", type="primary", use_container_width=True):
            ok, msg = send_report(st.session_state.email, result)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

    with col_restart:
        if st.button("🔄 Fazer novo teste", use_container_width=True):
            st.session_state.stage = "intro"
            st.session_state.current_q = 1
            st.session_state.answers = {}
            st.session_state.result = None
            st.rerun()

st.markdown("---")
st.caption("Mind Insight • Engine V2")
