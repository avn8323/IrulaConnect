import streamlit as st

def apply_styles():
 st.markdown('''<style>
 @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700;800&display=swap');
 .stApp{background:linear-gradient(180deg,#f7fbf4 0%,#fffaf1 42%,#f7f5ee 100%);color:#25352a;font-family:'DM Sans',sans-serif}
 [data-testid="stSidebar"]{background:linear-gradient(180deg,#e7f0df,#f5eee1);border-right:1px solid #dce7d5}
 .hero{min-height:390px;padding:clamp(2rem,6vw,5rem);border-radius:30px;position:relative;overflow:hidden;background:linear-gradient(90deg,rgba(17,48,34,.86),rgba(24,62,42,.57)),url('https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=1800&q=85') center/cover;color:#fff;display:flex;flex-direction:column;justify-content:center;box-shadow:0 18px 50px rgba(31,65,42,.16)}
 .hero h1{font-family:'Playfair Display',serif;color:#fff;font-size:clamp(2.5rem,6vw,5rem);line-height:1.05;max-width:850px;margin:.5rem 0 1rem}.hero p{font-size:1.15rem;max-width:680px;color:#f1f6eb}.eyebrow{letter-spacing:.18em;font-size:.75rem;font-weight:700;color:#d5e8bd}
 .section-card{background:rgba(255,255,255,.76);border:1px solid #e4eadf;border-radius:24px;padding:1.4rem;margin:.7rem 0;box-shadow:0 8px 28px rgba(36,62,39,.06)}
 .stButton>button{border-radius:14px;border:1px solid #cbdcc5;min-height:2.55rem;background:#fff;color:#294b35;font-weight:600}.stButton>button[kind="primary"]{background:#3f714e;color:white;border-color:#3f714e}
 [data-testid="stMetric"]{background:#fff;border:1px solid #e5ebdf;padding:1rem;border-radius:18px}
 h1,h2,h3{font-family:'Playfair Display',serif;color:#294a35}
 .progress-track{width:100%;height:12px;border-radius:999px;background:#d95b5b;overflow:hidden;margin:.35rem 0 1rem}.progress-done{height:100%;background:#31945b;border-radius:999px;transition:width .25s ease}
 @media(max-width:700px){.hero{min-height:330px;padding:1.5rem;border-radius:22px}.hero h1{font-size:2.55rem}.section-card{padding:1rem}}
 </style>''',unsafe_allow_html=True)
