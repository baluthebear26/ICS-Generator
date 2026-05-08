import streamlit as st
from datetime import datetime, timedelta, time
import uuid


st.set_page_config(
    page_title="ICS Generator",
    layout="centered"
)

st.title("📅 ICS Kalender Generator")
st.write(
    "Erzeuge mehrere Kalendereinträge und speichere sie in einer einzigen ICS-Datei."
)


# -------------------------------------------------
# Eingabefelder
# -------------------------------------------------

summary = st.text_input("Titel des Termins", value="Praxis ")

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(
        "Startdatum",
        format="DD.MM.YYYY"
    )

with col2:
    end_date = st.date_input(
        "Enddatum",
        format="DD.MM.YYYY"
    )

col3, col4 = st.columns(2)

with col3:
    start_time = st.time_input(
        "Startzeit",
        value=time(8, 0)
    )

with col4:
    end_time = st.time_input(
        "Endzeit",
        value=time(9, 0)
    )


# -------------------------------------------------
# Wochentage
# -------------------------------------------------

st.subheader("Wochentage auswählen")

weekday_options = {
    "Montag": 0,
    "Dienstag": 1,
    "Mittwoch": 2,
    "Donnerstag": 3,
    "Freitag": 4,
    "Samstag": 5,
    "Sonntag": 6,
}

selected_days = []

cols = st.columns(4)

for index, (day, number) in enumerate(weekday_options.items()):
    with cols[index % 4]:
        if st.checkbox(day):
            selected_days.append(number)


# -------------------------------------------------
# ICS erstellen
# -------------------------------------------------

if st.button("ICS-Datei erzeugen"):

    if not summary:
        st.error("Bitte einen Titel eingeben.")

    elif not selected_days:
        st.error("Bitte mindestens einen Wochentag auswählen.")

    elif end_date < start_date:
        st.error("Enddatum darf nicht vor dem Startdatum liegen.")

    else:

        events = []

        current_date = start_date

        while current_date <= end_date:

            if current_date.weekday() in selected_days:

                start_datetime = datetime.combine(
                    current_date,
                    start_time
                )

                end_datetime = datetime.combine(
                    current_date,
                    end_time
                )

                uid = str(uuid.uuid4())

                dtstamp = datetime.utcnow().strftime(
                    "%Y%m%dT%H%M%SZ"
                )

                event = f"""BEGIN:VEVENT
UID:{uid}
DTSTAMP:{dtstamp}
DTSTART:{start_datetime.strftime('%Y%m%dT%H%M%S')}
DTEND:{end_datetime.strftime('%Y%m%dT%H%M%S')}
SUMMARY:{summary}
END:VEVENT
"""

                events.append(event)

            current_date += timedelta(days=1)

        ics_content = (
            "BEGIN:VCALENDAR\n"
            "VERSION:2.0\n"
            "PRODID:-//Streamlit ICS Generator//DE\n"
        )

        ics_content += "\n".join(events)
        ics_content += "\nEND:VCALENDAR"

        filename = f"kalender_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ics"

        st.success(f"{len(events)} Termine wurden erzeugt.")

        st.download_button(
            label="📥 ICS-Datei herunterladen",
            data=ics_content,
            file_name=filename,
            mime="text/calendar"
        )


# -------------------------------------------------
# Hinweise
# -------------------------------------------------

with st.expander("Hinweise"):
    st.markdown(
        """
        ### Verwendung

        1. Titel eingeben
        2. Zeitraum auswählen (Datum im deutschen Format)
        3. Uhrzeiten festlegen
        4. Wochentage auswählen
        5. ICS-Datei erzeugen

        Die erzeugte Datei kann in:

        - Apple Kalender
        - Outlook
        - Google Kalender
        - iPhone Kalender

        importiert werden.
        """
    )


# -------------------------------------------------
# Start-Hinweis
# -------------------------------------------------

st.divider()

st.code(
    "streamlit run app.py",
    language="bash"
)
