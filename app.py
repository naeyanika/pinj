import streamlit as st
import pandas as pd
import numpy as np
import io



st.title('Aplikasi Filter Pinjaman Sanitasi dan Plafon Pinjaman Ke-')
st.write("""File yang dibutuhkan Daftar Pinjaman dan pivot_simpanan.xlsx""")
st.write("""Ubah Nama File dan nama Sheet jadi Pinjaman Detail Report""")
st.write("""Rapihkan data tersebut jadi seperti contoh ini : https://drive.google.com/file/d/14Ofz53dSVRFzlFrrc8snZmmkHq7CO-R2/view?usp=drive_link """)

# Function to format numbers
def format_no(no):
    try:
        if pd.notna(no):
            return f'{int(no):02d}.'
        else:
            return ''
    except (ValueError, TypeError):
        return str(no)

def format_center(center):
    try:
        if pd.notna(center):
            return f'{int(center):03d}'
        else:
            return ''
    except (ValueError, TypeError):
        return str(center)

def format_kelompok(kelompok):
    try:
        if pd.notna(kelompok):
            return f'{int(kelompok):02d}'
        else:
            return ''
    except (ValueError, TypeError):
        return str(kelompok)

uploaded_files = st.file_uploader("Unggah file Excel", accept_multiple_files=True, type=["xlsx"])

if uploaded_files:
    dfs = {}
    for file in uploaded_files:
        df = pd.read_excel(file, engine='openpyxl')  
        dfs[file.name] = df

if 'Pinjaman Detail Report.xlsx' in dfs and 'pivot_simpanan.xlsx' in dfs :
    df_PDR = dfs['Pinjaman Detail Report.xlsx']
    df_S = dfs['pivot_simpanan.xlsx']

## Bersikan spesial karakter
if df_PDR is not None:
    df_PDR.columns = df_PDR.columns.str.strip().str.replace(r'[^\w\s]', '', regex=True)

    df_PDR = df_PDR.apply(lambda x: x.astype(str).str.strip().str.replace(r'[^\w\s]', '', regex=True))

else:
    st.error(" File Pinjaman Detail Report.xlsx kosong atau tidak ada")

## Rapikan file df_pdr
df_PDR['DUMMY'] = df_PDR['ID ANGGOTA'] + '' + df_PDR['PENCAIRAN']

rename_dict = {
    'PINJAMAN MIKRO BISNIS': 'PINJAMAN MIKROBISNIS',
}
df_PDR['JENIS PINJAMAN'] = df_PDR['JENIS PINJAMAN'].replace(rename_dict)

desired_order = [
    'NO.', 'ID', 'ID.PINJAMAN', 'DUMMY','NAMA LENGKAP', 'PHONE', 'CENTER', 'GROUP', 'PRODUK', 'JML.PINJAMAN', 'OUTSTANDING', 'J.WAKTU', 'RATE (%)', 'ANGSURAN', 'TUJUAN PINJAMAN', 'PINJ.KE', 'NAMA F.O.', 'PENGAJUAN', 'PENCAIRAN', 'PEMBAYARAN'
]

for col in desired_order:
    if col not in df_PDR.columns:
        df_PDR[col] = 0

df_PDR = df_PDR[desired_order]

st.write('Pinjaman Detail Report:')
st.write(df_PDR)


######################################################################################
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
######################################################################################



