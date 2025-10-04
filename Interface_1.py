import json
from datetime import datetime
import streamlit as st
import streamlit_copybutton  # <– Zusatzmodul für Copy-Button

# Seiteneinstellungen
st.set_page_config(page_title="Zettelkasten · Philosophischer Promptbuilder", page_icon="🗂️", layout="wide")
st.title("🗂️ Zettelkasten · Philosophischer Promptbuilder")
st.caption("Hinweis: Keine personenbezogenen oder internen Daten eingeben.")

# ---------- Funktion für Kriterieneingabe ----------
def kriterienfeld(label, vorschlaege, key_text, key_dropdown):
    st.markdown(f"**{label}**")
    selected = st.multiselect(
        f"{label} · Vorschläge (Mehrfachauswahl möglich)", 
        options=vorschlaege, 
        key=key_dropdown
    )
    freie_eingabe = st.text_area(
        f"{label} · Eigene Eingaben (eine pro Zeile)", 
        key=key_text, 
        height=80
    )
    eigene = [x.strip("- ").strip() for x in freie_eingabe.splitlines() if x.strip()]
    return selected + eigene

# ---------- Linke und rechte Spalte ----------
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

# ---------- Kriterien-Felder ----------
must_kriterien = kriterienfeld(
    "Muss-Kriterien",
    [
        "keine personenbezogenen Daten",
        "prägnant, keine Füllwörter",
        "Begriffe klar definiert",
        "verwendete Theorie muss erkennbar sein",
        "These klar formuliert",
        "Zettellänge maximal wie angegeben",
    ],
    key_text="must_text",
    key_dropdown="must_select"
)

nice_kriterien = kriterienfeld(
    "Nice-to-have",
    [
        "überraschendes Bild",
        "prägnanter Merksatz",
        "Verbindung zu Luhmann",
        "analoge Beispiele",
        "Querverweise zu anderen Zetteln",
        "humorvolle Formulierung",
    ],
    key_text="nice_text",
    key_dropdown="nice_select"
)

exclude_kriterien = kriterienfeld(
    "Ausschlüsse",
    [
        "Fachjargon ohne Erklärung",
        "Quellen erfinden",
        "GPT verweist auf sich selbst",
        "unbelegte Allgemeinplätze",
        "Floskeln ohne Gehalt",
    ],
    key_text="exclude_text",
    key_dropdown="exclude_select"
)

# ---------- Briefing ----------
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
        "must": must_kriterien,
        "nice_to_have": nice_kriterien,
        "exclude": exclude_kriterien
    }
}

header_json = json.dumps(header, ensure_ascii=False, indent=2)
final_prompt = f"""[HEADER_JSON_START]
{header_json}
[HEADER_JSON_END]

[CONTENT_START]
{(briefing or '').strip()}
[CONTENT_END]""".strip()

# ---------- Vorschau ----------
st.markdown("### Vorschau · Finaler Prompt")
st.text_area("Prompt", value=final_prompt, height=380, key="prompt_area")

# ---------- Kopier-Button (funktioniert mit streamlit-copybutton) ----------
st.markdown("### 📋 Prompt in Zwischenablage kopieren")
streamlit_copybutton.copybutton(final_prompt)

# ---------- Download-Button ----------
st.download_button(
    "⬇️ Als .txt speichern",
    data=final_prompt.encode("utf-8"),
    file_name="zettel_prompt.txt",
    mime="text/plain"
)

st.markdown("---")
st.markdown("**Tipp:** Füge diesen Prompt in deinen CustomGPT ein. Der GPT sollte den oben beschriebenen Systemprompt nutzen, damit er den Header korrekt interpretiert und nur die gewünschte Ausgabe liefert.")
