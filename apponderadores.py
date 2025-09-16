import json
import pandas as pd
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Leer credenciales desde secrets
creds_dict = json.loads(st.secrets["gcp_service_account"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

SHEET_URL = st.secrets["SHEET_URL"]
SHEET_NAME = st.secrets["SHEET_NAME"]

# Cargar datos
worksheet = client.open_by_url(SHEET_URL).worksheet(SHEET_NAME)
data = worksheet.get_all_values()
df = pd.DataFrame(data)
df.columns = df.iloc[0]
df = df.drop(0).reset_index(drop=True)

def obtener_ponderador(mes_base, mes_destino):
    try:
        fila = df[df[df.columns[0]] == mes_base]
        if fila.empty:
            return None
        valor = fila[mes_destino].values[0]
        return float(valor.replace(",", ".")) if valor else None
    except KeyError:
        return None

st.title("Calculadora de Ponderadores IPC 🇦🇷")
mes_base = st.selectbox("Mes base", df[df.columns[0]].tolist())
mes_destino = st.selectbox("Mes destino", df.columns[1:].tolist())

if st.button("Calcular ponderador"):
    p = obtener_ponderador(mes_base, mes_destino)
    if p is not None:
        st.success(f"Para actualizar un valor desde el {mes_base} al {mes_destino} tenés que multiplicarlo por: {p}")
    else:
        st.error("No se encontró el ponderador para esa combinación.")



