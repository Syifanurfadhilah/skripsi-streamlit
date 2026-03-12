import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        /* Create an attractive background with gradients and abstract shapes */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, rgba(240, 244, 248, 1) 0%, rgba(217, 226, 236, 1) 100%) !important;
            background-attachment: fixed !important;
        }

        /* Abstract shapes in background */
        [data-testid="stAppViewContainer"]::before {
            content: "";
            position: fixed;
            top: -10%;
            left: -10%;
            width: 50%;
            height: 50%;
            background: radial-gradient(circle, rgba(59,130,246,0.1) 0%, rgba(255,255,255,0) 70%);
            z-index: 0;
            pointer-events: none;
        }

        [data-testid="stAppViewContainer"]::after {
            content: "";
            position: fixed;
            bottom: -10%;
            right: -10%;
            width: 60%;
            height: 60%;
            background: radial-gradient(circle, rgba(147,197,253,0.15) 0%, rgba(255,255,255,0) 70%);
            z-index: 0;
            pointer-events: none;
        }
        
        /* Ensure dark mode still is legible */
        @media (prefers-color-scheme: dark) {
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, rgba(15, 23, 42, 1) 0%, rgba(30, 41, 59, 1) 100%) !important;
            }
            [data-testid="stAppViewContainer"]::before {
                background: radial-gradient(circle, rgba(56,189,248,0.05) 0%, rgba(0,0,0,0) 70%);
            }
            [data-testid="stAppViewContainer"]::after {
                background: radial-gradient(circle, rgba(96,165,250,0.1) 0%, rgba(0,0,0,0) 70%);
            }
            .block-container {
                background-color: var(--background-color) !important;
            }
            h1 {
                color: var(--primary-color) !important;
            }
        }

        .block-container {
            padding: 3rem 4rem !important; 
            max-width: 100% !important;
            background-color: var(--background-color) !important;
            border-radius: 0px !important;
            box-shadow: none !important;
            margin-top: 0rem !important;
            margin-bottom: 2rem !important;
        }

        h1, h2, h3 {
            font-weight: 700 !important;
            letter-spacing: -0.5px !important;
        }
        
        h1 {
            border-bottom: 2px solid var(--secondary-background-color);
            padding-bottom: 10px;
            margin-bottom: 30px !important;
            color: var(--primary-color) !important;
        }

        div[data-testid="stMetric"] {
            background-color: var(--secondary-background-color) !important;
            border-radius: 12px !important;
            padding: 5px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.05) !important;
            border: 1px solid var(--secondary-background-color) !important;
            transition: all 0.3s ease;
        }
        
        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.15), 0 4px 6px -2px rgba(0, 0, 0, 0.1) !important;
        }

        div.stAlert {
            border-radius: 8px !important;
            border-left-width: 4px !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1) !important;
        }

        button[kind="primary"] {
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.5rem 2rem !important;
            transition: all 0.2s ease !important;
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
            border: none !important;
            color: white !important;
        }
        
        button[kind="primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
        }

        div.stRadio > div {
            background-color: var(--secondary-background-color);
            padding: 15px 20px;
            border-radius: 12px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02);
            gap: 20px;
        }
        
        div.stRadio label {
            cursor: pointer !important;
        }

        [data-testid="stSidebar"] {
            border-right: 1px solid var(--secondary-background-color) !important;
        }
        
        /* Hide sidebar elements since we use top navbar */
        [data-testid="collapsedControl"] { display: none !important; }
        section[data-testid="stSidebar"] { display: none !important; }
        
        hr {
            margin-top: 2em !important;
            margin-bottom: 2em !important;
            border-color: var(--secondary-background-color) !important;
        }
        </style>
    """, unsafe_allow_html=True)

def render_navbar():
    st.markdown("""
        <style>
        /* -- Mobile padding -- */
        @media (max-width: 768px) {
            .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }
        }

        /* -- Vertical centering on the navbar row -- */
        [data-testid="stHorizontalBlock"]:has([data-testid="stPageLink"]) {
            align-items: center !important;
            gap: 0 !important;
        }

        /* -- Page link reset -- */
        [data-testid="stPageLink"] { margin: 0 !important; padding: 0 !important; }
        [data-testid="stPageLink"] p { margin: 0 !important; }
        [data-testid="stPageLink"] svg { display: none !important; }
        [data-testid="stPageLink"] a {
            font-size: 0.88rem !important;
            font-weight: 500 !important;
            color: var(--text-color) !important;
            text-decoration: none !important;
            padding: 0.3rem 0.7rem !important;
            border-radius: 8px !important;
            background: transparent !important;
            white-space: nowrap !important;
            display: inline-block !important;
            transition: background 0.2s, color 0.2s !important;
        }
        [data-testid="stPageLink"] a:hover {
            background: rgba(37,99,235,0.1) !important;
            color: #2563eb !important;
        }
        [data-testid="stPageLink"]:last-of-type a {
            background: #2563eb !important;
            color: #fff !important;
            padding: 0.3rem 0.9rem !important;
        }
        [data-testid="stPageLink"]:last-of-type a:hover {
            background: #1d4ed8 !important;
        }

        /* -- Brand title -- */
        .rn-brand {
            font-size: 1.15rem;
            font-weight: 700;
            color: #2563eb;
            margin: 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* -- Scale down on small screens so everything fits in 1 row -- */
        @media (max-width: 600px) {
            .rn-brand { font-size: 0.85rem !important; }
            [data-testid="stPageLink"] a { font-size: 0.72rem !important; padding: 0.2rem 0.45rem !important; }
            [data-testid="stPageLink"]:last-of-type a { padding: 0.2rem 0.55rem !important; }
        }
        @media (max-width: 400px) {
            .rn-brand { font-size: 0.75rem !important; }
            [data-testid="stPageLink"] a { font-size: 0.65rem !important; padding: 0.15rem 0.35rem !important; }
        }

        /* -- Divider -- */
        .rn-divider {
            border: none;
            border-top: 1px solid rgba(100,116,139,0.2);
            margin: 0.4rem 0 2rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

    col_title, col_home, col_admin = st.columns([5.7, 0.5, 0.8])
    with col_title:
        st.markdown("<p class='rn-brand'>Analisis Perilaku Impulsif</p>", unsafe_allow_html=True)
    with col_home:
        st.page_link("Home.py", label="Home")
    with col_admin:
        st.page_link("pages/2_Admin.py", label="Log in (Admin)")

    st.markdown("<hr class='rn-divider'>", unsafe_allow_html=True)
