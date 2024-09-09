import streamlit as st
import pandas as pd
import numpy as np
import io

st.title('Aplikasi Filter Pinjaman Sanitasi dan Plafon Pinjaman Ke-')
st.write("File yang dibutuhkan: Daftar Pinjaman dan pivot_simpanan.xlsx")
st.write("Ubah Nama File dan nama Sheet jadi Pinjaman Detail Report")
st.write("Rapihkan data tersebut jadi seperti contoh ini: [Link ke contoh]")

# Function to format numbers
def format_number(value):
    try:
        return f"{float(value):,.0f}"
    except:
        return value

def format_percentage(value):
    try:
        return f"{float(value):.2f}%"
    except:
        return value

def format_date(value):
    try:
        return pd.to_datetime(value).strftime('%d/%m/%Y')
    except:
        return value

# File uploader
uploaded_files = st.file_uploader("Unggah file Excel", accept_multiple_files=True, type=["xlsx"])

df_PDR = None
df_S = None

if uploaded_files:
    for file in uploaded_files:
        if file.name == 'Pinjaman Detail Report.xlsx':
            df_PDR = pd.read_excel(file, engine='openpyxl')
        elif file.name == 'pivot_simpanan.xlsx':
            df_S = pd.read_excel(file, engine='openpyxl')

    if df_PDR is None:
        st.error("File 'Pinjaman Detail Report.xlsx' tidak ditemukan. Mohon upload file yang benar.")
    if df_S is None:
        st.error("File 'pivot_simpanan.xlsx' tidak ditemukan. Mohon upload file yang benar.")

if df_PDR is not None:
    try:
        # Bersihkan spesial karakter
        df_PDR.columns = df_PDR.columns.str.strip().str.replace(r'[^\w\s]', '', regex=True)
        
        # Rapikan file df_pdr
        df_PDR['DUMMY'] = df_PDR['ID'].astype(str) + df_PDR['PENCAIRAN'].astype(str)

        rename_dict = {
            'PINJAMAN MIKRO BISNIS': 'PINJAMAN MIKROBISNIS',
        }
        df_PDR['PRODUK'] = df_PDR['PRODUK'].replace(rename_dict)

        # Format kolom
        numeric_columns = ['JML.PINJAMAN', 'OUTSTANDING', 'ANGSURAN']
        for col in numeric_columns:
            df_PDR[col] = df_PDR[col].apply(format_number)

        df_PDR['RATE (%)'] = df_PDR['RATE (%)'].apply(format_percentage)
        
        date_columns = ['PENGAJUAN', 'PENCAIRAN', 'PEMBAYARAN']
        for col in date_columns:
            df_PDR[col] = df_PDR[col].apply(format_date)

        # Ensure all expected columns are present
        desired_order = [
            'NO.', 'ID', 'ID.PINJAMAN', 'DUMMY', 'NAMA LENGKAP', 'PHONE', 'CENTER', 'GROUP', 'PRODUK', 
            'JML.PINJAMAN', 'OUTSTANDING', 'J.WAKTU', 'RATE (%)', 'ANGSURAN', 'TUJUAN PINJAMAN', 
            'PINJ.KE', 'NAMA F.O.', 'PENGAJUAN', 'PENCAIRAN', 'PEMBAYARAN'
        ]

        for col in desired_order:
            if col not in df_PDR.columns:
                df_PDR[col] = ''

        df_PDR = df_PDR[desired_order]

        st.write('Pinjaman Detail Report:')
        st.dataframe(df_PDR)

        # Filter PU
        df_filter_pu = df_PDR[df_PDR['PRODUK'] == 'PINJAMAN UMUM'].copy()
        st.write("Filter PU")
        st.write(df_filter_pu)

        # Filter PMB
        df_filter_pmb = df_PDR[df_PDR['PRODUK'] == 'PINJAMAN MIKROBISNIS'].copy()
        st.write("Filter PMB")
        st.write(df_filter_pmb)

        # Filter PPD
        df_filter_ppd = df_PDR[df_PDR['PRODUK'] == 'PINJAMAN DT. PENDIDIKAN'].copy()
        st.write("Filter PPD")
        st.write(df_filter_ppd)

        # Filter PSA
        df_filter_psa = df_PDR[df_PDR['PRODUK'] == 'PINJAMAN SANITASI'].copy()
        st.write("Filter PSA")
        st.write(df_filter_psa)

        # Filter ARTA
        df_filter_arta = df_PDR[df_PDR['PRODUK'] == 'PINJAMAN ARTA'].copy()
        st.write("Filter ARTA")
        st.write(df_filter_arta)

        # Filter PRR
        df_filter_prr = df_PDR[df_PDR['PRODUK'] == 'PINJAMAN RENOVASI RUMAH'].copy()
        st.write("Filter PRR")
        st.write(df_filter_prr)

        # Filter PTN
        df_filter_ptn = df_PDR[df_PDR['PRODUK'] == 'PINJAMAN PERTANIAN'].copy()
        st.write("Filter PTN")
        st.write(df_filter_ptn)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses data: {str(e)}")
else:
    st.warning("Silakan upload file 'Pinjaman Detail Report.xlsx' dan 'pivot_simpanan.xlsx'")
