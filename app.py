import streamlit as st
import anthropic

st.set_page_config(
    page_title="Autohaus Kießling",
    page_icon="🚗",
    layout= "centered"
)

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

st.title("🚗 Autohaus Kießling")
st.subheader("Ihr digitaler Berater – powered by KI")
st.divider()
with st.chat_message("assistant"):
    st.write("Hallo! Ich bin Max, Ihr digitaler Autoberater beim Autohaus Kießling. 🚗 Wie kann ich Ihnen heute helfen?")

if "nachrichten" not in st.session_state:
    st.session_state.nachrichten = []

for nachricht in st.session_state.nachrichten:
    if nachricht["role"] == "user":
        st.chat_message("user").write(nachricht["content"])
    else:
        st.chat_message("assistant").write(nachricht["content"])

frage = st.chat_input("Wie kann ich Ihnen helfen?")

if frage:
    st.session_state.nachrichten.append({"role": "user", "content": frage})
    st.chat_message("user").write(frage)

    antwort = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system="""
Du bist Max, ein freundlicher Autoberater beim Autohaus Kießling in Zwickau.
Du bist offizieller VW Händler und antwortest immer auf Deutsch.
Du empfiehlst immer eine Probefahrt und sprichst den Kunden mit Namen an.

Aktuelles Fahrzeuginventar:

NEUWAGEN:
- VW Golf 8, Benzin, 2025, ab 28.900€
- VW Tiguan, Diesel, 2025, ab 38.500€
- VW Polo, Benzin, 2025, ab 22.400€

GEBRAUCHTWAGEN:
- VW Golf 7, Benzin, 2019, 89.000km, 16.900€, verfügbar
- VW Passat Kombi, Diesel, 2020, 67.000km, 24.500€, verfügbar
- VW Tiguan, Benzin, 2018, 112.000km, 19.800€, verfügbar
- Skoda Octavia, Diesel, 2021, 45.000km, 21.900€, verfügbar

Öffnungszeiten: Mo-Fr 9-18 Uhr, Sa 9-14 Uhr
Adresse: Musterstraße 1, 08056 Zwickau
Telefon: 0375 123456
""",
        messages=st.session_state.nachrichten
    )

    antwort_text = antwort.content[0].text
    st.session_state.nachrichten.append({"role": "assistant", "content": antwort_text})
    st.chat_message("assistant").write(antwort_text)






