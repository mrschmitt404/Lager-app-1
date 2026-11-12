import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Viega Material- & Lagerplanung",
    page_icon="🔧",
    layout="wide",
)

# Initialize Session State for Data persistence if not already present
if "inventory_df" not in st.session_state:
    # Base 31 Viega Temponox items
    items_data = [
        ("1703", "Temponox Rohr (6m Stange)", "28 mm", 3, 6, 0, 0),
        ("1703", "Temponox Rohr (6m Stange)", "22 mm", 2, 4, 0, 0),
        ("1703", "Temponox Rohr (6m Stange)", "35 mm", 1, 2, 0, 0),
        ("1716", "Temponox Bogen 90° (II - beidseitig Muffe)", "28 mm", 10, 20, 0, 0),
        ("1716.1", "Temponox Bogen 90° (IA - Muffe/Einsteckende)", "28 mm", 6, 12, 0, 0),
        ("1716", "Temponox Bogen 90° (II - beidseitig Muffe)", "22 mm", 8, 16, 0, 0),
        ("1716.1", "Temponox Bogen 90° (IA - Muffe/Einsteckende)", "22 mm", 4, 8, 0, 0),
        ("1726", "Temponox Bogen 45° (II - beidseitig Muffe)", "28 mm", 4, 8, 0, 0),
        ("1726.1", "Temponox Bogen 45° (IA - Muffe/Einsteckende)", "28 mm", 4, 8, 0, 0),
        ("1726", "Temponox Bogen 45° (II - beidseitig Muffe)", "22 mm", 4, 8, 0, 0),
        ("1726.1", "Temponox Bogen 45° (IA - Muffe/Einsteckende)", "22 mm", 2, 4, 0, 0),
        ("1715", "Temponox Muffe (beidseitig Muffe)", "28 mm", 4, 8, 0, 0),
        ("1715", "Temponox Muffe (beidseitig Muffe)", "22 mm", 4, 8, 0, 0),
        ("1715.5", "Temponox Schiebemuffe (ohne Anschlag)", "28 mm", 2, 4, 0, 0),
        ("1715.1", "Temponox Reduzierstück (Einsteckende/Muffe)", "28 x 22 mm", 4, 8, 0, 0),
        ("1715.1", "Temponox Reduzierstück (Einsteckende/Muffe)", "35 x 28 mm", 2, 4, 0, 0),
        ("1718", "Temponox T-Stück egal", "28 mm", 3, 6, 0, 0),
        ("1718", "Temponox T-Stück reduziert", "28 x 22 x 28 mm", 4, 8, 0, 0),
        ("1717.2", "Temponox T-Stück mit Innengewinde (Rp)", "28 x 1\" x 28 mm", 2, 4, 0, 0),
        ("1717.2", "Temponox T-Stück mit Innengewinde (Rp)", "28 x 1/2\" x 28 mm", 4, 8, 0, 0),
        ("1717.2", "Temponox T-Stück mit Innengewinde (Rp)", "28 x 3/4\" x 28 mm", 2, 4, 0, 0),
        ("1763", "Temponox Anschlussverschraubung flachdichtend (ÜWM)", "28 x G 1 1/2\"", 4, 8, 0, 0),
        ("1763", "Temponox Anschlussverschraubung flachdichtend (ÜWM)", "28 x G 1 1/4\"", 4, 8, 0, 0),
        ("1763", "Temponox Anschlussverschraubung flachdichtend (ÜWM)", "28 x G 1\"", 4, 8, 0, 0),
        ("1765", "Temponox Übergangsverschraubung flachdichtend (AG)", "28 x R 1\" AG", 2, 4, 0, 0),
        ("1762", "Temponox Übergangsverschraubung flachdichtend (IG)", "28 x Rp 1\" IG", 2, 4, 0, 0),
        ("1760", "Temponox Verschraubung Press/Press trennbar", "28 mm", 2, 4, 0, 0),
        ("1711", "Temponox Übergangsstück (Außengewinde)", "28 x R 1\" AG", 4, 8, 0, 0),
        ("1712", "Temponox Übergangsstück (Innengewinde)", "28 x Rp 1\" IG", 4, 8, 0, 0),
        ("1711", "Temponox Übergangsstück (Außengewinde)", "22 x R 3/4\" AG", 4, 8, 0, 0),
        ("1756", "Temponox Endkappe", "28 mm", 2, 4, 0, 0),
    ]
    
    st.session_state.inventory_df = pd.DataFrame(items_data, columns=[
        "Modell", "Artikelbezeichnung", "Dimension", "Ø Verbrauch", "Mindestbestand", "Im Lager", "In Montagekiste"
    ])

if "log_df" not in st.session_state:
    st.session_state.log_df = pd.DataFrame(columns=[
        "Datum", "Baustelle", "Artikel", "Dimension", "Menge", "Monteur"
    ])

st.title("🔧 Viega Temponox – Material & Lager-App")
st.markdown("Einfache mobile Erfassung für Baustellen & Live-Bestandsübersicht.")

# Sidebar Navigation
menu = st.sidebar.selectbox("Menü", [
    "📦 Lagerbestand & Status",
    "🏗️ Baustellen-Verbrauch buchen",
    "⚙️ Stammdaten / Lager anpassen"
])

df = st.session_state.inventory_df

# Calculate Total and Status dynamically
df["Gesamtbestand"] = df["Im Lager"] + df["In Montagekiste"]

# Safely subtract consumption from log even if empty
if not st.session_state.log_df.empty:
    consumption_totals = st.session_state.log_df.groupby(["Artikel", "Dimension"])["Menge"].sum().reset_index()
    df = df.merge(consumption_totals, on=["Artikel", "Dimension"], how="left")
    df["Menge"] = df["Menge"].fillna(0)
    df["Netto-Gesamt"] = df["Gesamtbestand"] - df["Menge"]
else:
    df["Menge"] = 0
    df["Netto-Gesamt"] = df["Gesamtbestand"]

df["Status"] = df.apply(lambda row: "🔴 BESTELLEN!" if row["Netto-Gesamt"] <= row["Mindestbestand"] else "🟢 OK", axis=1)

if menu == "📦 Lagerbestand & Status":
    st.subheader("Aktueller Lagerbestand & Bestell-Ampel")
    
    # KPI Metrics on top
    col1, col2, col3 = st.columns(3)
    total_items = len(df)
    to_order = len(df[df["Status"] == "🔴 BESTELLEN!"])
    col1.metric("Artikel gesamt", total_items)
    col2.metric("Nachbestellungen nötig", to_order, delta_color="inverse")
    col3.metric("Status", "Achtung!" if to_order > 0 else "Alles im grünen Bereich")
    
    st.divider()
    
    # Display Table
    display_df = df[["Modell", "Artikelbezeichnung", "Dimension", "Mindestbestand", "Im Lager", "In Montagekiste", "Menge", "Netto-Gesamt", "Status"]]
    display_df.columns = ["Modell", "Artikel", "Dimension", "Mindest", "Lager", "Kiste", "Verbraucht", "Gesamt", "Status"]
    st.dataframe(display_df, use_container_width=True, height=600)

elif menu == "🏗️ Baustellen-Verbrauch buchen":
    st.subheader("Baustellen-Verbrauch erfassen (Aufmaß)")
    st.markdown("Wähle den verbauten Artikel aus und trage die Stückzahl ein. Das System zieht es sofort vom Lager ab.")
    
    with st.form("verbrauch_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            baustelle = st.text_input("Baustelle / Kunde", placeholder="z.B. EFH Müller")
        with col_b:
            monteur = st.text_input("Monteur", placeholder="Dein Name")
        
        # Dropdown options formatted cleanly
        df["Dropdown_Label"] = df["Artikelbezeichnung"].str.replace("Temponox ", "") + " | " + df["Dimension"] + " (Mod. " + df["Modell"] + ")"
        selected_label = st.selectbox("Artikel & Dimension auswählen", df["Dropdown_Label"].tolist())
        
        menge = st.number_input("Verbrauchte Stück / Stangen", min_value=1, max_value=500, value=1)
        
        submitted = st.form_submit_button("Verbrauch buchen & Bestand aktualisieren")
        
        if submitted:
            selected_row = df[df["Dropdown_Label"] == selected_label].iloc[0]
            new_log = pd.DataFrame({
                "Datum": [pd.Timestamp.now().strftime("%d.%m.%Y %H:%M")],
                "Baustelle": [baustelle if baustelle else "Unbekannt"],
                "Artikel": [selected_row["Artikelbezeichnung"]],
                "Dimension": [selected_row["Dimension"]],
                "Menge": [menge],
                "Monteur": [monteur if monteur else "Team"]
            })
            st.session_state.log_df = pd.concat([st.session_state.log_df, new_log], ignore_index=True)
            st.success(f"Erfolgreich gebucht: {menge}x {selected_label} für Baustelle '{baustelle}'!")

    st.divider()
    st.subheader("Letzte Buchungen auf Baustellen")
    if not st.session_state.log_df.empty:
        st.dataframe(st.session_state.log_df, use_container_width=True)
    else:
        st.info("Bisher noch keine Verbräuche eingetragen.")

elif menu == "⚙️ Stammdaten / Lager anpassen":
    st.subheader("Startbestände anpassen (Regal & Kiste)")
    st.markdown("Hier trägst du ein, was physisch im Regal im Lager oder in den Kisten auf den Autos liegt.")
    
    edited_df = st.data_editor(
        df[["Modell", "Artikelbezeichnung", "Dimension", "Im Lager", "In Montagekiste"]],
        use_container_width=True,
        key="inventory_editor"
    )
    
    if st.button("Bestände speichern"):
        st.session_state.inventory_df["Im Lager"] = edited_df["Im Lager"]
        st.session_state.inventory_df["In Montagekiste"] = edited_df["In Montagekiste"]
        st.success("Bestände erfolgreich aktualisiert!")
