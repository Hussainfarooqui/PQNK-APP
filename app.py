import streamlit as st
import os
import PyPDF2
from groq import Groq

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
    """Reads all PDF files and returns text chunks."""
    all_text = ""
    data_folder = "data"
    
    if not os.path.exists(data_folder):
        return "No data folder found."

    files = [f for f in os.listdir(data_folder) if f.endswith('.pdf')]
    if not files:
        return "No PDF files found."

    for pdf_file in files:
        try:
            file_path = os.path.join(data_folder, pdf_file)
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        all_text += text + "\n"
        except Exception as e:
            print(f"Error reading {pdf_file}: {e}")
            
    return all_text

# Load data once
full_knowledge_text = load_knowledge_base()

# --- SMART CONTEXT RETRIEVER (The Fix) ---
def get_relevant_context(query, text_data, max_length=6000):
    """
    Instead of sending ALL text, we find paragraphs that match the user's question.
    This keeps the token count low (preventing Error 413).
    """
    if not query or len(text_data) < 100:
        return text_data[:2000] # Return summary if no query
    
    # Split text into chunks of ~1000 characters
    chunk_size = 1000
    chunks = [text_data[i:i+chunk_size] for i in range(0, len(text_data), chunk_size)]
    
    # Simple search: Score chunks based on keyword overlap
    query_words = set(query.lower().split())
    scored_chunks = []
    
    for chunk in chunks:
        score = sum(1 for word in query_words if word in chunk.lower())
        scored_chunks.append((score, chunk))
    
    # Sort by score (highest match first) and take top 5
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    top_chunks = [chunk for score, chunk in scored_chunks[:5]]
    
    # Combine relevant chunks
    relevant_text = "\n...\n".join(top_chunks)
    
    # Ensure we don't exceed limit
    return relevant_text[:max_length]

# --- Custom CSS (Exact Design) ---
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    
    /* Navbar */
    .nav-header { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #eee; margin-bottom: 40px; }
    .nav-logo { font-size: 1.5rem; font-weight: bold; color: #333; display: flex; align-items: center; gap: 10px; }
    .nav-links { color: #666; font-size: 0.9rem; }

    /* Hero */
    .hero-section { text-align: center; padding: 50px 20px; background-color: white; }
    .hero-title { color: #2E8B57; font-size: 3.5rem; font-weight: 800; margin-bottom: 15px; line-height: 1.2; }
    .hero-subtitle { color: #555; font-size: 1.2rem; max-width: 800px; margin: 0 auto 30px auto; }
    .mission-badge { background-color: #e6f4ea; color: #2E8B57; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 0.9rem; display: inline-block; margin-bottom: 20px; }

    /* Cards */
    .hover-card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); text-align: center; border-top: 4px solid #2E8B57; height: 100%; transition: transform 0.3s ease, box-shadow 0.3s ease; }
    .hover-card:hover { transform: translateY(-10px); box-shadow: 0 15px 30px rgba(0,0,0,0.15); }
    .tech-header { text-align: center; margin-top: 60px; margin-bottom: 40px; }
    .tech-icon { background-color: #2E8B57; color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify_content: center; margin: 0 auto 20px auto; font-size: 1.5rem; }

    /* Testimonials */
    .testimonial-img { width: 80px; height: 80px; border-radius: 50%; object-fit: cover; margin-bottom: 15px; border: 3px solid #2E8B57; }
    .quote-icon { font-size: 2rem; color: #2E8B57; opacity: 0.3; margin-bottom: 10px; }

    /* Team */
    .team-header { text-align: center; margin-top: 80px; margin-bottom: 50px; }
    .team-card { text-align: center; }
    .team-avatar { width: 100px; height: 100px; border-radius: 50%; background-color: #eee; margin: 0 auto 15px auto; object-fit: cover; }
    .team-name { font-weight: bold; color: #333; margin-bottom: 5px; }
    .team-role { color: #2E8B57; font-size: 0.9rem; font-weight: 600; }

    /* CTA */
    .cta-container { background-color: #2E8B57; border-radius: 20px; padding: 60px; text-align: center; color: white; margin-top: 80px; margin-bottom: 40px; }

    /* Chat UI */
    .chat-header { background-color: #2E8B57; color: white; padding: 20px; border-radius: 10px; text-align: center; font-size: 2rem; font-weight: bold; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .welcome-card { background-color: #F8F9FA; border: 1px solid #E9ECEF; border-radius: 15px; padding: 25px; margin-bottom: 20px; }
    .progress-track { background-color: #E9ECEF; border-radius: 10px; height: 10px; width: 100%; margin: 15px 0; }
    .progress-fill { background-color: #2E8B57; height: 100%; width: 95%; border-radius: 10px; }
    .stButton button { border: 1px solid #2E8B57; color: #2E8B57; background-color: white; border-radius: 20px; }
    .stButton button:hover { background-color: #2E8B57; color: white; border-color: #2E8B57; }
</style>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
current_page = st.query_params.get("page", "home")

# ==================================================
# PAGE 1: WEBSITE
# ==================================================
if current_page == "home":
    st.markdown("""<style>section[data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)

    # Navbar & Hero
    st.markdown("""
    <div class="nav-header">
        <div class="nav-logo"><span>🌱</span> PQNK Farming AI</div>
        <div class="nav-links">About our mission and team &nbsp;&nbsp; 🟢 Revolutionizing Agriculture</div>
    </div>
    <div class="hero-section">
        <div class="mission-badge">Revolutionizing Agriculture with AI</div>
        <div class="hero-title">The Future of Farming Intelligence</div>
        <div class="hero-subtitle">PQNK Farming AI combines cutting-edge AI with decades of agricultural expertise.</div>
    </div>
    """, unsafe_allow_html=True)

    # Mission
    st.markdown("<h2 style='text-align: center; color: #333;'>Our Mission</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; max-width: 700px; margin: 0 auto; color: #666;'>To democratize access to advanced agricultural knowledge and empower farmers worldwide.</p>", unsafe_allow_html=True)

    # Tech Stack
    st.markdown("""<div class="tech-header"><h2 style="color: #333;">Powered by Advanced Technology</h2></div>""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown("""<div class="hover-card"><div class="tech-icon">🧠</div><h3>AI & ML</h3><p style="color:#666;">Advanced RAG systems.</p></div>""", unsafe_allow_html=True)
    with c2: st.markdown("""<div class="hover-card"><div class="tech-icon">💾</div><h3>Data Infrastructure</h3><p style="color:#666;">Scalable databases.</p></div>""", unsafe_allow_html=True)
    with c3: st.markdown("""<div class="hover-card"><div class="tech-icon">🌐</div><h3>Web Technologies</h3><p style="color:#666;">Responsive design.</p></div>""", unsafe_allow_html=True)

    # Testimonials
    st.markdown("""<div class="tech-header"><h2 style="color: #333;">What Farmers Say</h2></div>""", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    with t1: st.markdown("""<div class="hover-card"><img src="https://randomuser.me/api/portraits/men/32.jpg" class="testimonial-img"><div class="quote-icon">❝</div><p><i>"PQNK saved my harvest."</i></p><h4>John D.</h4></div>""", unsafe_allow_html=True)
    with t2: st.markdown("""<div class="hover-card"><img src="https://randomuser.me/api/portraits/women/44.jpg" class="testimonial-img"><div class="quote-icon">❝</div><p><i>"Reduced fertilizer costs by 20%."</i></p><h4>Maria R.</h4></div>""", unsafe_allow_html=True)
    with t3: st.markdown("""<div class="hover-card"><img src="https://randomuser.me/api/portraits/men/85.jpg" class="testimonial-img"><div class="quote-icon">❝</div><p><i>"Precision farming at its best."</i></p><h4>Ahmed K.</h4></div>""", unsafe_allow_html=True)

    # Team
    st.markdown("""<div class="team-header"><h2 style="color: #333;">The Minds Behind PQNK</h2></div>""", unsafe_allow_html=True)
    t1, t2, t3, t4 = st.columns(4)
    def show_team(col, name, role, seed):
        with col: st.markdown(f"""<div class="team-card"><img src="https://api.dicebear.com/7.x/avataaars/svg?seed={seed}" class="team-avatar"><div class="team-name">{name}</div><div class="team-role">{role}</div></div>""", unsafe_allow_html=True)
    show_team(t1, "Dr. Sarah Chen", "Chief Scientist", "Sarah")
    show_team(t2, "Marcus Rodriguez", "Data Scientist", "Marcus")
    show_team(t3, "Dr. Priya Patel", "Agri Consultant", "Priya")
    show_team(t4, "Alex Thompson", "Full Stack Dev", "Alex")

    # CTA
    st.markdown("""<div class="cta-container"><h2 style="color: white !important;">Ready to Transform Your Farming?</h2><p style="color: #e6f4ea;">Join thousands of farmers today.</p></div>""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2: st.link_button("Start Chatting Now 🚀", url="/?page=chat", type="primary", use_container_width=True)

# ==================================================
# PAGE 2: CHATBOT INTERFACE (With Smart Context)
# ==================================================
elif current_page == "chat":
    
    with st.sidebar:
        st.image("https://api.dicebear.com/7.x/identicon/svg?seed=PQNK", width=50) 
        st.markdown("### PQNK Farming")
        st.caption("Expert guidance for sustainable farming")
        if st.button("Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        st.markdown("---")
        st.markdown("**Quick Tips:**")
        st.markdown("- Ask about soil microbiome")
        st.markdown("- Inquire about crop benefits")
        st.markdown("- Explore implementation")

    st.markdown("""<div class="chat-header">🌿 PQNK Farming Assistant</div>""", unsafe_allow_html=True)

    tab_chat, tab_about = st.tabs(["Chat Assistant", "About PQNK"])

    with tab_chat:
        if "messages" not in st.session_state: st.session_state.messages = []

        # Welcome Card
        if len(st.session_state.messages) == 0:
            st.markdown("""
            <div class="welcome-card">
                <div style="display:flex; align-items:center; gap:10px;">
                    <span style="font-size:20px;">🤖</span>
                    <div><b>Welcome to PQNK Farming AI Assistant!</b> I'm here to help you with all your agricultural needs. <br>How can I assist you today?</div>
                </div>
                <div style="display:flex; align-items:center; gap:10px; margin-top:10px;">
                    <span style="color:#2E8B57;">📈</span>
                    <div class="progress-track"><div class="progress-fill"></div></div>
                    <span style="font-weight:bold; color:#555;">95%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("💬 **Suggested questions:**")
            
            c1, c2 = st.columns(2)
            def set_q(q): st.session_state.messages.append({"role": "user", "content": q})
            
            with c1:
                if st.button("What are the best crops for my soil type?", use_container_width=True): set_q("What are the best crops for my soil type?"); st.rerun()
                if st.button("What are sustainable farming practices?", use_container_width=True): set_q("What are sustainable farming practices?"); st.rerun()
            with c2:
                if st.button("How can I improve my crop yield?", use_container_width=True): set_q("How can I improve my crop yield?"); st.rerun()
                if st.button("Tell me about pest management", use_container_width=True): set_q("Tell me about pest management"); st.rerun()

        # Chat Loop
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                     st.markdown(f"""<div style="background-color:#2E8B57; color:white; padding:10px 15px; border-radius:15px 15px 0 15px; display:inline-block;">{message["content"]}</div>""", unsafe_allow_html=True)
            else:
                with st.chat_message("assistant"):
                    st.markdown(message["content"])

        if prompt := st.chat_input("Ask me about PQNK..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_resp = ""
                if client:
                    try:
                        # --- THE SMART FIX ---
                        # We only fetch 6000 chars relevant to the SPECIFIC question
                        relevant_text = get_relevant_context(st.session_state.messages[-1]["content"], full_knowledge_text)
                        
                        dynamic_system_prompt = f"""
                        You are PQNK Farming AI. Answer based on this text:
                        {relevant_text}
                        """
                        
                        api_msgs = [{"role": "system", "content": dynamic_system_prompt}] + \
                                   [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                        
                        stream = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=api_msgs,
                            stream=True
                        )
                        for chunk in stream:
                            full_resp += (chunk.choices[0].delta.content or "")
                            placeholder.markdown(full_resp + "▌")
                        placeholder.markdown(full_resp)
                        st.session_state.messages.append({"role": "assistant", "content": full_resp})
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("API Key missing.")

    with tab_about:
        st.header("About PQNK Farming")
        st.write("PQNK stands for Physical, Quality, Natural, and Knowledge.")