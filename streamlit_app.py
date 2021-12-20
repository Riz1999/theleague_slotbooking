import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import pytz
from datetime import datetime

SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SPREADSHEET_ID = "14afCQaLe9KOHw5KPQupqWwCQJUmthuUPg_Tvs4jbhXY"
SHEET_NAME = "booked_slots"
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"

def header2(url): 
    st.markdown(f'<p style="color:#1261A0;font-size:40px;border-radius:2%;"><center><strong>{url}</strong></center></p>', unsafe_allow_html=True)

def get_data(gsheet_connector) -> pd.DataFrame:
    values = (
        gsheet_connector.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:E",
        )
        .execute()
    )

    df = pd.DataFrame(values["values"])
    df.columns = df.iloc[0]
    df = df[1:]
    return df


def add_row_to_gsheet(gsheet_connector, row) -> None:
    values = (
        gsheet_connector.values()
        .append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:E",
            body=dict(values=row),
            valueInputOption="USER_ENTERED",
        )
        .execute()
    )

@st.experimental_singleton()
def connect_to_gsheet():
    cred = {
  "type": "service_account",
  "project_id": "focus-sequencer-335515",
  "private_key_id": "4ad2d73126cd5338829bcb1650707c5ab5cb3051",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQC05g6fDjKWRBCq\ndbnaUTYTpJu9uKq7b7ug9a+x84tDYHyfVo8+JEDz7EZd9gZGf+jx2QxQsJxqxp8e\ngO0fUZ6M9/1YdMICEqoHSUi/Em0d7bAGo8LSbCzn0TvK9zk2bhW4iKupWBJ0henB\nPbKLRVxUzmEcdhFqlziK1+z9YrmnKdBeXNTaMDJdYFjLskOhZ2Nos9h/WgEytlz/\n8tc9uxLrp6fkInK6g4eSm3OsI0w3YZfcN7/THrxRGLT9cpOUwPdIDGVFQJjJ1++k\nW2vWH4R67/YPEWoBMAuVTk4N7GSjSJvAS0P3J7q1u75S48npji/f3wGygr4xosHu\nlb4WnkjHAgMBAAECggEAL2wqBBdoOo1QYydml+13RDIAY/2PwIBbiygtLXTfmsOm\nF+1Msuk1H9zeW459+ahZjGEugc6yyqkUGJ6Kyw2OB32RbEl7fKig6zUSfYiak2B2\np17x2VDjesgWqTAjTvoP9qbZfZTpjaN3cqG2dx0xRcgunBP1n+BRwdA2P/zMF56E\nRWjnQk9EAzThfQ2v5p9I1WIaiwP06VRyEiUsI1+6S0qiPBhpA+GZY0yAQMO4wFg/\n8Q3k8rCcQivQIj0iaYnckEUsSNsa3QCjKlWa+1gHkqlfNEctWaqLVGpMdDHdz9cN\nVc+5DRIF6SPQvOufv5LrvVJyA4vIyxygiv+yptzDYQKBgQD1TzlLfgOrhv7OO6Xv\nDHA1VwVBhcTXuFgRupOLgf1Lturiq0OIDvRwxFvXHnXC2nr0U3raC2O1jS91WNhl\nnR0zmBd1EEv/8gzkP6em9F6xB7hSiNu+3HCorR0QarV+bg2CrHlszA54+Mfe4pvl\n7vL7zzyPfA2OOfqjkcvKf50r5wKBgQC8yD01Mr4OY4OG0thSC0+X6b/Q4meekBDV\nrIpcoUW6lbvn4KgvYUcV1rD7agseoPlwab1WTQm9XFQU2udPcko/WHbdB4KedXiv\nsgZhfPFlURiDbRTe0FKB8/oQ1N2wbbTJ5ciLaMVtHIHEBoDgG/lCQvshLQVvZp9t\n4pmp8VNgIQKBgQCCVl6l2sWObIKUByNKGPzBioPzZWTKDVtVyCE+3Yk8omq4lrCh\n6Pg9tkbpzHhbWIQ9ruE2WxjWTLarjdIkY08xq5zDCS6oRe5Nk/i6/1oUi3qG98px\n5WRCawBnSZs3Grg49vTpNp517hEcPqEAkW4vFtQhlJMLP4kJQZza8eULfwKBgQCZ\n8eRP9HAeBbKlCF1VElo2tGwyZ9495JeF120BOpZFIIOaBI7CDF7OhUPP0dr9gCHJ\nNMEsligCHj+Gvjfwhm/blkVf2xb+JydihxdC+oNTrr0Bt7tUM6eEx7M9dIjPrbbH\nCbXvUWHlp2B+vRrtJoKuMTbfB/qtrI8IKchLWDs4YQKBgQDJ5ySsyJewEXbefo/l\nGJBkV1RZSSA/qkmgQOgJWAjgteKxLqgahGfZFD+lD0c0Ot66oper1rOTU2Bgug+V\nl2jkowt1yNs4AVcbN8Q721kycWj7hiNpqrmWXw+MIfiAiL5qVHsbHnJfqxtnAyiu\n6ZfmW3PboX9B5usytdfzww4qBA==\n-----END PRIVATE KEY-----\n",
  "client_email": "access-drive@focus-sequencer-335515.iam.gserviceaccount.com",
  "client_id": "109156515093815992059",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/access-drive%40focus-sequencer-335515.iam.gserviceaccount.com"
}

    # Create a connection object.
    credentials = service_account.Credentials.from_service_account_info(cred,
        scopes=[SCOPE],
    )

    service = build("sheets", "v4", credentials=credentials)
    gsheet_connector = service.spreadsheets()
    return gsheet_connector


def slot_main():

    st.set_page_config(page_title="The League: Slot Booking", layout="centered")

    col1, col2, col3 = st.columns([0.4,1,0.2])
    with col2:
        st.image("league.jpeg",width = 300)

    col1, col2, col3 = st.columns([0.2,2,0.2])

    with col2:
        st.title("Slot Booking for The League")

    gsheet_connector = connect_to_gsheet()

    mail_id = st.text_input("Enter your woxsen Mail ID")

    if len(mail_id) == 0 or "woxsen.edu.in" in mail_id:
        
        name = st.text_input("Enter your Name")
        contact = st.text_input("Enter your contact")

        if len(name) != 0 and len(contact) != 0 and len(mail_id) != 0:
            sports = ["-","Football pitch 1","Football pitch 2","Box Cricket","Basketball",
                      "Sand Volleyball","Volleyball Court 1","Volleyball Court 2",
                      "Lawn Tennis Court 1","Lawn Tennis Court 2","Kabaddi","Golf","Croquet"]
            sports.sort()
            sport_type = st.selectbox("Choose your Venue",sports)


            if sport_type != "-":
                
                df = get_data(gsheet_connector)
                time_df = df[df["Venue"] == sport_type]
                
                booked = list(time_df["Slot Timing"])
                
                all_slots = []
                
                UTC = pytz.utc
                IST = pytz.timezone('Asia/Kolkata')
                
                hr = str(datetime.now(IST).time())

                if int(hr[0:2]) == 22:
                    header2("Booking opens at 12AM")
                else:
                    for i in range(int(hr[0:2]),22):
                       x = "{}:00 - {}:00".format(i+1,i+2)
                       all_slots.append(x)
                    
                    new_slots = ["-"]

                    for s in all_slots:
                        if s not in booked:
                            new_slots.append(s)

                    del_slots = []

                    for i in range(0,6):
                        x = "{}:00 - {}:00".format(i,i+1)
                        del_slots.append(x)

                    for i in del_slots:
                        if i in new_slots:
                            new_slots.remove(i)

                    if len(new_slots) == 1:
                        header2("No Slots Available")

                    else:
                        slot_time = st.selectbox("Choose your time slot", new_slots)

                        if slot_time != "-":
                            if st.button("Book Slot"):
                                add_row_to_gsheet(
                                    gsheet_connector, [[name, mail_id, contact, sport_type, slot_time]]
                                )
                                header2("Your slot has been booked!")
                                st.success(" **Take a Screenshot of the slot details** ")
                                st.write("**Name:**",name)
                                st.write("**Venue:**", sport_type)
                                st.write("**Slot Time:**", slot_time)
                                st.info("Click refresh before choosing different time slot")
                    st.button("refresh")


    else:
        st.error("You are not allowed to book a slot. Please enter woxsen mail ID")



if __name__ == "__main__":
    slot_main()
