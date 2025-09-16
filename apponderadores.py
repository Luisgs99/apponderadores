import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

# --- CONFIGURACIÓN ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/14Iw0tKrbcqeC-xGkTABUS2gjG2OJYA18iAzb8X-ma-U/edit#gid=396533980"
SHEET_NAME = "Ponderador IPC 19-25"
CREDENTIALS_FILE = "sofia-454214-d2cad15f9b9d.json"

# --- CONEXIÓN ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

# Abrir hoja
worksheet = client.open_by_url(SHEET_URL).worksheet(SHEET_NAME)
data = worksheet.get_all_values()

# DataFrame
df = pd.DataFrame(data)
df.columns = df.iloc[0]
df = df.drop(0).reset_index(drop=True)

# --- FUNCIÓN ---
def obtener_ponderador(mes_base, mes_destino):
    try:
        fila = df[df[df.columns[0]] == mes_base]
        if fila.empty:
            return None
        valor = fila[mes_destino].values[0]
        return float(valor.replace(",", ".")) if valor else None
    except KeyError:
        return None

# --- INTERFAZ STREAMLIT ---
st.title("Calculadora de Ponderadores IPC 🇦🇷")

mes_base = st.selectbox("Mes base", df[df.columns[0]].tolist())
mes_destino = st.selectbox("Mes destino", df.columns[1:].tolist())

if st.button("Calcular ponderador"):
    ponderador = obtener_ponderador(mes_base, mes_destino)
    if ponderador is not None:
        st.success(f"Ponderador de {mes_base} a {mes_destino}: {ponderador}")
    else:
        st.error("No se encontró el ponderador para esa combinación.")
