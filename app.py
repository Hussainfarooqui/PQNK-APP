import streamlit as st
import os
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

# --- System Prompt ---
system_prompt = """
You are PQNK Farming AI, an intelligent agricultural assistant.
You utilize the PQNK principles:
1. Physical (Soil health)
2. Quality (Crop superiority)
3. Natural (Biological ecosystems)
4. Knowledge (Data-driven insights)
"""

# --- Custom CSS ---
st.markdown("""
<style>
    /* Global Settings */
    .stApp { background-color: #FFFFFF; }
    
    /* ---------------- WEBSITE (LANDING PAGE) STYLES ---------------- */
    
    /* Navbar Simulation */
    .nav-header {
        display: flex;
        justify_content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid #eee;
        margin-bottom: 40px;
    }
    .nav-logo {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .nav-links {
        color: #666;
        font-size: 0.9rem;
    }

    /* Hero Section (White BG, Green Text) */
    .hero-section {
        text-align: center;
        padding: 50px 20px;
        background-color: white;
    }
    .hero-title {
        color: #2E8B57; /* PQNK Green */
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 15px;
        line-height: 1.2;
    }
    .hero-subtitle {
        color: #555;
        font-size: 1.2rem;
        max-width: 800px;
        margin: 0 auto 30px auto;
        line-height: 1.6;
    }
    .mission-badge {
        background-color: #e6f4ea;
        color: #2E8B57;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
        display: inline-block;
        margin-bottom: 20px;
    }

    /* --- HOVER CARDS (Used for Tech & Testimonials) --- */
    .hover-card {
        background: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        text-align: center;
        border-top: 4px solid #2E8B57;
        height: 100%;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .hover-card:hover {
        transform: translateY(-10px); /* Lifts up */
        box-shadow: 0 15px 30px rgba(0,0,0,0.15); /* Deeper shadow */
    }

    .tech-header {
        text-align: center;
        margin-top: 60px;
        margin-bottom: 40px;
    }
    .tech-icon {
        background-color: #2E8B57;
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify_content: center;
        margin: 0 auto 20px auto;
        font-size: 1.5rem;
    }

    /* Testimonial Specifics */
    .testimonial-img {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        object-fit: cover;
        margin-bottom: 15px;
        border: 3px solid #2E8B57;
    }
    .quote-icon {
        font-size: 2rem;
        color: #2E8B57;
        opacity: 0.3;
        margin-bottom: 10px;
    }

    /* Team Section */
    .team-header {
        text-align: center;
        margin-top: 80px;
        margin-bottom: 50px;
    }
    .team-card {
        text-align: center;
    }
    .team-avatar {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background-color: #eee;
        margin: 0 auto 15px auto;
        object-fit: cover;
    }
    .team-name {
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
    }
    .team-role {
        color: #2E8B57;
        font-size: 0.9rem;
        font-weight: 600;
    }

    /* CTA Section (Bottom) */
    .cta-container {
        background-color: #2E8B57;
        border-radius: 20px;
        padding: 60px;
        text-align: center;
        color: white;
        margin-top: 80px;
        margin-bottom: 40px;
    }

    /* ---------------- CHAT UI STYLES (UNCHANGED) ---------------- */
    .chat-header {
        background-color: #2E8B57; 
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .welcome-card {
        background-color: #F8F9FA;
        border: 1px solid #E9ECEF;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
    }
    .progress-track {
        background-color: #E9ECEF;
        border-radius: 10px;
        height: 10px;
        width: 100%;
        margin: 15px 0;
    }
    .progress-fill {
        background-color: #2E8B57;
        height: 100%;
        width: 95%;
        border-radius: 10px;
    }
    .stButton button {
        border: 1px solid #2E8B57;
        color: #2E8B57;
        background-color: white;
        border-radius: 20px;
    }
    .stButton button:hover {
        background-color: #2E8B57;
        color: white;
        border-color: #2E8B57;
    }
    
</style>
""", unsafe_allow_html=True)

# --- QUERY PARAMETER NAVIGATION ---
current_page = st.query_params.get("page", "home")

# ==================================================
# PAGE 1: WEBSITE / LANDING PAGE
# ==================================================
if current_page == "home":
    # Hide Sidebar on Landing Page
    st.markdown("""<style>section[data-testid="stSidebar"] {display: none;}</style>""", unsafe_allow_html=True)

    # 1. Navbar Simulation
    st.markdown("""
    <div class="nav-header">
        <div class="nav-logo">
            <span>🌱</span> PQNK Farming AI
        </div>
        <div class="nav-links">
            About our mission and team &nbsp;&nbsp; 🟢 Revolutionizing Agriculture with AI
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="mission-badge">Revolutionizing Agriculture with AI</div>
        <div class="hero-title">The Future of Farming Intelligence</div>
        <div class="hero-subtitle">
            PQNK Farming AI combines cutting-edge artificial intelligence with decades of 
            agricultural expertise to provide farmers with intelligent, actionable insights 
            for sustainable and profitable farming.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Mission
    st.markdown("<h2 style='text-align: center; color: #333;'>Our Mission</h2>", unsafe_allow_html=True)
    st.markdown("""
    <p style="text-align: center; max-width: 700px; margin: 0 auto; color: #666; line-height: 1.6;">
    To democratize access to advanced agricultural knowledge and empower farmers worldwide with 
    AI-driven insights that promote sustainable farming practices.
    </p>
    """, unsafe_allow_html=True)

    # 4. Technology Stack (Hover Cards)
    st.markdown("""<div class="tech-header"><h2 style="color: #333;">Powered by Advanced Technology</h2></div>""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="hover-card"><div class="tech-icon">🧠</div><h3>AI & ML</h3><p style="color:#666;">Advanced RAG systems.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="hover-card"><div class="tech-icon">💾</div><h3>Data Infrastructure</h3><p style="color:#666;">Scalable databases.</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="hover-card"><div class="tech-icon">🌐</div><h3>Web Technologies</h3><p style="color:#666;">Responsive design.</p></div>""", unsafe_allow_html=True)

    # 5. TESTIMONIALS (New Section with Hover Cards)
    st.markdown("""<div class="tech-header"><h2 style="color: #333;">What Farmers Say</h2></div>""", unsafe_allow_html=True)
    
    test1, test2, test3 = st.columns(3)
    
    with test1:
        st.markdown("""
        <div class="hover-card">
            <img src="https://randomuser.me/api/portraits/men/32.jpg" class="testimonial-img">
            <div class="quote-icon">❝</div>
            <p><i>"PQNK saved my harvest this year. The water usage tips were spot on."</i></p>
            <h4>John D.</h4>
            <small>Wheat Farmer</small>
        </div>
        """, unsafe_allow_html=True)

    with test2:
        st.markdown("""
        <div class="hover-card">
            <img src="https://randomuser.me/api/portraits/women/44.jpg" class="testimonial-img">
            <div class="quote-icon">❝</div>
            <p><i>"The soil analysis helped me reduce fertilizer costs by 20%."</i></p>
            <h4>Maria R.</h4>
            <small>Organic Grower</small>
        </div>
        """, unsafe_allow_html=True)

    with test3:
        st.markdown("""
        <div class="hover-card">
            <img src="https://randomuser.me/api/portraits/men/85.jpg" class="testimonial-img">
            <div class="quote-icon">❝</div>
            <p><i>"Finally, an AI that actually understands precision farming."</i></p>
            <h4>Ahmed K.</h4>
            <small>Agri-Tech Consultant</small>
        </div>
        """, unsafe_allow_html=True)

    # 6. Team Section
    st.markdown("""<div class="team-header"><h2 style="color: #333;">The Minds Behind PQNK</h2></div>""", unsafe_allow_html=True)
    t1, t2, t3, t4 = st.columns(4)
    def show_team(col, name, role, seed):
        with col:
            st.markdown(f"""
            <div class="team-card">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={seed}" class="team-avatar">
                <div class="team-name">{name}</div>
                <div class="team-role">{role}</div>
            </div>
            """, unsafe_allow_html=True)
    show_team(t1, "Dr. Sarah Chen", "Chief Scientist", "Sarah")
    show_team(t2, "Marcus Rodriguez", "Data Scientist", "Marcus")
    show_team(t3, "Dr. Priya Patel", "Agri Consultant", "Priya")
    show_team(t4, "Alex Thompson", "Full Stack Dev", "Alex")

    # 7. CTA
    st.markdown("""
    <div class="cta-container">
        <h2 style="color: white !important;">Ready to Transform Your Farming?</h2>
        <p style="color: #e6f4ea;">Join thousands of farmers who are already using PQNK Farming AI.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_cta1, col_cta2, col_cta3 = st.columns([1, 2, 1])
    with col_cta2:
        st.link_button("Start Chatting Now 🚀", url="/?page=chat", type="primary", use_container_width=True)


# ==================================================
# PAGE 2: CHATBOT INTERFACE (Unchanged)
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
            
            col_q1, col_q2 = st.columns(2)
            def set_q(q): st.session_state.messages.append({"role": "user", "content": q})
            
            with col_q1:
                if st.button("What are the best crops for my soil type?", use_container_width=True):
                    set_q("What are the best crops for my soil type?")
                    st.rerun()
                if st.button("What are sustainable farming practices?", use_container_width=True):
                    set_q("What are sustainable farming practices?")
                    st.rerun()
            with col_q2:
                if st.button("How can I improve my crop yield?", use_container_width=True):
                    set_q("How can I improve my crop yield?")
                    st.rerun()
                if st.button("Tell me about pest management", use_container_width=True):
                    set_q("Tell me about pest management")
                    st.rerun()

        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                     st.markdown(f"""
                     <div style="background-color:#2E8B57; color:white; padding:10px 15px; border-radius:15px 15px 0 15px; display:inline-block;">
                        {message["content"]}
                     </div>
                     """, unsafe_allow_html=True)
            else:
                with st.chat_message("assistant"):
                    st.markdown(message["content"])

        if prompt := st.chat_input("Hello, tell me about PQNK..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_resp = ""
                if client:
                    try:
                        api_msgs = [{"role": "system", "content": system_prompt}] + \
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