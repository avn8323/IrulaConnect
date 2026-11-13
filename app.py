import time, re
from datetime import datetime
import streamlit as st
from src.corpus import load_corpus, inventory, all_records
from src.language import get_language_key
from src.chat import answer_without_provider
from src.config import GEMINI_MODEL, get_google_api_key
from src.progress import load_progress, update_progress, record_visit, add_session_seconds
from src.audio import generate_audio, audio_data_uri
from src.ui import apply_styles

st.set_page_config(page_title="IrulaConnect | Irula language & culture", page_icon="I", layout="wide")
apply_styles()
try:
    corpus = load_corpus()
except Exception as exc:
    st.error(f"Could not load data/corpus.json: {exc}")
    st.stop()

progress = load_progress()
if "session_start" not in st.session_state:
    st.session_state.session_start = time.time()
if "visit_initialized" not in st.session_state:
    progress = record_visit()
    st.session_state.visit_initialized = True
if "last_session_tick" not in st.session_state:
    st.session_state.last_session_tick = time.time()
else:
    now_tick = time.time()
    add_session_seconds(min(300, now_tick - st.session_state.last_session_tick))
    st.session_state.last_session_tick = now_tick
if "messages" not in st.session_state:
    st.session_state.messages = []
if "learn_index_by_section" not in st.session_state:
    st.session_state.learn_index_by_section = {}
if "story_index" not in st.session_state:
    st.session_state.story_index = 0

LANGS = [("irula", "Irula"), ("english", "English"), ("tamil", "Tamil"), ("telugu", "Telugu"), ("hindi", "Hindi")]
with st.sidebar:
    st.title("IrulaConnect")
    language_label = st.selectbox("Response language", ["English", "Tamil", "Telugu", "Hindi"], key="response_language")
    language = get_language_key(language_label)
    page = st.radio("Navigate", ["Home", "Laila", "Learn", "Stories & Culture", "Progress"])

def value(record, key, lang=None):
    lang = lang or key
    v = record.get(key, "")
    if isinstance(v, dict):
        return v.get(lang) or v.get("english") or ""
    return v if isinstance(v, str) else ""

def record_title(section, r):
    for k in ("irula", "word", "title", "rule_name", "scenario", "english"):
        v = r.get(k)
        if isinstance(v, str) and v.strip():
            return v
    if section == "riddles":
        return value(r.get("riddle", {}), "english") or "Riddle"
    return section.replace("_", " ").title()

def item_label(section, r):
    title = record_title(section, r)
    # Prefer a human-readable title, never a machine id.
    if title == str(r.get("id", "")) or re.fullmatch(r"[a-zA-Z]\d+", title):
        if section == "riddles":
            return value(r.get("riddle", {}), "english") or "Riddle"
        return r.get("english") or r.get("rule_name") or r.get("scenario") or section.title()
    return title

def audio_control(text, lang, key):
    if not text or lang == "irula":
        return
    if st.button("Listen", key="audio-" + str(key)):
        try:
            path = generate_audio(text, lang)
            uri = audio_data_uri(path)
            import streamlit.components.v1 as components
            nonce = time.time_ns()
            player = "<audio id='laila-audio-" + str(nonce) + "' autoplay preload='auto' src='" + uri + "'></audio>"
            player += "<script>const a=document.getElementById('laila-audio-" + str(nonce) + "'); if(a){a.currentTime=0; a.play().catch(()=>{});}</script>"
            components.html(player, height=1, scrolling=False)
        except Exception:
            st.warning("Audio is temporarily unavailable. Please try again.")

def show_language_lines(record, section, prefix):
    for lang, label in LANGS:
        if section == "riddles":
            txt = value(record.get("riddle", {}), lang, lang)
        else:
            txt = value(record, lang, lang)
        if txt:
            a, b = st.columns([12, 1])
            with a: st.markdown(f"**{label}:** {txt}")
            with b: audio_control(txt, lang, f"{prefix}-{lang}")

def id_for(section, r, i):
    return str(r.get("id") or f"{section}-{i}")

def render_story(section, r, i):
    rid = id_for(section, r, i)
    title = item_label(section, r)
    with st.container(border=True):
        st.subheader(title)
        if section == "riddles":
            show_language_lines(r, section, rid)
            with st.expander("Reveal answer"):
                for lang, label in LANGS:
                    ans = value(r.get("answer", {}), lang, lang)
                    if ans:
                        a,b=st.columns([12,1])
                        with a: st.markdown(f"**{label}:** {ans}")
                        with b: audio_control(ans, lang, f"{rid}-answer-{lang}")
        elif section == "dialogues":
            for j,line in enumerate(r.get("lines", [])):
                st.markdown(f"**{line.get('speaker','Speaker')}**")
                show_language_lines(line, section, f"{rid}-{j}")
        else:
            show_language_lines(r, section, rid)
            if r.get("context_note"):
                with st.expander("Cultural context"): st.write(r["context_note"])
        p = load_progress()
        c1,c2,c3 = st.columns(3)
        if c1.button("Mark completed", key=f"complete-story-{rid}"):
            update_progress(rid, "known", section=section)
            st.rerun()
        if c2.button("Save for later" if rid not in p["saved"] else "Remove saved", key=f"save-story-{rid}"):
            update_progress(rid, "saved" if rid not in p["saved"] else "unsave", section=section)
            st.rerun()
        if rid in p["known"]: c3.success("Completed")
        elif rid in p["saved"]: c3.info("Saved")

if page == "Home":
    st.markdown("""<section class="hero"><div class="eyebrow">LANGUAGE · PEOPLE · LIVING HERITAGE</div><h1>Meet Irula.</h1><p>A living language of southern India — discover its words, stories, knowledge and the people who carry it forward.</p></section>""", unsafe_allow_html=True)
    st.header("Irula: a living Dravidian language")
    st.write("Irula (ISO 639-3: iru) is spoken by Irula communities in parts of Tamil Nadu and neighbouring regions of southern India. It belongs to the Dravidian language family. Irula is used in everyday communication and carries expressions, knowledge, stories and relationships across generations.")
    st.image("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1800&q=85", use_container_width=True)
    st.header("Roots and evolution")
    st.write("Irula developed as a spoken community language over many generations. Its varieties reflect local histories and contact with neighbouring languages, including Tamil, Kannada and Malayalam. Linguists study its sounds, vocabulary and grammar through field research, word lists, recordings and comparisons with other Dravidian languages. There is no single documented starting date for a language that grew through everyday use.")
    st.header("A language shaped by place")
    st.write("Irula communities have deep connections with the landscapes in which they live. The language is part of family life, oral expression, local place knowledge, practical skills, humour and cultural memory. Community experiences are diverse, and no single description represents every Irula person.")
    st.header("Why Irula matters")
    a,b,c=st.columns(3)
    with a:
        st.subheader("Identity & belonging")
        st.write("Language carries relationships, memories and a sense of belonging.")
    with b:
        st.subheader("Knowledge & nature")
        st.write("Words preserve ways of describing local environments and everyday experience.")
    with c:
        st.subheader("Learning & future")
        st.write("Dictionaries, recordings and learning tools can support access for new generations.")
    st.image("https://images.unsplash.com/photo-1472396961693-142e6e269027?auto=format&fit=crop&w=1800&q=85", use_container_width=True)
    st.header("Challenges and opportunities")
    st.write("Like many smaller community languages, Irula faces challenges including uneven documentation, limited digital resources, language shift and a shortage of verified speech technology. Learning materials, dictionaries, community recordings and intergenerational teaching can help make the language easier to access and learn.")
    st.header("Explore and learn more")
    st.markdown("""
    - [Wikipedia — Irula language](https://en.wikipedia.org/wiki/Irula_language)
    - [Glottolog — language classification and bibliography](https://glottolog.org/)
    - [Google Scholar — Irula language research](https://scholar.google.com/scholar?q=Irula+language)
    - [Internet Archive — Irula language publications](https://archive.org/search?query=Irula+language)
    - [Ethnologue — language profiles](https://www.ethnologue.com/)
    """)

elif page == "Laila":
    st.title("Laila")
    if get_google_api_key():
        st.caption(f"Your friendly companion")
    else:
        st.caption("Offline mode · Add your Google AI Studio key to enable online chat and RAG")
    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else "👸"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("audio_text"):
                audio_control(msg["audio_text"], language, "laila-" + str(msg.get("id", "saved")))
    prompt = st.chat_input("Say hi, ask a question, or look up an Irula word…")
    if prompt:
        st.session_state.messages.append({"role":"user","content":prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        response = answer_without_provider(corpus, prompt, language, history=st.session_state.messages[:-1])
        audio_text = response
        # Speak only the selected response-language line for compact dictionary answers.
        wanted_label = {"english":"English", "tamil":"Tamil", "telugu":"Telugu", "hindi":"Hindi"}.get(language, "English")
        for line in response.splitlines():
            if line.startswith(f"**{wanted_label}:**"):
                audio_text = line.split(":", 1)[1].replace("**", "").strip()
                break
        else:
            if "\n\n" in response:
                audio_text = response.split("\n\n", 1)[1]
        st.session_state.messages.append({"role":"assistant","content":response,"audio_text":audio_text,"id":len(st.session_state.messages)})
        with st.chat_message("assistant", avatar="👸"):
            st.markdown(response)
            if audio_text:
                audio_control(audio_text, language, "laila-" + str(len(st.session_state.messages)))


elif page == "Learn":
    st.title("Learn Irula")
    sections=[s for s in corpus if isinstance(corpus[s],list) and s not in ("quizzes",)]
    section=st.selectbox("Choose learning material", sections, format_func=lambda s:s.replace("_"," ").title())
    items=corpus.get(section, [])
    if items:
        idx=st.session_state.learn_index_by_section.get(section, 0)
        idx=max(0,min(idx,len(items)-1))
        r=items[idx]; rid=id_for(section,r,idx)
        st.caption(f"Item {idx+1} of {len(items)}")
        st.subheader(item_label(section,r))
        if section=="riddles":
            show_language_lines(r, section, rid)
            with st.expander("Reveal answer"):
                for lang,label in LANGS:
                    ans=value(r.get("answer",{}),lang,lang)
                    if ans:
                        a,b=st.columns([12,1])
                        with a: st.markdown(f"**{label}:** {ans}")
                        with b: audio_control(ans,lang,f"{rid}-ans-{lang}")
        elif section=="grammar_rules":
            st.markdown("**Rule**")
            st.write(r.get("explanation",""))
            for j,ex in enumerate(r.get("examples",[])):
                with st.container(border=True):
                    show_language_lines(ex, section, f"{rid}-ex{j}")
        elif section=="dialogues":
            for j,line in enumerate(r.get("lines",[])):
                st.markdown(f"**{line.get('speaker','Speaker')}**")
                show_language_lines(line,section,f"{rid}-{j}")
        else:
            show_language_lines(r,section,rid)
            if r.get("category"): st.caption("Category: "+str(r["category"]))
            if r.get("context_note"):
                with st.expander("Context"): st.write(r["context_note"])
        p=load_progress()
        prev,nxt,done,save=st.columns(4)
        with prev:
            if st.button("Previous",disabled=idx==0,key="prev-"+section):
                st.session_state.learn_index_by_section[section]=idx-1; st.rerun()
        with nxt:
            if st.button("Next",disabled=idx>=len(items)-1,key="next-"+section):
                st.session_state.learn_index_by_section[section]=idx+1; st.rerun()
        with done:
            if rid in p["known"]:
                st.success("✓ Completed")
            elif st.button("Mark completed",key="done-"+rid):
                update_progress(rid,"known",section=section); st.rerun()
        with save:
            if st.button("Saved" if rid in p["saved"] else "Save",key="save-"+rid):
                update_progress(rid,"unsave" if rid in p["saved"] else "saved",section=section); st.rerun()
    else:
        st.info("No entries in this section yet.")

elif page == "Stories & Culture":
    st.title("Stories & Culture")
    section=st.selectbox("Choose a collection",["stories_or_proverbs","riddles","dialogues"],format_func=lambda s:s.replace("_"," ").title())
    items=corpus.get(section,[])
    if items:
        idx=max(0,min(st.session_state.story_index,len(items)-1))
        render_story(section,items[idx],idx)
        a,b=st.columns(2)
        with a:
            if st.button("Previous story/item",disabled=idx==0):
                st.session_state.story_index=idx-1; st.rerun()
        with b:
            if st.button("Next story/item",disabled=idx>=len(items)-1):
                st.session_state.story_index=idx+1; st.rerun()
        st.caption(f"{idx+1} of {len(items)}")
    else: st.info("No items in this collection.")

elif page == "Progress":
    st.title("Your learning garden")
    p=load_progress()
    elapsed=max(0,int(time.time()-st.session_state.session_start))
    total=len(p.get("known",[])); saved=len(p.get("saved",[]))
    total_items=sum(len(v) for k,v in corpus.items() if isinstance(v,list) and k!="quizzes")
    a,b,c,d=st.columns(4)
    a.metric("Completed",f"{total}/{total_items}")
    b.metric("Still to learn",max(0,total_items-total))
    c.metric("Saved for later",saved)
    d.metric("This visit",f"{elapsed//60} min")
    st.subheader("Your learning journey")
    def readable_time(raw):
        if not raw:
            return "Not recorded yet"
        try:
            dt = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
            return dt.astimezone().strftime("%d %b %Y, %I:%M %p")
        except (TypeError, ValueError):
            return "Not recorded yet"
    st.write("**Last visit:**", readable_time(p.get("last_visit")))
    st.write("**Last learning activity:**", readable_time(p.get("last_practice")))
    st.write("**Time spent this visit:**",f"{elapsed//3600} h {(elapsed%3600)//60} min")
    st.write("**Time spent previously:**",f"{int(p.get('total_seconds',0))//3600} h {(int(p.get('total_seconds',0))%3600)//60} min")
    lookup={}; sections={}
    for section,records in corpus.items():
        if isinstance(records,list) and section!="quizzes":
            sections[section]=[]
            for i,r in enumerate(records):
                rid=id_for(section,r,i); lookup[rid]=item_label(section,r); sections[section].append(rid)
    st.subheader("Section-wise progress")
    for section,ids in sections.items():
        done=sum(x in p["known"] for x in ids); pct=done/len(ids)*100 if ids else 0
        st.write(f"**{section.replace('_',' ').title()}** · {done} of {len(ids)} completed · {pct:.0f}%")
        st.markdown(
            f'<div class="progress-track" role="img" aria-label="{done} of {len(ids)} completed">'
            f'<div class="progress-done" style="width:{pct:.2f}%"></div></div>',
            unsafe_allow_html=True
        )
    def grouped_list(ids):
        groups={}
        for rid in ids:
            section=next((s for s,vals in sections.items() if rid in vals),"Other")
            groups.setdefault(section,[]).append(lookup.get(rid,"Learning item"))
        for section,names in groups.items():
            with st.expander(f"{section.replace('_',' ').title()} ({len(names)})"):
                for name in names: st.write("• "+name)
    st.subheader("Saved for later")
    grouped_list(p["saved"]) if p["saved"] else st.caption("Your saved words and stories will grow here.")
    st.subheader("Completed items")
    grouped_list(p["known"]) if p["known"] else st.caption("Your completed learning items will appear here.")
    st.caption("Your progress stays on this device for now. Cloud sync is something we hope to bring in a future update. 🌱")
