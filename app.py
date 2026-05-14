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

# -------------------------------------------------
# Standard-Datumswerte
# -------------------------------------------------

heute = datetime.today()

if heute.month == 12:
    next_month = 1
    next_year = heute.year + 1
else:
    next_month = heute.month + 1
    next_year = heute.year

# Erster Tag des Folgemonats
first_day_next_month = datetime(
    next_year,
    next_month,
    1
).date()

# Sechs Monate später
end_month = next_month + 5
end_year = next_year

while end_month > 12:
    end_month -= 12
    end_year += 1

# Letzter Tag des Zielmonats
if end_month == 12:
    next_calc_month = 1
    next_calc_year = end_year + 1
else:
    next_calc_month = end_month + 1
    next_calc_year = end_year

last_day_target_month = (
    datetime(next_calc_year, next_calc_month, 1)
    - timedelta(days=1)
).date()


col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(
        "Startdatum",
        value=first_day_next_month,
        format="DD.MM.YYYY"
    )

with col2:

    # Automatischer Abstand: Ende = letzter Tag des Monats
    # fünf Monate nach dem Startdatum

    auto_end_month = start_date.month + 5
    auto_end_year = start_date.year

    while auto_end_month > 12:
        auto_end_month -= 12
        auto_end_year += 1

    if auto_end_month == 12:
        next_month_calc = 1
        next_year_calc = auto_end_year + 1
    else:
        next_month_calc = auto_end_month + 1
        next_year_calc = auto_end_year

    auto_end_date = (
        datetime(next_year_calc, next_month_calc, 1)
        - timedelta(days=1)
    ).date()

    end_date = st.date_input(
        "Enddatum",
        value=auto_end_date,
        format="DD.MM.YYYY"
    )

col3, col4 = st.columns(2)

with col3:
    start_time = st.time_input(
        "Startzeit",
        value=time(8, 0)
    )

with col4:

    default_end_datetime = datetime.combine(
        datetime.today(),
        start_time
    ) + timedelta(hours=1)

    default_end_time = default_end_datetime.time()

    end_time = st.time_input(
        "Endzeit",
        value=default_end_time
    )


# -------------------------------------------------
# Wochenintervall
# -------------------------------------------------

wochen_intervall = st.selectbox(
    "Terminrhythmus",
    options=[1, 2, 3, 4],
    format_func=lambda x: (
        "Jede Woche" if x == 1 else f"Alle {x} Wochen"
    )
)


# -------------------------------------------------
# Wochentage
# -------------------------------------------------

st.subheader("Wochentage auswählen")

weekday_options = [
    ("Montag", 0),
    ("Dienstag", 1),
    ("Mittwoch", 2),
    ("Donnerstag", 3),
    ("Freitag", 4),
    ("Samstag", 5),
    ("Sonntag", 6),
]

selected_days = []

for day, number in weekday_options:

    default_value = day in [
        "Montag",
        "Dienstag",
        "Mittwoch",
        "Donnerstag"
    ]

    if st.checkbox(day, value=default_value):
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

            # Anzahl Wochen seit Startdatum
            wochen_diff = (
                (current_date - start_date).days // 7
            )

            intervall_passend = (
                wochen_diff % wochen_intervall == 0
            )

            if (
                current_date.weekday() in selected_days
                and intervall_passend
            ):

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
