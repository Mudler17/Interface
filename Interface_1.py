import json
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Zettelkasten · Philosophischer Promptbuilder", page_icon="🗂️", layout="wide")
st.title("🗂️ Zettelkasten · Philosophischer Promptbuilder")
st.caption("Hinweis: Keine personenbezogenen oder internen Daten eingeben.")

# ---------- Menüs ----------
col1, col2 = st.columns(2)

with col1:
    denkhorizont = st.selectbox(
        "Denkhorizont (Gedanklicher Rahmen)",
        [
            "Erkenntnistheoretiker:in",
            "Systemtheoretiker:in (Luhmann)",
            "Phänomenolog:in",
            "Dialektiker:in",
            "Dekonstrukteur:in",
            "Kritische Theorie",
            "Strukturalist:in",
            "Poststrukturalist:in",
            "Analytische Philosophie",
            "Kognitionswissenschaft / Predictive Processing",
            "Essayist:in",
            "Poet:in",
            "Künstler:in",
            "Analogiebauer:in",
            "Narrativ-Designer:in",
        ],
        index=2
    )

    ausdrucksmodus = st.selectbox(
        "Ausdrucksmodus (Stil)",
        [
            "präzise & analytisch",
            "spekulativ & offen",
            "poetisch & bildhaft",
            "aphoristisch & verdichtet",
            "systematisch & strukturiert",
            "kritisch & dialektisch",
            "experimentell & spielerisch",
        ],
        index=0
    )

    ziel = st.selectbox(
        "Ziel (Art des Zettels)",
        [
            "Begriff klären",
            "These entwickeln",
            "Gegenzettel erzeugen",
            "Analogie entwerfen",
            "Theorie verbinden (Brückenzettel)",
            "Map of Content (Themenlandkarte)",
            "Kreativer Essay / Notiz",
        ],
        index=1
    )

with col2:
    ausgabe = st.selectbox("Ausgabeformat", ["markdown", "liste", "tabelle", "yaml", "json"], index=0)
    laenge = st.select_slider("Ziellänge (Wörter)", options=[150, 300, 500, 700, 1000, 1500], value=500)

    struktur = st.multiselect(
        "Strukturelemente",
        ["leitidee", "herleitung", "beispiele", "reflexion", "implikationen", "offene_fragen", "begriffsarbeit", "verweise"],
        default=["leitidee", "herleitung", "reflexion"]
    )

must = st.text_area("Muss-Kriterien (1/Zeile)", height=90, placeholder="- keine personenbezogenen Daten\n- prägnant, keine Füllwörter")
nice = st.text_area("Nice-to-have (1/Zeile)", height=70, placeholder="- überraschendes Bild\n- 1 kurzer Merksatz")
exclude = st.text_area("Ausschlüsse (1/Zeile)", height=60, placeholder="- Fachjargon ohne Erklärung\n- Quellen erfinden")

st.markdown("### Briefing / Inhalt")
briefing = st.text_area(
    "Worum geht's? (Thema, Thesen, Zitate/Quellen, zu verbindende Theorien …)",
    height=220,
    placeholder="z. B. 'Begriff: Plastizität (Malabou) mit Predictive Processing koppeln; Risiken ästhetischer Metaphern; Bezug zu Luhmann.'"
)

# ---------- Header bauen ----------
header = {
    "protocol": "zettel.app/1.0",
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "locale": "de-DE",
    "profile": "zettel",
    "meta": {
        "denkhorizont": denkhorizont,
        "ausdrucksmodus": ausdrucksmodus,
        "ziel": ziel,
        "ausgabe_format": ausgabe,
        "laenge_woerter": laenge
    },
    "struktur": struktur,
    "compliance": ["keine_personenbezogenen_daten"],
    "prio": ["must", "meta", "nice_to_have"],
    "constraints": {
        "must": [x.strip("- ").strip() for x in must.splitlines() if x.strip()],
        "nice_to_have": [x.strip("- ").strip() for x in nice.splitlines() if x.strip()],
        "exclude": [x.strip("- ").strip() for x in exclude.splitlines() if x.strip()]
    }
}

header_json = json.dumps(header, ensure_ascii=False, indent=2)
final_prompt = f"""[HEADER_JSON_START]
{header_json}
[HEADER_JSON_END]

[CONTENT_START]
{(briefing or '').strip()}
[CONTENT_END]""".strip()

# ---------- Vorschau + Copy ----------
st.markdown("### Vorschau · Finaler Prompt")
st.text_area("Prompt", value=final_prompt, height=380, key="prompt_area")

COPY_JS = """
<script>
function copyPrompt(){
  const el = document.getElementById("prompt_area");
  if (!el) return;
  const text = el.value || el.textContent || "";
  navigator.clipboard.writeText(text).then(()=>{
    const note = document.getElementById("copy-note");
    if(note){ note.innerText = "✅ Prompt kopiert"; }
  });
}
</script>
"""
st.markdown(COPY_JS, unsafe_allow_html=True)
st.markdown('<div id="copy-note" style="margin:0.4rem 0; color:#3a7;"></div>', unsafe_allow_html=True)

st.button(
    "📋 Prompt in Zwischenablage kopieren",
    on_click=lambda: components.html(
        COPY_JS + '<button onclick="copyPrompt()">copy</button><script>copyPrompt()</script>',
        height=0
    )
)

st.download_button(
    "⬇️ Als .txt speichern",
    data=final_prompt.encode("utf-8"),
    file_name="zettel_prompt.txt",
    mime="text/plain"
)

st.markdown("---")
st.markdown("**Tipp:** Füge diesen Prompt in deinen CustomGPT ein. Der GPT sollte den oben beschriebenen Systemprompt nutzen, damit er den Header korrekt interpretiert und nur die gewünschte Ausgabe liefert.")

