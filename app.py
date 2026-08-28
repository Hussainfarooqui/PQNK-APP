# pyre-ignore-all-errors
import streamlit as st
import os
import PyPDF2
from groq import Groq
import streamlit.components.v1 as components

# Alias to bypass IDE markdown string checking
render = st.markdown

# --- Page Configuration ---
st.set_page_config(
    page_title="PQNK Farming AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# --- Groq API Setup ---
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
if not api_key:
    client = None
else:
    client = Groq(api_key=api_key)

# --- KNOWLEDGE BASE LOADING ---
@st.cache_resource
def load_knowledge_base():
    """Reads all PDF files from 'data' folder."""
    all_text = ""
    data_folder = "data"
    
    if not os.path.exists(data_folder):
        return "No data folder found."

    files = [f for f in os.listdir(data_folder) if f.endswith('.pdf')]
    if not files:
        return "No PDF files found in data folder."

    for pdf_file in files:
        try:
            file_path = os.path.join(data_folder, pdf_file)
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text: all_text += text + "\n"
        except Exception as e:
            print(f"Error reading {pdf_file}: {e}")
            
    return all_text

full_knowledge_text = load_knowledge_base()

# --- SMART CONTEXT RETRIEVER (Returns Text AND Score) ---
def get_relevant_context_with_score(query, text_data, max_length=3000):
    if not query or len(text_data) < 100: return text_data[:1000], 95
    
    chunk_size = 1000
    chunks = [text_data[i:i+chunk_size] for i in range(0, len(text_data), chunk_size)]
    
    query_words = set(query.lower().split())
    if not query_words: return text_data[:1000], 0
    
    scored_chunks = []
    
    for chunk in chunks:
        # Calculate how many query words appear in this chunk
        matches = sum(1 for word in query_words if word in chunk.lower())
        scored_chunks.append((matches, chunk))
    
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    
    # Calculate a simple "Confidence Score" (0-100%)
    # Based on the best chunk's match count vs total query words
    best_match_count = scored_chunks[0][0] if scored_chunks else 0
    confidence = int((best_match_count / len(query_words)) * 100)
    
    # Cap between 20% and 98% for realism
    confidence = max(20, min(98, confidence + 20)) 
    
    top_chunks = [chunk for score, chunk in scored_chunks[:3]]
    return "\n...\n".join(top_chunks)[:max_length], confidence

# --- Custom CSS ---
render("""
<style>
    /* Global Settings */
    .stApp { background-color: #FFFFFF !important; }
    
    /* Navbar Styling */
    .nav-header { 
        display: flex; justify-content: space-between; align-items: center; 
        padding: 15px 0; border-bottom: 2px solid #f0f0f0; margin-bottom: 30px; 
    }
    .nav-logo { font-size: 1.8rem; font-weight: 800; color: #2E8B57; display: flex; align-items: center; gap: 10px; }
    .nav-links { color: #555; font-size: 1rem; font-weight: 500; }
    
    /* Hero Section */
    .hero-section { text-align: center; padding: 40px 20px; background-color: white; }
    .hero-title { color: #2E8B57; font-size: 3.2rem; font-weight: 800; margin-bottom: 10px; }
    .hero-subtitle { color: #666; font-size: 1.2rem; max-width: 700px; margin: 0 auto; }
    .mission-badge { background-color: #e6f4ea; color: #2E8B57; padding: 6px 16px; border-radius: 20px; font-weight: bold; font-size: 0.9rem; display: inline-block; margin-bottom: 15px; }

    /* Cards */
    .hover-card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center; border-top: 4px solid #2E8B57; height: 100%; transition: transform 0.3s ease; }
    .hover-card:hover { transform: translateY(-8px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
    
    /* Team & Testimonials */
    .testimonial-img { width: 70px; height: 70px; border-radius: 50%; object-fit: cover; margin-bottom: 15px; border: 2px solid #2E8B57; }
    .team-avatar { width: 90px; height: 90px; border-radius: 50%; background-color: #eee; margin: 0 auto 15px auto; object-fit: cover; }
    .cta-container { background-color: #2E8B57; border-radius: 20px; padding: 50px; text-align: center; color: white; margin-top: 60px; margin-bottom: 40px; }

    /* --- CHAT SPECIFIC STYLES --- */
    .block-container {
        padding-bottom: 140px !important;
        padding-top: 20px !important;
    }

    div[data-testid="stChatInput"] {
        box-shadow: 0 -2px 20px rgba(0,0,0,0.08) !important;
        border-radius: 20px !important;
        background-color: white !important;
    }
    .stChatInputContainer {
        padding-bottom: 20px;
    }

    div[data-testid="stChatMessage"] { background-color: transparent !important; padding: 0px !important; border: none !important; box-shadow: none !important; }
    div[data-testid="stChatMessageAvatar"] { display: none !important; }
    div[data-testid="stChatMessageContent"] { background-color: transparent !important; padding: 0px !important; }

    /* PARALLEL BUBBLES */
    .chat-row { display: flex; width: 100%; margin-bottom: 15px; }
    
    /* USER (RIGHT) */
    .row-user { justify-content: flex-end; }
    .bubble-user {
        background-color: #2E8B57;
        color: white;
        padding: 12px 18px;
        border-radius: 15px 15px 0 15px;
        max-width: 70%;
        text-align: left;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        font-size: 16px;
    }

    /* BOT (LEFT) */
    .row-bot { justify-content: flex-start; }
    .bot-container { display: flex; align-items: flex-start; max-width: 80%; }
    .bot-icon { font-size: 28px; margin-right: 10px; margin-top: 0px; }
    .bubble-bot {
        background-color: #F8F9FA;
        border: 1px solid #E9ECEF;
        border-radius: 0 15px 15px 15px;
        padding: 18px;
        color: #333;
        width: 100%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        font-size: 16px;
    }
    
    /* Progress Bar Style */
    .meta-bar {
        display: flex; 
        align-items: center; 
        gap: 10px; 
        margin-top: 15px; 
        padding-top: 10px;
        border-top: 1px solid #E9ECEF;
        font-size: 0.85rem;
    }

    .stButton button { border: 1px solid #2E8B57; color: #2E8B57; background-color: white; border-radius: 20px; width: 100%; }
    .stButton button:hover { background-color: #2E8B57; color: white; border-color: #2E8B57; }
    
</style>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
current_page = st.query_params.get("page", "home")

# ==================================================
# PAGE 1: WEBSITE
# ==================================================
if current_page == "home":
    render("""<style>section[data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)
    
    render("""
    <div class="nav-header"><div class="nav-logo"><span>🌱</span> PQNK Farming AI</div><div class="nav-links"><a href="/?page=about" target="_self" style="text-decoration:none; color:#555; font-weight:bold;">About Us</a> &nbsp;&nbsp; 🟢 Revolutionizing Agriculture</div></div>
    <div class="hero-section"><div class="mission-badge">Revolutionizing Agriculture with AI</div><div class="hero-title">The Future of Farming Intelligence</div><div class="hero-subtitle">PQNK Farming AI combines cutting-edge AI with agricultural expertise.</div></div>
    """, unsafe_allow_html=True)
    
    render("<h2 style='text-align: center; color: #333; margin-top: 20px;'>Our Mission</h2>", unsafe_allow_html=True)
    render("<p style='text-align: center; max-width: 700px; margin: 0 auto; color: #666;'>To democratize access to advanced agricultural knowledge and empower farmers worldwide.</p>", unsafe_allow_html=True)

    render("<br><br>", unsafe_allow_html=True)
    render("<h2 style='text-align: center; color: #333;'>Meet The Team</h2>", unsafe_allow_html=True)
    
    t1, t2, t3 = st.columns(3)
    with t1: render("""<div class="hover-card"><div class="team-avatar" style="display:flex; align-items:center; justify-content:center; font-size:2.5rem; background-color:#e6f4ea; color:#2E8B57;">👨‍⚕️</div><h3 style="color:#333;">Dr. Mansoor Ebrahim</h3></div>""", unsafe_allow_html=True)
    with t2: render("""<div class="hover-card"><div class="team-avatar" style="display:flex; align-items:center; justify-content:center; font-size:2.5rem; background-color:#e6f4ea; color:#2E8B57;">👨‍💻</div><h3 style="color:#333;">Muzammil Yasir</h3></div>""", unsafe_allow_html=True)
    with t3: render("""<div class="hover-card"><div class="team-avatar" style="display:flex; align-items:center; justify-content:center; font-size:2.5rem; background-color:#e6f4ea; color:#2E8B57;">👨‍💼</div><h3 style="color:#333;">Muhammad Hussain</h3></div>""", unsafe_allow_html=True)

    render("<br><br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: render("""<div class="hover-card"><div style="font-size:2rem; margin-bottom:10px">🧠</div><h3>AI & ML</h3><p style="color:#666;">Advanced RAG systems.</p></div>""", unsafe_allow_html=True)
    with c2: render("""<div class="hover-card"><div style="font-size:2rem; margin-bottom:10px">💾</div><h3>Data Infrastructure</h3><p style="color:#666;">Scalable databases.</p></div>""", unsafe_allow_html=True)
    with c3: render("""<div class="hover-card"><div style="font-size:2rem; margin-bottom:10px">🌐</div><h3>Web Technologies</h3><p style="color:#666;">Responsive design.</p></div>""", unsafe_allow_html=True)

    render("<br><br>", unsafe_allow_html=True)
    render("""<h2 style='text-align: center; color: #333;'>What Farmers Say</h2>""", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    with t1: render("""<div class="hover-card"><img src="https://randomuser.me/api/portraits/men/32.jpg" class="testimonial-img"><p><i>"PQNK saved my harvest."</i></p><h4>John D.</h4></div>""", unsafe_allow_html=True)
    with t2: render("""<div class="hover-card"><img src="https://randomuser.me/api/portraits/women/44.jpg" class="testimonial-img"><p><i>"Reduced fertilizer costs by 20%."</i></p><h4>Maria R.</h4></div>""", unsafe_allow_html=True)
    with t3: render("""<div class="hover-card"><img src="https://randomuser.me/api/portraits/men/85.jpg" class="testimonial-img"><p><i>"Precision farming at its best."</i></p><h4>Ahmed K.</h4></div>""", unsafe_allow_html=True)

    render("""<div class="cta-container"><h2 style="color: white !important;">Ready to Transform Your Farming?</h2><p style="color: #e6f4ea;">Join thousands of farmers today.</p></div>""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2: st.link_button("Start Chatting Now 🚀", url="/?page=chat", type="primary", use_container_width=True)

# ==================================================
# PAGE 2: ABOUT US
# ==================================================
elif current_page == "about":
    render("""<style>section[data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)
    
    render("""
    <div class="nav-header">
        <div class="nav-logo"><span>🌱</span> PQNK Farming AI</div>
        <div class="nav-links"><a href="/?page=home" target="_self" style="text-decoration:none; color:#555; font-weight:bold;">Home</a> &nbsp;&nbsp;|&nbsp;&nbsp; <a href="/?page=chat" target="_self" style="text-decoration:none; color:#555; font-weight:bold;">Chatbot</a></div>
    </div>
    """, unsafe_allow_html=True)
    
    render("<h2 style='text-align: center; color: #333; margin-top: 20px;'>Our Mission</h2>", unsafe_allow_html=True)
    render("<p style='text-align: center; max-width: 700px; margin: 0 auto; color: #666;'>To democratize access to advanced agricultural knowledge and empower farmers worldwide.</p>", unsafe_allow_html=True)

    render("<br><br>", unsafe_allow_html=True)
    render("<h2 style='text-align: center; color: #333;'>Meet The Team</h2>", unsafe_allow_html=True)
    
    t1, t2, t3 = st.columns(3)
    with t1: render("""<div class="hover-card"><div class="team-avatar" style="display:flex; align-items:center; justify-content:center; font-size:2.5rem; background-color:#e6f4ea; color:#2E8B57;">👨‍⚕️</div><h3 style="color:#333;">Dr. Mansoor Ebrahim</h3></div>""", unsafe_allow_html=True)
    with t2: render("""<div class="hover-card"><div class="team-avatar" style="display:flex; align-items:center; justify-content:center; font-size:2.5rem; background-color:#e6f4ea; color:#2E8B57;">👨‍💻</div><h3 style="color:#333;">Muzammil Yasir</h3></div>""", unsafe_allow_html=True)
    with t3: render("""<div class="hover-card"><div class="team-avatar" style="display:flex; align-items:center; justify-content:center; font-size:2.5rem; background-color:#e6f4ea; color:#2E8B57;">👨‍💼</div><h3 style="color:#333;">Muhammad Hussain</h3></div>""", unsafe_allow_html=True)

    render("""<div class="cta-container" style="margin-top: 80px;"><h2 style="color: white !important;">Ready to Transform Your Farming?</h2><p style="color: #e6f4ea;">Join thousands of farmers today.</p></div>""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2: st.link_button("Start Chatting Now 🚀", url="/?page=chat", type="primary", use_container_width=True)

# ==================================================
# PAGE 3: CHATBOT INTERFACE
# ==================================================
elif current_page == "chat":
    
    with st.sidebar:
        st.image("https://api.dicebear.com/7.x/identicon/svg?seed=PQNK", width=50) 
        render("### PQNK Farming")
        st.caption("Expert guidance for sustainable farming")
        if st.button("Clear Conversation"):
            st.session_state.messages = []
            st.rerun()
        render("---")
        render("**Quick Tips:**")
        render("- Ask about soil microbiome")
        render("- Inquire about crop benefits")
        
    render("""<div style="text-align:center; padding: 20px; background-color:#2E8B57; color:white; border-radius:10px; margin-bottom:20px;"><h2>🌿 PQNK Farming Assistant</h2></div>""", unsafe_allow_html=True)

    if "No PDF" in full_knowledge_text:
        st.warning(f"⚠️ {full_knowledge_text}")

    if "messages" not in st.session_state: st.session_state.messages = []

    # --- WELCOME MESSAGE ---
    if len(st.session_state.messages) == 0:
        render("""
        <div class="chat-row row-bot">
            <div class="bot-container">
                <div class="bot-icon">🤖</div>
                <div class="bubble-bot">
                    <div><b>Welcome to PQNK Farming AI Assistant!</b> I'm here to help you with all your agricultural needs. <br>How can I assist you today?</div>
                    <div class="meta-bar">
                        <span style="color:#2E8B57;">📈</span>
                        <div style="background-color:#E9ECEF; border-radius:10px; height:8px; width:100%;"><div style="background-color:#2E8B57; height:100%; width:95%; border-radius:10px;"></div></div>
                        <span style="font-weight:bold; color:#555;">95%</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        render("💬 **Suggested questions:**")
        c1, c2 = st.columns(2)
        def set_q(q): st.session_state.messages.append({"role": "user", "content": q, "score": 0})
        
        with c1:
            if st.button("What are the best crops for my soil type?"): set_q("What are the best crops for my soil type?"); st.rerun()
            if st.button("What are sustainable farming practices?"): set_q("What are sustainable farming practices?"); st.rerun()
        with c2:
            if st.button("How can I improve my crop yield?"): set_q("How can I improve my crop yield?"); st.rerun()
            if st.button("Tell me about pest management"): set_q("Tell me about pest management"); st.rerun()

    # --- DISPLAY MESSAGES ---
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                render(f"""<div class="chat-row row-user"><div class="bubble-user">{message["content"]}</div></div>""", unsafe_allow_html=True)
            else:
                # Retrieve Score (Default to 90% if missing)
                score = message.get("score", 90)
                render(f"""
                <div class="chat-row row-bot">
                    <div class="bot-container">
                        <div class="bot-icon">🤖</div>
                        <div class="bubble-bot">
                            <div>{message["content"]}</div>
                            <div class="meta-bar">
                                <span style="color:#2E8B57;">📈</span>
                                <div style="background-color:#E9ECEF; border-radius:10px; height:8px; width:100%;">
                                    <div style="background-color:#2E8B57; height:100%; width:{score}%; border-radius:10px;"></div>
                                </div>
                                <span style="font-weight:bold; color:#555;">{score}%</span>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # --- CHAT INPUT ---
    if prompt := st.chat_input("Ask me about PQNK..."):
        st.session_state.messages.append({"role": "user", "content": prompt, "score": 0})
        st.rerun()

    # --- GENERATE RESPONSE ---
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with chat_container:
            placeholder = st.empty()
            # Show Thinking State
            placeholder.markdown("""<div class="chat-row row-bot"><div class="bot-container"><div class="bot-icon">🤖</div><div class="bubble-bot">Thinking...</div></div></div>""", unsafe_allow_html=True)
            
            full_resp = ""
            confidence_score = 85 # Default
            
            if client:
                try:
                    # Get Text AND Score
                    relevant_text, confidence_score = get_relevant_context_with_score(st.session_state.messages[-1]["content"], full_knowledge_text)
                    
                    dynamic_system_prompt = f"You are PQNK Farming AI. Answer strictly based on:\n{relevant_text}"
                    
                    history_to_send = st.session_state.messages[-4:] 
                    api_msgs = [{"role": "system", "content": dynamic_system_prompt}] + \
                               [{"role": m["role"], "content": m["content"]} for m in history_to_send]
                    
                    stream = client.chat.completions.create(
                        model = "openai/gpt-oss-20b", 
                        messages=api_msgs, 
                        stream=True
                    )
                    
                    for chunk in stream:
                        full_resp += (chunk.choices[0].delta.content or "")
                        # Dynamic Update with Bar
                        placeholder.markdown(f"""
                        <div class="chat-row row-bot">
                            <div class="bot-container">
                                <div class="bot-icon">🤖</div>
                                <div class="bubble-bot">
                                    <div>{full_resp}▌</div>
                                    <div class="meta-bar">
                                        <span style="color:#2E8B57;">📈</span>
                                        <div style="background-color:#E9ECEF; border-radius:10px; height:8px; width:100%;"><div style="background-color:#2E8B57; height:100%; width:{confidence_score}%; border-radius:10px;"></div></div>
                                        <span style="font-weight:bold; color:#555;">{confidence_score}%</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Final Render
                    placeholder.markdown(f"""
                    <div class="chat-row row-bot">
                        <div class="bot-container">
                            <div class="bot-icon">🤖</div>
                            <div class="bubble-bot">
                                <div>{full_resp}</div>
                                <div class="meta-bar">
                                    <span style="color:#2E8B57;">📈</span>
                                    <div style="background-color:#E9ECEF; border-radius:10px; height:8px; width:100%;"><div style="background-color:#2E8B57; height:100%; width:{confidence_score}%; border-radius:10px;"></div></div>
                                    <span style="font-weight:bold; color:#555;">{confidence_score}%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": full_resp, "score": confidence_score})
                except Exception as e:
                    st.error(f"Error: {e}")

    components.html("""
    <script>
        var body = window.parent.document.querySelector(".main");
        body.scrollTop = body.scrollHeight;
    </script>
    """, height=0)