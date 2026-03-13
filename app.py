import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import requests
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Brew Haven Café",
    page_icon="☕",
    layout="wide"
)

# --- n8n WEBHOOK URL ---
N8N_WEBHOOK_URL = "https://allexandar123.app.n8n.cloud/webhook/638b09c2-2bb7-4f2c-bae2-107b7a4e4265/chat"

# --- LOCAL PROXY SERVER (bypasses CORS) ---
PROXY_PORT = 8502

class ChatProxyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            r = requests.post(
                N8N_WEBHOOK_URL,
                data=body,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )

            self.send_response(r.status_code)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(r.content)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def log_message(self, format, *args):
        pass  # Suppress console logs

def start_proxy():
    try:
        server = HTTPServer(('127.0.0.1', PROXY_PORT), ChatProxyHandler)
        server.serve_forever()
    except OSError:
        pass  # Port already in use (proxy already running)

if 'proxy_started' not in st.session_state:
    st.session_state.proxy_started = True
    thread = threading.Thread(target=start_proxy, daemon=True)
    thread.start()

# --- CLEAN DARK THEME CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

.stApp {
    background: #111 !important;
    font-family: 'Inter', sans-serif !important;
}
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    color: #ddd !important;
}

[data-testid="stSidebar"] {
    background: #181818 !important;
    border-right: 1px solid #222 !important;
}
[data-testid="stSidebar"] * { color: #ccc !important; }

h1, h2, h3, [data-testid="stHeadingWithActionElements"] {
    color: #fff !important;
    font-weight: 700 !important;
}

.hero-title {
    font-size: 3.2rem;
    font-weight: 800;
    text-align: center;
    color: #fff;
    margin-bottom: 4px;
}
.hero-sub {
    text-align: center;
    font-size: 1.1rem;
    color: #999 !important;
    font-weight: 400;
    letter-spacing: 1px;
}

.coffee-card {
    background: #1a1a1a;
    padding: 0;
    border-radius: 14px;
    text-align: center;
    border: 1px solid #2a2a2a;
    transition: all 0.3s ease;
    margin-bottom: 16px;
    overflow: hidden;
}
.coffee-card:hover {
    transform: translateY(-6px);
    border-color: #CBA258;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}
.coffee-card img {
    width: 100%;
    height: 180px;
    object-fit: cover;
    display: block;
}
.coffee-card .card-body {
    padding: 18px 16px;
}
.coffee-card h4 { color: #fff !important; font-weight: 600; margin-bottom: 6px; font-size: 1.05rem; }
.coffee-card p { color: #999 !important; font-size: 0.85rem; line-height: 1.4; margin: 0; }
.price {
    font-size: 20px !important;
    font-weight: 700 !important;
    color: #CBA258 !important;
    margin-top: 10px;
}

.stButton, .stButton > div {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
}
.stButton > button {
    background: #CBA258 !important;
    color: #111 !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 12px 32px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    max-width: 280px !important;
    width: 100% !important;
    transition: all 0.25s ease !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: #d4b56c !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(203,162,88,0.3) !important;
}

.order-box {
    background: #1a1a1a;
    padding: 28px;
    border-radius: 14px;
    border: 1px solid #2a2a2a;
}

.stSelectbox > div > div {
    background: #1a1a1a !important;
    border: 1px solid #333 !important;
    border-radius: 10px !important;
    color: #ddd !important;
}
.stSelectbox label { color: #aaa !important; font-weight: 500 !important; }

hr { border-color: #222 !important; }
p, span, li { color: #bbb !important; }

[data-testid="stImage"] img { border-radius: 12px !important; }

[data-testid="stPlotlyChart"] {
    background: #1a1a1a !important;
    border-radius: 14px !important;
    border: 1px solid #2a2a2a !important;
    padding: 12px !important;
}

[data-testid="stNotification"] {
    background: rgba(203,162,88,0.1) !important;
    border-left-color: #CBA258 !important;
    border-radius: 8px !important;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #111; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }

</style>
""", unsafe_allow_html=True)

# --- MENU DATA ---
MENU = {
    "Hot Coffee": [
        {
            "name": "Caffe Latte",
            "price": 4.95,
            "desc": "Rich espresso and steamed milk.",
            "img": "https://images.unsplash.com/photo-1570968915860-54d5c301fa9f?w=400&h=300&fit=crop"
        },
        {
            "name": "Cappuccino",
            "price": 4.75,
            "desc": "Dark espresso under a thick layer of foam.",
            "img": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=400&h=300&fit=crop"
        },
        {
            "name": "Caramel Macchiato",
            "price": 5.45,
            "desc": "Vanilla syrup, milk, and espresso topped with caramel.",
            "img": "https://images.unsplash.com/photo-1485808191679-5f86510681a2?w=400&h=300&fit=crop"
        }
    ],
    "Cold Coffee": [
        {
            "name": "Cold Brew",
            "price": 4.25,
            "desc": "Slow-steeped for 20 hours.",
            "img": "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?w=400&h=300&fit=crop"
        },
        {
            "name": "Iced Americano",
            "price": 3.95,
            "desc": "Espresso shots topped with cold water.",
            "img": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&h=300&fit=crop"
        }
    ],
    "Pastries": [
        {
            "name": "Butter Croissant",
            "price": 3.45,
            "desc": "Flaky and golden.",
            "img": "https://images.unsplash.com/photo-1555507036-ab1f4038024a?w=400&h=300&fit=crop"
        },
        {
            "name": "Cheese Danish",
            "price": 3.95,
            "desc": "Sweet cream cheese filling.",
            "img": "https://images.unsplash.com/photo-1509365390695-33aee754301f?w=400&h=300&fit=crop"
        }
    ]
}

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://www.pngall.com/wp-content/uploads/13/Starbucks-Logo-PNG-File.png", width=100)
    st.markdown("## Brew Haven")
    page = st.radio(
        "Navigate",
        ["🏠 Home", "☕ Menu", "🛒 Order Now", "📊 Dashboard"]
    )

# --- HOME PAGE ---
if page == "🏠 Home":
    st.markdown('<h1 class="hero-title">Brew Haven Café</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Handcrafted coffee · Premium experience</p>', unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("https://images.unsplash.com/photo-1495474472287-4d71bcdd2085", use_container_width=True)
    with col2:
        st.markdown("### Our Coffee Philosophy")
        st.write("""
        At Brew Haven, we believe coffee is more than a drink.  
        It's an experience crafted from the finest beans, roasted 
        to perfection and served with passion.
        """)
        st.button("Explore Menu")

# --- MENU PAGE ---
elif page == "☕ Menu":
    st.title("Our Menu")
    for category, items in MENU.items():
        st.subheader(category)
        cols = st.columns(3)
        for i, item in enumerate(items):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="coffee-card">
                    <img src="{item['img']}" alt="{item['name']}" />
                    <div class="card-body">
                        <h4>{item['name']}</h4>
                        <p>{item['desc']}</p>
                        <p class="price">${item['price']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# --- ORDER PAGE ---
elif page == "🛒 Order Now":
    st.title("Place Your Order")
    col1, col2 = st.columns([1, 1])
    with col1:
        drink = st.selectbox("Select Drink", [item['name'] for cat in MENU.values() for item in cat])
        size = st.selectbox("Choose Size", ["Tall", "Grande", "Venti"])
        milk = st.selectbox("Milk Option", ["Whole Milk", "Oat Milk", "Almond Milk", "Soy Milk"])
    with col2:
        st.markdown('<div class="order-box">', unsafe_allow_html=True)
        st.subheader("Your Order")
        st.write(f"**Drink:** {drink}")
        st.write(f"**Size:** {size}")
        st.write(f"**Milk:** {milk}")
        st.divider()
        if st.button("Place Order ☕"):
            st.success("Your order has been placed!")
            st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)

# --- DASHBOARD PAGE ---
elif page == "📊 Dashboard":
    st.title("Store Analytics")
    df = pd.DataFrame({
        'Drink': ['Latte', 'Cold Brew', 'Mocha', 'Tea'],
        'Orders': [120, 200, 150, 80]
    })
    fig = px.pie(
        df, values="Orders", names="Drink", hole=0.45,
        color_discrete_sequence=["#CBA258", "#f0d89a", "#a07c3a", "#7a5c2e"]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=16, color="#ddd"), legend=dict(font=dict(color="#bbb"))
    )
    st.plotly_chart(fig, use_container_width=True)

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption("Brew Haven Café | Premium Coffee Experience")

# =====================================================================
# FLOATING CHATBOT WIDGET — uses local proxy to bypass CORS
# =====================================================================
chatbot_html = f"""
<script>
(function() {{
    if (window.parent.document.getElementById('brewChatToggle')) return;

    const parentDoc = window.parent.document;
    const PROXY_URL = "http://localhost:{PROXY_PORT}";

    const style = parentDoc.createElement('style');
    style.textContent = `
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        #brewChatToggle {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            width: 58px;
            height: 58px;
            border-radius: 50%;
            background: #CBA258;
            border: none;
            cursor: pointer;
            z-index: 999999;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 16px rgba(203,162,88,0.4);
            transition: all 0.3s ease;
        }}
        #brewChatToggle:hover {{
            transform: scale(1.08);
            box-shadow: 0 6px 24px rgba(203,162,88,0.55);
        }}
        #brewChatToggle svg {{ width: 26px; height: 26px; fill: #111; }}

        #brewChatWindow {{
            position: fixed;
            bottom: 94px;
            right: 24px;
            width: 370px;
            height: 500px;
            background: #181818;
            border-radius: 16px;
            border: 1px solid #2a2a2a;
            box-shadow: 0 16px 48px rgba(0,0,0,0.5);
            z-index: 999998;
            display: none;
            flex-direction: column;
            overflow: hidden;
            font-family: 'Inter', sans-serif;
        }}
        #brewChatWindow.open {{ display: flex; }}

        .brew-chat-header {{
            background: #1e1e1e;
            padding: 14px 18px;
            border-bottom: 1px solid #2a2a2a;
            display: flex;
            align-items: center;
            gap: 10px;
            flex-shrink: 0;
        }}
        .brew-chat-header .dot {{
            width: 9px; height: 9px;
            background: #4ade80;
            border-radius: 50%;
            animation: brewPulse 2s infinite;
        }}
        @keyframes brewPulse {{
            0%,100% {{ opacity:1; }}
            50% {{ opacity:0.4; }}
        }}
        .brew-chat-header .info h4 {{
            margin: 0; font-size: 0.92rem; color: #fff; font-weight: 600;
        }}
        .brew-chat-header .info p {{
            margin: 0; font-size: 0.72rem; color: #888;
        }}

        .brew-chat-msgs {{
            flex: 1;
            overflow-y: auto;
            padding: 14px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .brew-chat-msgs::-webkit-scrollbar {{ width: 4px; }}
        .brew-chat-msgs::-webkit-scrollbar-thumb {{ background: #333; border-radius: 2px; }}

        .brew-msg {{
            max-width: 82%;
            padding: 10px 14px;
            border-radius: 12px;
            font-size: 0.86rem;
            line-height: 1.45;
            word-wrap: break-word;
        }}
        .brew-msg.bot {{
            background: #222;
            color: #ddd;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
        }}
        .brew-msg.user {{
            background: #CBA258;
            color: #111;
            align-self: flex-end;
            border-bottom-right-radius: 4px;
            font-weight: 500;
        }}

        .brew-typing {{
            align-self: flex-start;
            padding: 10px 16px;
            background: #222;
            border-radius: 12px;
            border-bottom-left-radius: 4px;
            display: none;
        }}
        .brew-typing span {{
            display: inline-block;
            width: 6px; height: 6px;
            background: #666;
            border-radius: 50%;
            margin: 0 2px;
            animation: brewTyping 1.4s infinite ease-in-out;
        }}
        .brew-typing span:nth-child(2) {{ animation-delay: 0.2s; }}
        .brew-typing span:nth-child(3) {{ animation-delay: 0.4s; }}
        @keyframes brewTyping {{
            0%,80%,100% {{ transform: scale(0.6); opacity: 0.4; }}
            40% {{ transform: scale(1); opacity: 1; }}
        }}

        .brew-chat-input {{
            padding: 10px 14px;
            border-top: 1px solid #2a2a2a;
            display: flex;
            gap: 8px;
            background: #1a1a1a;
            flex-shrink: 0;
        }}
        .brew-chat-input input {{
            flex: 1;
            background: #222;
            border: 1px solid #333;
            border-radius: 10px;
            padding: 10px 12px;
            color: #ddd;
            font-size: 0.86rem;
            outline: none;
            font-family: 'Inter', sans-serif;
        }}
        .brew-chat-input input:focus {{ border-color: #CBA258; }}
        .brew-chat-input input::placeholder {{ color: #555; }}

        .brew-chat-send {{
            background: #CBA258;
            border: none;
            border-radius: 10px;
            padding: 0 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            transition: background 0.2s;
        }}
        .brew-chat-send:hover {{ background: #d4b56c; }}
        .brew-chat-send svg {{ width: 18px; height: 18px; fill: #111; }}
    `;
    parentDoc.head.appendChild(style);

    // --- Toggle Button ---
    const toggleBtn = parentDoc.createElement('button');
    toggleBtn.id = 'brewChatToggle';
    toggleBtn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12z"/><path d="M7 9h2v2H7zm4 0h2v2h-2zm4 0h2v2h-2z"/></svg>';
    parentDoc.body.appendChild(toggleBtn);

    // --- Chat Window ---
    const chatWin = parentDoc.createElement('div');
    chatWin.id = 'brewChatWindow';
    chatWin.innerHTML = `
        <div class="brew-chat-header">
            <div class="dot"></div>
            <div class="info">
                <h4>Brew Assistant</h4>
                <p>Typically replies instantly</p>
            </div>
        </div>
        <div class="brew-chat-msgs" id="brewMsgs">
            <div class="brew-msg bot">Hi there! ☕ I'm your Brew Haven assistant. Ask me anything about our menu, hours, or recommendations!</div>
            <div class="brew-typing" id="brewTyping"><span></span><span></span><span></span></div>
        </div>
        <div class="brew-chat-input">
            <input type="text" id="brewInput" placeholder="Type a message..." />
            <button class="brew-chat-send" id="brewSendBtn">
                <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
            </button>
        </div>
    `;
    parentDoc.body.appendChild(chatWin);

    // --- Toggle Logic ---
    let isOpen = false;
    toggleBtn.addEventListener('click', function() {{
        isOpen = !isOpen;
        chatWin.classList.toggle('open', isOpen);
        if (isOpen) {{
            toggleBtn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>';
            parentDoc.getElementById('brewInput').focus();
        }} else {{
            toggleBtn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12z"/><path d="M7 9h2v2H7zm4 0h2v2h-2zm4 0h2v2h-2z"/></svg>';
        }}
    }});

    // --- Add Message ---
    function addMsg(text, sender) {{
        const container = parentDoc.getElementById('brewMsgs');
        const typing = parentDoc.getElementById('brewTyping');
        const msg = parentDoc.createElement('div');
        msg.className = 'brew-msg ' + sender;
        msg.textContent = text;
        container.insertBefore(msg, typing);
        container.scrollTop = container.scrollHeight;
    }}

    // --- Send Message (via local proxy) ---
    async function sendMsg() {{
        const input = parentDoc.getElementById('brewInput');
        const text = input.value.trim();
        if (!text) return;

        addMsg(text, 'user');
        input.value = '';

        const typing = parentDoc.getElementById('brewTyping');
        typing.style.display = 'flex';
        const container = parentDoc.getElementById('brewMsgs');
        container.scrollTop = container.scrollHeight;

        try {{
            const res = await fetch(PROXY_URL, {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ chatInput: text, sessionId: 'brew-haven-widget' }})
            }});
            const raw = await res.text();
            typing.style.display = 'none';

            // Parse NDJSON response
            const lines = raw.trim().split('\\n');
            let reply = '';
            for (const line of lines) {{
                try {{
                    const chunk = JSON.parse(line);
                    if (chunk.type === 'item' && chunk.content) {{
                        reply += chunk.content;
                    }}
                }} catch(e) {{}}
            }}
            if (!reply) {{
                try {{
                    const data = JSON.parse(raw);
                    reply = data.output || data.response || data.text || data.message || JSON.stringify(data);
                }} catch(e) {{ reply = raw; }}
            }}
            addMsg(reply, 'bot');
        }} catch(err) {{
            typing.style.display = 'none';
            addMsg('Sorry, could not connect. Please try again.', 'bot');
        }}
    }}

    // --- Event Listeners ---
    parentDoc.getElementById('brewSendBtn').addEventListener('click', sendMsg);
    parentDoc.getElementById('brewInput').addEventListener('keydown', function(e) {{
        if (e.key === 'Enter') sendMsg();
    }});
}})();
</script>
"""

components.html(chatbot_html, height=0, width=0)