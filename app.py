import streamlit as st
import os
from datetime import datetime, date, timedelta
import time

# Page config
st.set_page_config(
    page_title="BeautyFlix",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

/* ── LIGHT MODE (default) ── */
:root, html[data-theme="light"], html:not([data-theme="dark"]) {
  --text: #1A1118;
  --text-secondary: #5A4A55;
  --card-bg: #ffffff;
  --card-border: #F0E4DA;
  --input-label: #1A1118;
  --info-bg: #FFF5F7;
  --success-bg: #F0FFF4;
  --divider: #F0E4DA;
}

/* ── DARK MODE — Streamlit sets data-theme on <html> ── */
html[data-theme="dark"] {
  --text: #F0E8F4 !important;
  --text-secondary: #C8B8D0 !important;
  --card-bg: #1E1525 !important;
  --card-border: #3D2A4A !important;
  --input-label: #F0E8F4 !important;
  --info-bg: #2A1520 !important;
  --success-bg: #0D2318 !important;
  --divider: #3D2A4A !important;
}

html, body, .stApp {
  font-family: 'DM Sans', sans-serif;
}

/* Texto geral — escopo no stApp para não vazar */
.stApp, .stApp p, .stApp li, .stApp label,
.stApp .stMarkdown, .stApp .stMarkdown p,
.stApp .stMarkdown li, .stApp .stMarkdown span {
  color: var(--text) !important;
  font-family: 'DM Sans', sans-serif;
}

.stApp h1, .stApp h2, .stApp h3 {
  font-family: 'Playfair Display', serif;
  color: var(--text) !important;
}

.main-header {
  background: linear-gradient(135deg, #1A1118 0%, #3D1F2E 60%, #E8788A 100%);
  padding: 2.5rem 2rem;
  border-radius: 16px;
  margin-bottom: 2rem;
  color: white;
  text-align: center;
}

.main-header h1 {
  font-size: 3rem;
  font-weight: 700;
  letter-spacing: -1px;
  margin: 0;
  color: white !important;
}

.main-header .tagline {
  color: #F5C2CB !important;
  font-size: 1.05rem;
  margin-top: 0.3rem;
  font-style: italic;
}

.plan-card {
  background: var(--card-bg);
  border-radius: 16px;
  padding: 1.5rem;
  border: 2px solid var(--card-border);
  text-align: center;
  transition: all 0.2s;
  cursor: pointer;
  height: 100%;
  color: var(--text);
}

.plan-card h3 {
  color: var(--text) !important;
}

.plan-card li {
  color: var(--text-secondary) !important;
}

.plan-card:hover {
  border-color: #E8788A;
  box-shadow: 0 8px 24px rgba(232,120,138,0.2);
  transform: translateY(-2px);
}

.plan-card.featured {
  background: linear-gradient(145deg, #1A1118, #3D1F2E);
  border-color: #C9A96E;
  color: white !important;
}

.plan-card.featured h3,
.plan-card.featured li,
.plan-card.featured p,
.plan-card.featured small {
  color: #F5C2CB !important;
}

.plan-card h3 {
  font-size: 1.4rem;
  margin-bottom: 0.5rem;
}

.plan-price {
  font-size: 2rem;
  font-weight: 700;
  color: #E8788A !important;
}

.plan-card.featured .plan-price {
  color: #C9A96E !important;
}

.badge {
  background: #E8788A;
  color: white !important;
  padding: 0.2rem 0.7rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

.badge-gold {
  background: #C9A96E;
}

.salon-card {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 1.2rem;
  border: 1px solid var(--card-border);
  margin-bottom: 0.8rem;
  cursor: pointer;
  transition: all 0.15s;
  color: var(--text);
}

.salon-card b, .salon-card strong {
  color: var(--text) !important;
}

.salon-card small {
  color: var(--text-secondary) !important;
}

.salon-card:hover {
  border-color: #E8788A;
  box-shadow: 0 4px 12px rgba(232,120,138,0.12);
}

.metric-box {
  background: linear-gradient(135deg, #1A1118, #3D1F2E);
  color: white;
  border-radius: 12px;
  padding: 1.2rem;
  text-align: center;
}

.metric-box .value {
  font-size: 2rem;
  font-weight: 700;
  color: #C9A96E !important;
  font-family: 'Playfair Display', serif;
}

.metric-box .label {
  font-size: 0.85rem;
  color: #F5C2CB !important;
  margin-top: 0.2rem;
}

.booking-slot {
  background: var(--nude);
  border-radius: 8px;
  padding: 0.5rem 1rem;
  margin: 0.3rem;
  display: inline-block;
  cursor: pointer;
  font-size: 0.9rem;
  border: 2px solid transparent;
  transition: all 0.15s;
  color: var(--text);
}

.booking-slot:hover {
  background: #F5C2CB;
  border-color: #E8788A;
  color: #1A1118 !important;
}

.booking-slot.selected {
  background: #E8788A;
  color: white !important;
}

.status-active {
  color: #2ECC71 !important;
  font-weight: 600;
}

.status-pending {
  color: #F39C12 !important;
  font-weight: 600;
}

.divider {
  border: none;
  border-top: 1px solid var(--divider);
  margin: 1.5rem 0;
}

[data-testid="stSidebar"] {
  background: #1A1118 !important;
}

[data-testid="stSidebar"] * {
  color: white !important;
}

[data-testid="stSidebar"] .stButton > button {
  background: linear-gradient(135deg, #E8788A, #C9607A) !important;
  color: white !important;
}

.stButton > button {
  background: linear-gradient(135deg, #E8788A, #C9607A) !important;
  color: white !important;
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1.5rem;
  font-family: 'DM Sans', sans-serif;
  font-weight: 500;
  transition: all 0.2s;
}

.stButton > button:hover {
  background: linear-gradient(135deg, #C9607A, #A84060) !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(232,120,138,0.3);
  color: white !important;
}

.stButton > button p, .stButton > button span {
  color: white !important;
}

.stApp .stSelectbox label, .stApp .stDateInput label,
.stApp .stTextInput label, .stApp .stSelectbox > label,
.stApp .stDateInput > label, .stApp .stTextInput > label,
.stApp [data-testid="stWidgetLabel"] {
  font-family: 'DM Sans', sans-serif;
  font-weight: 500;
  color: var(--text) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
  color: var(--text-secondary) !important;
}
.stTabs [aria-selected="true"] {
  color: #E8788A !important;
}

/* Expander */
.streamlit-expanderHeader, [data-testid="stExpander"] summary {
  color: var(--text) !important;
}

/* Dataframe */
.stDataFrame {
  color: var(--text) !important;
}

.info-box {
  background: var(--info-bg);
  border-left: 4px solid #E8788A;
  color: var(--text);
  border-radius: 0 8px 8px 0;
  padding: 1rem 1.2rem;
  margin: 1rem 0;
}

.success-box {
  background: var(--success-bg);
  border-left: 4px solid #2ECC71;
  border-radius: 0 8px 8px 0;
  padding: 1rem 1.2rem;
  margin: 1rem 0;
  color: var(--text);
}

.info-box b, .info-box strong { color: var(--text) !important; }
.success-box b, .success-box strong { color: var(--text) !important; }

/* salon-card e plan-card: garantir herança no dark */
html[data-theme="dark"] .salon-card,
html[data-theme="dark"] .salon-card b,
html[data-theme="dark"] .salon-card strong {
  color: #F0E8F4 !important;
}
html[data-theme="dark"] .salon-card small {
  color: #C8B8D0 !important;
}
html[data-theme="dark"] .plan-card {
  color: #F0E8F4 !important;
}
html[data-theme="dark"] .plan-card h3 {
  color: #F0E8F4 !important;
}
html[data-theme="dark"] .plan-card li {
  color: #C8B8D0 !important;
}
html[data-theme="dark"] .info-box {
  color: #F0E8F4 !important;
}
html[data-theme="dark"] .info-box b,
html[data-theme="dark"] .info-box strong {
  color: #ffffff !important;
}

/* light mode explicit overrides */
html[data-theme="light"] .salon-card,
html[data-theme="light"] .salon-card b,
html[data-theme="light"] .salon-card strong,
html:not([data-theme="dark"]) .salon-card b {
  color: #1A1118 !important;
}
html[data-theme="light"] .plan-card,
html:not([data-theme="dark"]) .plan-card {
  color: #1A1118 !important;
}
</style>
""", unsafe_allow_html=True)

# --- Session State Init ---
if "user_type" not in st.session_state:
    st.session_state.user_type = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "bookings" not in st.session_state:
    st.session_state.bookings = []
if "page" not in st.session_state:
    st.session_state.page = "login"

# --- Mock Data ---
MOCK_SALONS = [
    {
        "id": 1,
        "name": "Studio Bella Joinville",
        "address": "Rua XV de Novembro, 1200 - Centro",
        "rating": 4.8,
        "distance": "0.8 km",
        "services": ["Lavagem", "Escova", "Corte", "Manicure", "Pedicure"],
        "available_today": True,
        "image_emoji": "💇‍♀️"
    },
    {
        "id": 2,
        "name": "Espaço Glam",
        "address": "Av. Beira Rio, 450 - Glória",
        "rating": 4.6,
        "distance": "1.2 km",
        "services": ["Sobrancelha", "Hidratação", "Limpeza de Pele", "Massagem"],
        "available_today": True,
        "image_emoji": "✨"
    },
    {
        "id": 3,
        "name": "Salão Elegance",
        "address": "Rua Visconde de Taunay, 800 - Anita Garibaldi",
        "rating": 4.9,
        "distance": "2.1 km",
        "services": ["Corte", "Coloração", "Escova", "Manicure", "Sobrancelha"],
        "available_today": False,
        "image_emoji": "💅"
    },
    {
        "id": 4,
        "name": "Beauty Corner",
        "address": "Rua do Príncipe, 321 - Centro",
        "rating": 4.5,
        "distance": "0.4 km",
        "services": ["Massagem", "Limpeza de Pele", "Hidratação", "Pedicure"],
        "available_today": True,
        "image_emoji": "🌸"
    },
]

MOCK_PROCEDURES = [
    "Lavagem de Cabelo", "Escova", "Corte de Cabelo",
    "Manicure", "Pedicure", "Sobrancelha",
    "Hidratação de Cabelo", "Limpeza de Pele", "Massagem Relaxante"
]

PLANS = {
    "Starter": {
        "price": 79.90,
        "procedures": 4,
        "color": "#E8788A",
        "features": ["4 procedimentos/mês", "Acesso a todos os salões", "Agendamento pelo app"],
        "featured": False,
    },
    "Plus": {
        "price": 139.90,
        "procedures": 8,
        "color": "#C9A96E",
        "features": ["8 procedimentos/mês", "Prioridade no agendamento", "Suporte prioritário", "Acesso a todos os salões"],
        "featured": True,
    },
    "Premium": {
        "price": 199.90,
        "procedures": 14,
        "color": "#7B4FBF",
        "features": ["14 procedimentos/mês", "Procedimentos ilimitados*", "Consultor pessoal", "Descontos especiais"],
        "featured": False,
    }
}

MOCK_BOOKINGS_SALON = [
    {"id": "BF001", "client": "Ana Souza", "procedure": "Escova", "date": "21/04", "time": "14:00", "status": "Confirmado", "value": 28.0},
    {"id": "BF002", "client": "Carla Lima", "procedure": "Manicure", "date": "21/04", "time": "15:30", "status": "Confirmado", "value": 22.0},
    {"id": "BF003", "client": "Júlia Mendes", "procedure": "Corte", "date": "22/04", "time": "10:00", "status": "Pendente", "value": 35.0},
    {"id": "BF004", "client": "Fernanda Costa", "procedure": "Hidratação", "date": "22/04", "time": "11:30", "status": "Confirmado", "value": 45.0},
]


# =================== PAGES ===================

def page_login():
    st.markdown("""
    <div class="main-header">
        <h1>✨ BeautyFlix</h1>
        <p class="tagline">Beleza por assinatura, do seu jeito.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("### Entrar como:")
        tab1, tab2 = st.tabs(["👩 Assinante", "💼 Salão Parceiro"])

        with tab1:
            st.markdown("**Demo — Assinante**")
            email = st.text_input("E-mail", value="ana@email.com", key="sub_email")
            senha = st.text_input("Senha", type="password", value="123456", key="sub_pass")
            if st.button("Entrar como Assinante", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.user_type = "subscriber"
                st.session_state.user_data = {
                    "name": "Ana Souza",
                    "email": email,
                    "plan": "Plus",
                    "procedures_used": 3,
                    "procedures_total": 8,
                    "member_since": "Jan 2025",
                    "next_billing": "05/05/2025",
                }
                st.session_state.page = "subscriber_home"
                st.rerun()

        with tab2:
            st.markdown("**Demo — Salão**")
            email_s = st.text_input("E-mail do salão", value="studio@bella.com", key="sal_email")
            senha_s = st.text_input("Senha", type="password", value="123456", key="sal_pass")
            if st.button("Entrar como Salão", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.user_type = "salon"
                st.session_state.user_data = {
                    "name": "Studio Bella Joinville",
                    "email": email_s,
                    "address": "Rua XV de Novembro, 1200",
                    "balance": 892.50,
                    "bookings_month": 31,
                    "rating": 4.8,
                    "services": ["Lavagem", "Escova", "Corte", "Manicure", "Pedicure"],
                }
                st.session_state.page = "salon_home"
                st.rerun()

        st.markdown("---")
        st.markdown("<center><small>Ainda não é assinante? <b>Conheça os planos ↓</b></small></center>", unsafe_allow_html=True)
        if st.button("Ver Planos BeautyFlix", use_container_width=True, key="plans_btn"):
            st.session_state.page = "plans"
            st.rerun()


def page_plans():
    st.markdown("""
    <div class="main-header">
        <h1>✨ BeautyFlix</h1>
        <p class="tagline">Escolha o plano ideal para você</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Voltar"):
        st.session_state.page = "login"
        st.rerun()

    cols = st.columns(3)
    for i, (plan_name, plan) in enumerate(PLANS.items()):
        with cols[i]:
            featured_class = "featured" if plan["featured"] else ""
            badge = '<span class="badge badge-gold">🔥 Mais Popular</span><br><br>' if plan["featured"] else "<br><br>"
            features_html = "".join([f"<li>✓ {f}</li>" for f in plan["features"]])
            st.markdown(f"""
            <div class="plan-card {featured_class}">
                {badge}
                <h3>{plan_name}</h3>
                <div class="plan-price">R$ {plan['price']:.2f}<small style="font-size:0.5em">/mês</small></div>
                <ul style="text-align:left; margin-top:1rem; padding-left:1.2rem; font-size:0.9rem">
                    {features_html}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            st.button(f"Assinar {plan_name}", key=f"plan_{plan_name}", use_container_width=True)

    st.markdown("---")
    st.markdown("### 🗺️ Salões parceiros em Joinville")
    for salon in MOCK_SALONS:
        avail = "🟢 Disponível hoje" if salon["available_today"] else "🔴 Sem horário hoje"
        st.markdown(f"""
        <div class="salon-card">
            <b>{salon['image_emoji']} {salon['name']}</b> &nbsp;
            <span class="badge">⭐ {salon['rating']}</span> &nbsp;
            <span style="color:#888; font-size:0.85rem">📍 {salon['distance']}</span><br>
            <small style="color:#888">{salon['address']}</small><br>
            <small>{avail} &nbsp;|&nbsp; {', '.join(salon['services'][:3])}...</small>
        </div>
        """, unsafe_allow_html=True)


def sidebar_subscriber():
    with st.sidebar:
        st.markdown(f"""
        <div style="color:white; padding:1rem 0">
            <div style="font-size:2rem; text-align:center">✨</div>
            <h2 style="color:#F5C2CB; font-family:'Playfair Display',serif; text-align:center; margin:0.3rem 0">BeautyFlix</h2>
            <hr style="border-color:#3D1F2E">
            <p style="color:#F5C2CB; font-size:0.85rem">Olá, <b style="color:white">{st.session_state.user_data.get('name','')}</b></p>
            <p style="color:#C9A96E; font-size:0.8rem">Plano {st.session_state.user_data.get('plan','')}</p>
        </div>
        """, unsafe_allow_html=True)

        pages = {
            "🏠 Início": "subscriber_home",
            "🔍 Buscar Salões": "search_salons",
            "📅 Meus Agendamentos": "my_bookings",
            "👤 Minha Assinatura": "subscription",
        }
        for label, pg in pages.items():
            if st.button(label, key=f"nav_{pg}", use_container_width=True):
                st.session_state.page = pg
                st.rerun()

        st.markdown("<hr style='border-color:#3D1F2E'>", unsafe_allow_html=True)
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()


def sidebar_salon():
    with st.sidebar:
        st.markdown(f"""
        <div style="color:white; padding:1rem 0">
            <div style="font-size:2rem; text-align:center">💼</div>
            <h2 style="color:#F5C2CB; font-family:'Playfair Display',serif; text-align:center; margin:0.3rem 0">Painel Salão</h2>
            <hr style="border-color:#3D1F2E">
            <p style="color:#F5C2CB; font-size:0.85rem"><b style="color:white">{st.session_state.user_data.get('name','')}</b></p>
            <p style="color:#C9A96E; font-size:0.8rem">Parceiro BeautyFlix ✓</p>
        </div>
        """, unsafe_allow_html=True)

        pages = {
            "📊 Dashboard": "salon_home",
            "📅 Agenda": "salon_schedule",
            "🔔 Reservas": "salon_bookings",
            "💰 Financeiro": "salon_financial",
            "⚙️ Serviços": "salon_services",
        }
        for label, pg in pages.items():
            if st.button(label, key=f"nav_{pg}", use_container_width=True):
                st.session_state.page = pg
                st.rerun()

        st.markdown("<hr style='border-color:#3D1F2E'>", unsafe_allow_html=True)
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()


# --- SUBSCRIBER PAGES ---

def page_subscriber_home():
    sidebar_subscriber()
    u = st.session_state.user_data
    used = u["procedures_used"]
    total = u["procedures_total"]
    remaining = total - used
    pct = int((used / total) * 100)

    st.markdown(f"""
    <div class="main-header">
        <h1>Olá, {u['name'].split()[0]}! ✨</h1>
        <p class="tagline">Você tem <b>{remaining} procedimentos</b> disponíveis este mês</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="value">{remaining}</div>
            <div class="label">Procedimentos restantes</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="value">{used}</div>
            <div class="label">Usados este mês</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="value">{len(MOCK_SALONS)}</div>
            <div class="label">Salões próximos</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"**Uso do plano este mês** — {used}/{total} procedimentos")
    st.progress(pct / 100)

    st.markdown("---")
    st.markdown("### 💅 Agendar rápido")
    col1, col2 = st.columns(2)
    with col1:
        proc = st.selectbox("Procedimento", MOCK_PROCEDURES)
    with col2:
        data = st.date_input("Data", min_value=date.today(), value=date.today())

    if st.button("🔍 Buscar Salões Disponíveis"):
        st.session_state.page = "search_salons"
        st.session_state.quick_search = {"procedure": proc, "date": data}
        st.rerun()

    st.markdown("---")
    st.markdown("### 📍 Salões em Destaque — Joinville")
    for salon in MOCK_SALONS[:2]:
        avail_color = "#2ECC71" if salon["available_today"] else "#E74C3C"
        avail_txt = "Disponível hoje" if salon["available_today"] else "Sem horário hoje"
        st.markdown(f"""
        <div class="salon-card">
            <b style="font-size:1.05rem">{salon['image_emoji']} {salon['name']}</b>
            &nbsp;<span class="badge">⭐ {salon['rating']}</span>
            <span style="float:right; color:{avail_color}; font-size:0.8rem">● {avail_txt}</span><br>
            <small style="color:#888">📍 {salon['address']} · {salon['distance']}</small><br>
            <small style="color:#666; margin-top:0.3rem; display:block">{' · '.join(salon['services'])}</small>
        </div>
        """, unsafe_allow_html=True)


def page_search_salons():
    sidebar_subscriber()
    st.markdown("## 🔍 Buscar Salões")

    col1, col2, col3 = st.columns(3)
    with col1:
        proc_filter = st.selectbox("Procedimento", ["Todos"] + MOCK_PROCEDURES)
    with col2:
        date_filter = st.date_input("Data", min_value=date.today(), value=date.today())
    with col3:
        dist_filter = st.selectbox("Distância", ["Todos", "Até 1km", "Até 2km", "Até 5km"])

    filtered = MOCK_SALONS
    if proc_filter != "Todos":
        filtered = [s for s in filtered if any(proc_filter.lower() in sv.lower() for sv in s["services"])]

    st.markdown(f"**{len(filtered)} salões encontrados**")
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    for salon in filtered:
        avail_color = "#2ECC71" if salon["available_today"] else "#E74C3C"
        avail_txt = "🟢 Disponível" if salon["available_today"] else "🔴 Sem horário"
        with st.expander(f"{salon['image_emoji']} {salon['name']}  ·  ⭐ {salon['rating']}  ·  📍 {salon['distance']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"📍 {salon['address']}")
                st.markdown(f"**Serviços:** {', '.join(salon['services'])}")
            with col2:
                st.markdown(f"<span style='color:{avail_color}'><b>{avail_txt}</b></span>", unsafe_allow_html=True)

            if salon["available_today"]:
                st.markdown("**Horários disponíveis hoje:**")
                slots = ["09:00", "10:30", "11:00", "14:00", "15:30", "17:00"]
                cols = st.columns(6)
                for i, slot in enumerate(slots):
                    with cols[i]:
                        if st.button(slot, key=f"slot_{salon['id']}_{slot}"):
                            new_booking = {
                                "id": f"BF{len(st.session_state.bookings)+100:03d}",
                                "salon": salon["name"],
                                "procedure": proc_filter if proc_filter != "Todos" else salon["services"][0],
                                "date": date_filter.strftime("%d/%m/%Y"),
                                "time": slot,
                                "status": "Confirmado",
                                "address": salon["address"],
                            }
                            st.session_state.bookings.append(new_booking)
                            st.success(f"✅ Agendado com sucesso! {salon['name']} — {date_filter.strftime('%d/%m')} às {slot}")
                            time.sleep(1)
                            st.session_state.page = "my_bookings"
                            st.rerun()


def page_my_bookings():
    sidebar_subscriber()
    st.markdown("## 📅 Meus Agendamentos")

    all_bookings = st.session_state.bookings + [
        {"id": "BF010", "salon": "Studio Bella Joinville", "procedure": "Escova", "date": "18/04/2025", "time": "14:00", "status": "Realizado", "address": "Rua XV de Novembro, 1200"},
        {"id": "BF009", "salon": "Espaço Glam", "procedure": "Sobrancelha", "date": "12/04/2025", "time": "10:30", "status": "Realizado", "address": "Av. Beira Rio, 450"},
    ]

    upcoming = [b for b in all_bookings if b["status"] == "Confirmado"]
    past = [b for b in all_bookings if b["status"] == "Realizado"]

    tab1, tab2 = st.tabs([f"🗓️ Próximos ({len(upcoming)})", f"✅ Histórico ({len(past)})"])

    with tab1:
        if not upcoming:
            st.markdown("""
            <div class="info-box">
                📭 Você não tem agendamentos próximos.<br>
                <b>Que tal agendar agora?</b>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Buscar Salões"):
                st.session_state.page = "search_salons"
                st.rerun()
        for b in upcoming:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div class="salon-card">
                    <b>💅 {b['procedure']}</b> &nbsp;
                    <span class="badge">Confirmado</span><br>
                    <small><b>{b['salon']}</b></small><br>
                    <small style="color:#888">📅 {b['date']} às {b['time']} · 📍 {b['address']}</small>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("Cancelar", key=f"cancel_{b['id']}"):
                    st.session_state.bookings = [bk for bk in st.session_state.bookings if bk["id"] != b["id"]]
                    st.rerun()

    with tab2:
        for b in past:
            st.markdown(f"""
            <div class="salon-card" style="opacity:0.7">
                <b>✅ {b['procedure']}</b><br>
                <small><b>{b['salon']}</b></small><br>
                <small style="color:#888">📅 {b['date']} às {b['time']}</small>
            </div>
            """, unsafe_allow_html=True)


def page_subscription():
    sidebar_subscriber()
    u = st.session_state.user_data
    plan = PLANS[u["plan"]]

    st.markdown("## 👤 Minha Assinatura")

    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown(f"""
        <div class="plan-card featured" style="text-align:left">
            <span class="badge badge-gold">Plano Atual</span><br><br>
            <h3 style="color:white">BeautyFlix {u['plan']}</h3>
            <div class="plan-price">R$ {plan['price']:.2f}<small style="font-size:0.5em; color:#F5C2CB">/mês</small></div>
            <hr style="border-color:#3D1F2E; margin:1rem 0">
            <p style="color:#F5C2CB; font-size:0.9rem">📅 Próxima cobrança: <b style="color:white">{u['next_billing']}</b></p>
            <p style="color:#F5C2CB; font-size:0.9rem">🗓️ Membro desde: <b style="color:white">{u['member_since']}</b></p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### Uso este mês")
        used = u["procedures_used"]
        total = u["procedures_total"]
        st.metric("Utilizados", f"{used}/{total}")
        st.progress(used / total)
        st.metric("Restantes", total - used)

    st.markdown("---")
    st.markdown("### 🔄 Mudar de Plano")
    cols = st.columns(3)
    for i, (plan_name, plan_data) in enumerate(PLANS.items()):
        with cols[i]:
            current = "✅ Atual" if plan_name == u["plan"] else ""
            st.markdown(f"""
            <div class="plan-card">
                <b>{plan_name}</b> {current}<br>
                <div class="plan-price" style="font-size:1.4rem">R$ {plan_data['price']:.2f}</div>
                <small>{plan_data['procedures']} proc./mês</small>
            </div>
            """, unsafe_allow_html=True)
            if plan_name != u["plan"]:
                if st.button(f"Mudar para {plan_name}", key=f"change_{plan_name}", use_container_width=True):
                    st.session_state.user_data["plan"] = plan_name
                    st.session_state.user_data["procedures_total"] = plan_data["procedures"]
                    st.success(f"✅ Plano alterado para {plan_name}!")
                    st.rerun()


# --- SALON PAGES ---

def page_salon_home():
    sidebar_salon()
    u = st.session_state.user_data

    st.markdown(f"""
    <div class="main-header">
        <h1>{u['name']}</h1>
        <p class="tagline">Painel Parceiro BeautyFlix · Joinville/SC</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("R$ 892,50", "Saldo a receber"),
        ("31", "Atendimentos este mês"),
        ("4.8 ⭐", "Avaliação média"),
        ("4", "Reservas hoje"),
    ]
    for col, (val, label) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-box">
                <div class="value">{val}</div>
                <div class="label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔔 Próximas Reservas")
        for b in MOCK_BOOKINGS_SALON[:3]:
            status_color = "#2ECC71" if b["status"] == "Confirmado" else "#F39C12"
            st.markdown(f"""
            <div class="salon-card">
                <b>{b['client']}</b> &nbsp;
                <span style="color:{status_color}; font-size:0.8rem">● {b['status']}</span><br>
                <small>💅 {b['procedure']} · {b['date']} às {b['time']}</small><br>
                <small style="color:#C9A96E; font-weight:600">R$ {b['value']:.2f}</small>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 📊 Desempenho do Mês")
        import random
        days = list(range(1, 22))
        vals = [random.randint(1, 5) for _ in days]
        st.bar_chart(dict(zip([str(d) for d in days], vals)), color="#E8788A")

    st.markdown("""
    <div class="info-box">
        <b>📋 Lembrete BeautyFlix:</b> Seu contrato exige mínimo de <b>2 horários/dia</b> disponíveis para assinantes. Você está cumprindo a meta hoje ✅
    </div>
    """, unsafe_allow_html=True)


def page_salon_schedule():
    sidebar_salon()
    st.markdown("## 📅 Gerenciar Agenda")

    st.markdown("""
    <div class="info-box">
        Defina os horários disponíveis para assinantes BeautyFlix. O contrato exige no mínimo <b>2 horários por dia</b>.
    </div>
    """, unsafe_allow_html=True)

    selected_date = st.date_input("Selecionar data", min_value=date.today(), value=date.today())

    st.markdown(f"### Horários para {selected_date.strftime('%d/%m/%Y')}")

    all_slots = ["08:00", "09:00", "09:30", "10:00", "10:30", "11:00",
                 "13:00", "14:00", "14:30", "15:00", "15:30", "16:00", "17:00", "18:00"]

    if "selected_slots" not in st.session_state:
        st.session_state.selected_slots = ["09:00", "14:00", "16:00"]

    st.markdown("**Clique para ativar/desativar horários:**")
    cols = st.columns(7)
    for i, slot in enumerate(all_slots):
        with cols[i % 7]:
            is_selected = slot in st.session_state.selected_slots
            btn_label = f"✅ {slot}" if is_selected else slot
            if st.button(btn_label, key=f"time_{slot}", use_container_width=True):
                if slot in st.session_state.selected_slots:
                    st.session_state.selected_slots.remove(slot)
                else:
                    st.session_state.selected_slots.append(slot)
                st.rerun()

    count = len(st.session_state.selected_slots)
    status_msg = "✅ Meta atingida" if count >= 2 else "⚠️ Adicione mais horários (mín. 2)"
    status_color = "#2ECC71" if count >= 2 else "#F39C12"

    st.markdown(f"""
    <div style="margin-top:1rem; padding:1rem; background:#F9F9F9; border-radius:8px">
        <b>Horários selecionados:</b> {', '.join(sorted(st.session_state.selected_slots)) if st.session_state.selected_slots else 'Nenhum'}<br>
        <span style="color:{status_color}"><b>{status_msg}</b> ({count} horários)</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💾 Salvar Disponibilidade", use_container_width=True):
        st.success(f"✅ Agenda salva para {selected_date.strftime('%d/%m/%Y')} com {count} horário(s)!")


def page_salon_bookings():
    sidebar_salon()
    st.markdown("## 🔔 Reservas")

    tab1, tab2 = st.tabs(["Hoje & Próximas", "Histórico"])

    with tab1:
        for b in MOCK_BOOKINGS_SALON:
            status_color = "#2ECC71" if b["status"] == "Confirmado" else "#F39C12"
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div class="salon-card">
                    <b>{b['client']}</b> &nbsp;
                    <span style="color:{status_color}; font-size:0.85rem">● {b['status']}</span><br>
                    <small>💅 <b>{b['procedure']}</b> · 📅 {b['date']} às {b['time']}</small><br>
                    <small style="color:#C9A96E; font-weight:600">Valor: R$ {b['value']:.2f}</small>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if b["status"] == "Pendente":
                    if st.button("✅ Confirmar", key=f"conf_{b['id']}", use_container_width=True):
                        st.success("Confirmado!")
                else:
                    if st.button("✔ Realizado", key=f"done_{b['id']}", use_container_width=True):
                        st.success("Marcado como realizado!")

    with tab2:
        st.markdown("*Histórico dos últimos 30 dias*")
        past = [
            {"client": "Paula Ramos", "procedure": "Manicure", "date": "15/04", "value": 22.0},
            {"client": "Mariana Silva", "procedure": "Escova", "date": "14/04", "value": 28.0},
            {"client": "Camila Ferreira", "procedure": "Corte", "date": "13/04", "value": 35.0},
        ]
        for b in past:
            st.markdown(f"""
            <div class="salon-card" style="opacity:0.8">
                ✅ <b>{b['client']}</b> · {b['procedure']} · {b['date']}
                &nbsp;<span style="color:#C9A96E; font-weight:600">R$ {b['value']:.2f}</span>
            </div>
            """, unsafe_allow_html=True)


def page_salon_financial():
    sidebar_salon()
    st.markdown("## 💰 Financeiro")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="metric-box"><div class="value">R$ 892,50</div><div class="label">Saldo disponível</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="metric-box"><div class="value">R$ 1.240,00</div><div class="label">Recebido este mês</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="metric-box"><div class="value">31</div><div class="label">Atendimentos faturados</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 Extrato de procedimentos")

    extrato = [
        {"date": "21/04", "client": "Ana Souza", "procedure": "Escova", "valor_cheio": 60.0, "taxa": 32.0, "liquido": 28.0},
        {"date": "21/04", "client": "Carla Lima", "procedure": "Manicure", "valor_cheio": 40.0, "taxa": 18.0, "liquido": 22.0},
        {"date": "20/04", "client": "Beatriz Oliveira", "procedure": "Corte", "valor_cheio": 80.0, "taxa": 45.0, "liquido": 35.0},
        {"date": "19/04", "client": "Larissa Duarte", "procedure": "Hidratação", "valor_cheio": 90.0, "taxa": 45.0, "liquido": 45.0},
    ]

    import pandas as pd
    df = pd.DataFrame(extrato)
    df.columns = ["Data", "Cliente", "Procedimento", "Valor Balcão", "Taxa Plataforma", "Valor Líquido"]
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="info-box">
        💡 <b>Como funciona:</b> A BeautyFlix negocia com a assinante o valor total do plano. Para cada procedimento realizado, 
        você recebe o <b>valor líquido</b> acordado em contrato. A taxa da plataforma cobre marketing, tecnologia e aquisição de clientes.
    </div>
    """, unsafe_allow_html=True)


def page_salon_services():
    sidebar_salon()
    st.markdown("## ⚙️ Meus Serviços")

    u = st.session_state.user_data
    current_services = u.get("services", [])

    st.markdown("### Serviços cadastrados na plataforma")
    st.markdown("*Estes são os serviços que aparecem para as assinantes na busca*")

    for svc in current_services:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"✅ **{svc}**")
        with col2:
            if st.button("Remover", key=f"rm_{svc}"):
                st.session_state.user_data["services"].remove(svc)
                st.rerun()

    st.markdown("---")
    st.markdown("### ➕ Adicionar serviço")
    available_to_add = [s for s in MOCK_PROCEDURES if s not in current_services]
    if available_to_add:
        new_svc = st.selectbox("Selecionar procedimento", available_to_add)
        if st.button("Adicionar Serviço"):
            st.session_state.user_data["services"].append(new_svc)
            st.success(f"✅ {new_svc} adicionado!")
            st.rerun()
    else:
        st.info("Você já cadastrou todos os procedimentos disponíveis.")

    st.markdown("""
    <div class="info-box">
        📋 Precisa de um procedimento não listado? Entre em contato com nossa equipe de onboarding pelo WhatsApp da plataforma.
    </div>
    """, unsafe_allow_html=True)


# =================== ROUTER ===================

def main():
    page = st.session_state.page

    if not st.session_state.logged_in:
        if page == "plans":
            page_plans()
        else:
            page_login()
        return

    # Subscriber pages
    if st.session_state.user_type == "subscriber":
        routes = {
            "subscriber_home": page_subscriber_home,
            "search_salons": page_search_salons,
            "my_bookings": page_my_bookings,
            "subscription": page_subscription,
        }
        routes.get(page, page_subscriber_home)()

    # Salon pages
    elif st.session_state.user_type == "salon":
        routes = {
            "salon_home": page_salon_home,
            "salon_schedule": page_salon_schedule,
            "salon_bookings": page_salon_bookings,
            "salon_financial": page_salon_financial,
            "salon_services": page_salon_services,
        }
        routes.get(page, page_salon_home)()


if __name__ == "__main__":
    main()
