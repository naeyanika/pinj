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
        # Bersihkan spesial karakter pada kolom header
        df_PDR.columns = df_PDR.columns.str.strip().str.replace(r'[^\w\s]', '', regex=True)
        
        # Function to clean special characters in the DataFrame
        def clean_special_chars(df):
            for col in df.columns:
                if df[col].dtype == 'object':  # Only apply this to string columns
                    # Replace non-breaking spaces and other special characters with normal space
                    df[col] = df[col].str.replace(r'\s+', ' ', regex=True).str.strip()
                    # Replace any non-word characters (including special characters) with nothing
                    df[col] = df[col].str.replace(r'[^\w\s]', '', regex=True)
            return df

        # Apply cleaning function to df_PDR (remove special characters from all columns)
        df_PDR = clean_special_chars(df_PDR)
        
        # Debugging: Print out the available column names to check if 'JML.PINJAMAN' exists
        st.write("Kolom yang tersedia di df_PDR:")
        st.write(df_PDR.columns.tolist())

        # Cek apakah kolom 'JML.PINJAMAN' ada di DataFrame
        numeric_columns = ['JMLPINJAMAN', 'OUTSTANDING', 'ANGSURAN']  # Cleaned version of column names
        for col in numeric_columns:
            if col in df_PDR.columns:
                df_PDR[col] = df_PDR[col].apply(format_number)
            else:
                st.warning(f"Kolom '{col}' tidak ditemukan di Pinjaman Detail Report.xlsx")

        # Format kolom RATE (%)
        if 'RATE ' in df_PDR.columns:
            df_PDR['RATE '] = df_PDR['RATE '].apply(format_percentage)
        else:
            st.warning("Kolom 'RATE (%)' tidak ditemukan di Pinjaman Detail Report.xlsx")

        # Format kolom tanggal
        date_columns = ['PENGAJUAN', 'PENCAIRAN', 'PEMBAYARAN']
        for col in date_columns:
            if col in df_PDR.columns:
                df_PDR[col] = df_PDR[col].apply(format_date)
            else:
                st.warning(f"Kolom '{col}' tidak ditemukan di Pinjaman Detail Report.xlsx")

        # Susun ulang kolom sesuai dengan urutan yang diinginkan
        desired_order = [
            'NO', 'ID', 'IDPINJAMAN', 'DUMMY', 'NAMA LENGKAP', 'PHONE', 'CENTER', 'GROUP', 'PRODUK', 
            'JMLPINJAMAN', 'OUTSTANDING', 'JWAKTU', 'RATE ', 'ANGSURAN', 'TUJUAN PINJAMAN', 
            'PINJKE', 'NAMA FO', 'PENGAJUAN', 'PENCAIRAN', 'PEMBAYARAN'
        ]

        # Pastikan semua kolom ada, jika tidak, tambahkan kolom kosong
        for col in desired_order:
            if col not in df_PDR.columns:
                df_PDR[col] = ''

        df_PDR = df_PDR[desired_order]

        st.write('Pinjaman Detail Report:')
        st.dataframe(df_PDR)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses data: {str(e)}")
else:
    st.warning("Silakan upload file 'Pinjaman Detail Report.xlsx' dan 'pivot_simpanan.xlsx'")


       import streamlit as st
import pandas as pd
import numpy as np
import io

st.title('Aplikasi Filter Pinjaman Sanitasi dan Plafon Pinjaman Ke-')
st.write("File yang dibutuhkan: Daftar Pinjaman dan pivot_simpanan.xlsx")
st.write("Ubah Nama File dan nama Sheet jadi Pinjaman Detail Report")
st.write("Rapihkan data tersebut jadi seperti contoh ini: [Link ke contoh]")
st.write("Hapus karakter spesial terlebih dahulu pada file excel nya")

## FUNGSI FORMAT NOMOR
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

## SESI UPLOAD FILE   
uploaded_files = st.file_uploader("Upload files", accept_multiple_files=True, type=['xlsx'])

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

    ## SESI PENAMBAHAN DUMMY
    df_PDR['PENGAJUAN']
    df_PDR['DUMMY'] = df_PDR['ID'].astype(str) + '' + df_PDR['PENCAIRAN'].astype(str)
    df_PDR['CENTER'] = df_PDR['CENTER'].astype(str).str[:3]
    df_PDR['PHONE'] = df_PDR['PHONE'].astype(str).apply(lambda x: '0' + x if not x.startswith('0') else x)
    
    df_PDR['PENGAJUAN'] = pd.to_datetime(df['PENGAJUAN']).dt.strftime('%d/%m/%Y')
    df_PDR['PENCAIRAN'] = pd.to_datetime(df['PENCAIRAN']).dt.strftime('%d/%m/%Y')
    df_PDR['PEMBAYARAN'] = pd.to_datetime(df['PEMBAYARAN']).dt.strftime('%d/%m/%Y')

    rename_dict = {
        'PINJAMAN MIKRO BISNIS': 'PINJAMAN MIKROBISNIS'
    }

    df_PDR['PRODUK'] = df_PDR['PRODUK'].replace(rename_dict)

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


    st.warning("Silakan upload file 'Pinjaman Detail Report.xlsx' dan 'pivot_simpanan.xlsx'")


#------------------ Proses Filter

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
