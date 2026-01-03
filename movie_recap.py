import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Movie Recap Genius", page_icon="📝", layout="wide")

# UI Styling
st.markdown("""
    <style>
    .stTextArea textarea { font-size: 1.1rem !important; line-height: 1.7 !important; color: #1a1a1a; }
    .main { background-color: #fafafa; }
    .stButton>button { background-color: #e63946; color: white; font-weight: bold; width: 100%; border-radius: 10px; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🚀 Settings")
    api_key_input = st.text_input("Gemini API Key:", type="password")
    st.divider()
    
    depth = st.select_slider(
        "ဇာတ်လမ်းအသေးစိတ်မှု (Length)", 
        options=["အကျဉ်းချုပ်", "ပုံမှန်ဇာတ်ကြောင်း", "အသေးစိတ်ဇာတ်ကြောင်း", "ဇာတ်လမ်းတစ်ဆုံး ရှည်ရှည်ဝေးဝေး"]
    )
    
    style = st.selectbox(
        "တင်ဆက်မှုပုံစံ (Style)", 
        [
            "ရင်တထိတ်ထိတ် (Thriller)", 
            "ဟာသနှောသော (Funny)", 
            "အလွမ်းအဆွေး (Drama)", 
            "ကျောချမ်းစရာ (Horror)",
            "စုံထောက်စတိုင် (Mystery)",
            "ဝေဖန်ဆန်းစစ်ချက် (Analytical)"
        ]
    )
    
    st.info("💡 Tip: စာသားများကို အချောသတ်ပြီးလျှင် Copy ကူးယူ၍ ပြင်ပ TTS Reader များတွင် အသုံးပြုနိုင်ပါသည်။")

st.title("🎬 High-Quality Movie Recap Generator")
st.write("ဇာတ်လမ်းအစကနေ အဆုံးထိ စိတ်ဝင်စားစရာကောင်းတဲ့ Article များကို ဖန်တီးပါ။")

if 'final_article' not in st.session_state:
    st.session_state.final_article = ""

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🔎 Movie Details")
    movie_name = st.text_input("ဇာတ်ကားအမည် -", placeholder="ဥပမာ - Shutter")
    key_points = st.text_area("အထူးထည့်စေချင်သည့် အချက်များ -", placeholder="ဥပမာ - ဇာတ်သိမ်းပိုင်း Twist ကို သေချာရှင်းပြပေးပါ...", height=150)
    
    generate_btn = st.button("Generate Article ✨")

with col2:
    st.subheader("📄 Generated Content")
    
    if generate_btn:
        if not api_key_input:
            st.error("API Key အရင်ထည့်ပေးပါ!")
        elif not movie_name:
            st.error("ဇာတ်ကားအမည် ထည့်ပေးပါ!")
        else:
            with st.status("Gemini 2.0 က ဇာတ်ကြောင်း ရေးသားနေပါသည်...", expanded=True) as status:
                try:
                    genai.configure(api_key=api_key_input.strip())
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    
                    prompt = f"""
                    မင်းက အတွေ့အကြုံရင့်ကျက်တဲ့ Movie Content Creator တစ်ယောက်ပါ။ {movie_name} ဇာတ်ကားကို 
                    {depth} အနေနဲ့ {style} စတိုင်သုံးပြီး မြန်မာစကားပြော စစ်စစ်နဲ့ ရေးပေးပါ။
                    
                    ညွှန်ကြားချက်များ -
                    ၁။ ဇာတ်လမ်းကို အစကနေ အဆုံးထိ အသေးစိတ်နဲ့ စိတ်ဝင်စားစရာကောင်းအောင် ရေးပါ။
                    ၂။ အကျဉ်းချုပ်ရုံတင်မဟုတ်ဘဲ Storytelling ပုံစံဖြင့် ရှည်ရှည်ဝေးဝေး ရေးပေးပါ။
                    ၃။ [Action] သို့မဟုတ် (Stage Direction) များ လုံးဝမထည့်ပါနှင့်။
                    ၄။ 'အဲ့ဒီမှာတင်' ၊ 'ဒါပေမဲ့ ထူးဆန်းတာက' စသည့် ဆွဲဆောင်မှုရှိသော အသုံးအနှုန်းများ သုံးပါ။
                    {f'အထူးမှာကြားချက် - {key_points}' if key_points else ''}
                    """
                    
                    # Streaming Response
                    full_response = ""
                    placeholder = st.empty()
                    
                    response = model.generate_content(prompt, stream=True)
                    for chunk in response:
                        full_response += chunk.text
                        placeholder.text_area("Writing...", value=full_response, height=500)
                    
                    st.session_state.final_article = full_response
                    status.update(label="ရေးသားပြီးပါပြီ!", state="complete", expanded=False)
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    if st.session_state.final_article:
        st.download_button("📥 Save Article (Text File)", st.session_state.final_article, file_name=f"{movie_name}_recap.txt")