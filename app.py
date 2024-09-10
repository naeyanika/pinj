import streamlit as st
import pandas as pd
import numpy as np
import pyarrow as pa
import io

st.title('Aplikasi Filter Pinjaman Sanitasi dan Plafon Pinjaman Ke-')
st.write("""File yang dibutuhkan: Daftar Pinjaman dan pivot_simpanan.xlsx""")
st.write("""Ubah Nama File dan nama Sheet jadi Pinjaman Detail Report""")
st.write("""Rapihkan data tersebut jadi seperti contoh ini: https://drive.google.com/file/d/14Ofz53dSVRFzlFrrc8snZmmkHq7CO-R2/view?usp=drive_link""")
st.write("""Hapus karakter spesial terlebih dahulu pada file excel nya, lengkapnya ada disini tutorialnya : https://drive.google.com/file/d/1xABUwrMatieKFsNeUbOWl2KuDh6BVLwy/view?usp=drive_link """)

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
    elif df_S is None:
        st.error("File 'pivot_simpanan.xlsx' tidak ditemukan. Mohon upload file yang benar.")
    else:
    ## SESI PENAMBAHAN DUMMY
        for col in ['PENGAJUAN', 'PENCAIRAN', 'PEMBAYARAN']:
            df_PDR[col] = pd.to_datetime(df_PDR[col]).dt.strftime('%d%m%Y')
        df_PDR['DUMMY'] = df_PDR['ID'].astype(str) + '' + df_PDR['PENGAJUAN']
        df_PDR['CENTER'] = df_PDR['CENTER'].astype(str).str[:3]
        df_PDR['PHONE'] = df_PDR['PHONE'].astype(str).apply(lambda x: '0' + x if not x.startswith('0') else x)

        rename_dict = {
        'PINJAMAN MIKRO BISNIS': 'PINJAMAN MIKROBISNIS'
        }

        df_PDR['PRODUK'] = df_PDR['PRODUK'].replace(rename_dict)

        desired_order = [
                    'NO.', 'ID', 'ID.PINJAMAN', 'DUMMY', 'NAMA LENGKAP', 'PHONE', 'CENTER', 'GROUP', 'PRODUK', 'JML.PINJAMAN', 'OUTSTANDING', 'J.WAKTU', 'RATE (%)', 'ANGSURAN', 'TUJUAN PINJAMAN', 'PINJ.KE', 'NAMA F.O.', 'PENGAJUAN', 'PENCAIRAN', 'PEMBAYARAN'
        ]

        for col in desired_order:
            if col not in df_PDR.columns:
                df_PDR[col] = ''

        df_PDR = df_PDR[desired_order]

        df_PDR['PENGAJUAN'] = pd.to_datetime(df_PDR['PENGAJUAN'], format='%d%m%Y').dt.strftime('%d/%m/%Y')
        df_PDR['PENCAIRAN'] = pd.to_datetime(df_PDR['PENCAIRAN'], format='%d%m%Y').dt.strftime('%d/%m/%Y')
        df_PDR['PEMBAYARAN'] = pd.to_datetime(df_PDR['PEMBAYARAN'], format='%d%m%Y').dt.strftime('%d/%m/%Y')

        st.write('Pinjaman Detail Report:')
        st.dataframe(df_PDR) 

#------------------------ SIMPANAN ------------------------------#
    st.write("Transaksi Simpanan:")
    st.write(df_S)
#------------------ Proses Filter
    # Filter PU
    df_filter_pu = df_PDR[df_PDR['PRODUK'] == 'PINJAMAN UMUM'].copy()

    # Filter PMB
    df_filter_pmb = df_PDR[df_PDR['PRODUK'] == 'PINJAMAN MIKROBISNIS'].copy()

    # Filter PPD
    df_filter_ppd = df_PDR[df_PDR['PRODUK'] == 'PINJAMAN DT. PENDIDIKAN'].copy()

    # Filter PSA
    df_filter_psa = df_PDR[df_PDR['PRODUK'] == 'PINJAMAN SANITASI'].copy()

    # Filter ARTA
    df_filter_arta = df_PDR[df_PDR['PRODUK'] == 'PINJAMAN ARTA'].copy()

    # Filter PRR
    df_filter_prr = df_PDR[df_PDR['PRODUK'] == 'PINJAMAN RENOVASI RUMAH'].copy()

    # Filter PTN
    df_filter_ptn = df_PDR[df_PDR['PRODUK'] == 'PINJAMAN PERTANIAN'].copy()

#----------------- ANOMALI

#---------------------------------- PU -------------------------------------------#
    desired_order = [
        'NO.', 'ID', 'ID.PINJAMAN', 'DUMMY', 'NAMA LENGKAP', 'CENTER', 'GROUP', 'PRODUK', 'JML.PINJAMAN','J.WAKTU', 'NAMA F.O.', 'PINJ.KE'
        ]

    for col in desired_order:
            if col not in df_filter_pu.columns:
                df_filter_pu[col] = ''

    df_filter_pu = df_filter_pu[desired_order]

#Buat Kriteria PU
    def check_criteria(row):
            if row['PRODUK'] == 'PINJAMAN UMUM':
                if row['PINJ.KE'] == 1 and 1 <= row['JML.PINJAMAN'] <= 3000000:
                    return True
                elif row['PINJ.KE'] == 2 and 1 <= row['JML.PINJAMAN'] <= 4000000:
                    return True
                elif row['PINJ.KE'] == 3 and 1 <= row['JML.PINJAMAN'] <= 6000000:
                    return True
                elif row['PINJ.KE'] == 4 and 1 <= row['JML.PINJAMAN'] <= 8000000:
                    return True
                elif row['PINJ.KE'] == 5 and 1 <= row['JML.PINJAMAN'] <= 10000000:
                    return True
                elif row['PINJ.KE'] >= 6 and 1 <= row['JML.PINJAMAN'] <= 12000000:
                    return True
                else:
                    return False
            else:
                return False

# Tambahkan Kolom Untuk Cek Kriteria
    df_filter_pu['CEK KRITERIA'] = df_filter_pu.apply(check_criteria, axis=1)

    st.write("Anomali PU:")
    st.write(df_filter_pu)


#----------------------------------------- PMB ---------------------------------------#

    desired_order = [
            'NO.', 'ID', 'ID.PINJAMAN', 'DUMMY', 'NAMA LENGKAP', 'CENTER', 'GROUP', 'PRODUK', 'JML.PINJAMAN','J.WAKTU', 'NAMA F.O.', 'PINJ.KE'
            ]

    for col in desired_order:
            if col not in df_filter_pmb.columns:
                df_filter_pmb[col] = ''

    df_filter_pmb = df_filter_pmb[desired_order]

#Buat Kriteria PMB
    def check_criteria(row):
            if row['PRODUK'] == 'PINJAMAN MIKROBISNIS':
                if row['PINJ.KE'] == 1 and 1 <= row['JML.PINJAMAN'] <= 15000000:
                    return True
                elif row['PINJ.KE'] >= 2 and 1 <= row['JML.PINJAMAN'] <= 30000000:
                    return True
                else:
                    return False
            else:
                return False


    df_filter_pmb['CEK KRITERIA'] = df_filter_pmb.apply(check_criteria, axis=1)

    st.write("Anomali PMB:")
    st.write(df_filter_pmb)

#--------------------------------------- PPD --------------------------------------#
    desired_order = [
            'NO.', 'ID', 'ID.PINJAMAN', 'DUMMY', 'NAMA LENGKAP', 'CENTER', 'GROUP', 'PRODUK', 'JML.PINJAMAN','J.WAKTU', 'NAMA F.O.', 'PINJ.KE'
        ]

    for col in desired_order:
            if col not in df_filter_ppd.columns:
                df_filter_ppd[col] = ''


#Buat Kriteria DTP 
    def check_criteria(row):
            if row['PRODUK'] == 'PINJAMAN DT. PENDIDIKAN':
                if 500000 <= row['JML.PINJAMAN'] <= 10000000:
                    return True
                else:
                    return False
            else:
                return False
    
    df_filter_ppd['CEK KRITERIA'] = df_filter_ppd.apply(check_criteria, axis=1)

    st.write("Anomali DTP:")
    st.write(df_filter_ppd)

#----------------------------------------- ARTA --------------------------------#
    desired_order = [
            'NO.', 'ID', 'ID.PINJAMAN', 'DUMMY', 'NAMA LENGKAP', 'CENTER', 'GROUP', 'PRODUK', 'JML.PINJAMAN','J.WAKTU', 'NAMA F.O.', 'PINJ.KE'
            ]

    for col in desired_order:
            if col not in df_filter_arta.columns:
                df_filter_arta[col] = ''


#Buat Kriteria ARTA 
    def check_criteria(row):
            if row['PRODUK'] == 'PINJAMAN ARTA':
                if 100000 <= row['JML.PINJAMAN'] <= 5000000:
                    return True
                else:
                    return False
            else:
                return False
    
    df_filter_arta['CEK KRITERIA'] = df_filter_arta.apply(check_criteria, axis=1)

    st.write("Anomali ARTA:")
    st.write(df_filter_arta)

#----------------------------------------- PERTANIAN --------------------------------#
    desired_order = [
        'NO.', 'ID', 'ID.PINJAMAN', 'DUMMY', 'NAMA LENGKAP', 'CENTER', 'GROUP', 'PRODUK', 
        'JML.PINJAMAN', 'J.WAKTU', 'NAMA F.O.', 'PINJ.KE', 'TUJUAN PINJAMAN']

    for col in desired_order:
            if col not in df_filter_ptn.columns:
                df_filter_ptn[col] = ''


#Buat Kriteria PTN 
    def check_criteria(row):
            if row['PRODUK'] == 'PINJAMAN PERTANIAN':
                if 500000 <= row['JML.PINJAMAN'] <= 10000000:
                    return True
                else:
                    return False
            else:
                return False

# Buat Kriteria JW
    def check_criteria_jw(row):
            if row['TUJUAN PINJAMAN'] == 'PERTANIAN PADI' and row['J.WAKTU'] == 25:
                    return True
            elif row['TUJUAN PINJAMAN'] == 'PERTANIAN SAYURAN' and row['J.WAKTU'] == 16:
                    return True
            elif row['TUJUAN PINJAMAN'] == 'PERTANIAN PALAWIJA' and row['J.WAKTU'] == 33:
                    return True
            else:
                    return False

    df_filter_ptn['KRITERIA DISBURSE'] = df_filter_ptn.apply(check_criteria, axis=1)
    df_filter_ptn['KRITERIA J.WAKTU'] = df_filter_ptn.apply(check_criteria_jw, axis=1)

    df_filter_ptn['SEMUA KRITERIA TERPENUHI'] = df_filter_ptn['KRITERIA DISBURSE'] & df_filter_ptn['KRITERIA J.WAKTU']

    final_order = desired_order + ['KRITERIA DISBURSE', 'KRITERIA J.WAKTU', 'SEMUA KRITERIA TERPENUHI']
    df_filter_ptn = df_filter_ptn.reindex(columns=final_order)

    st.write("Anomali PTN:")
    st.write(df_filter_ptn)

#---------------------- PRR -----------------------#
    desired_order = [
        'NO.','ID', 'ID.PINJAMAN', 'DUMMY', 'NAMA LENGKAP', 'CENTER', 'GROUP', 'PRODUK', 
        'JML.PINJAMAN', 'J.WAKTU', 'NAMA F.O.'
        ]

    for col in desired_order:
            if col not in df_filter_prr.columns:
                df_filter_prr[col] = ''

#Buat Kriteria Renovasi Rumah 
    def check_criteria(row):
            if row['PRODUK'] == 'PINJAMAN RENOVASI RUMAH':
                if 3000000 <= row['JML.PINJAMAN'] <= 30000000:
                    return True
                else:
                    return False
            else:
                return False
    
    df_filter_prr['CEK KRITERIA'] = df_filter_prr.apply(check_criteria, axis=1)
#---Merge df_S dan PRR
    merge_column = 'DUMMY'
    df_prr_merge = pd.merge(df_filter_prr, df_S, on=merge_column, suffixes=('_df_S','_df_filter_prr'))
    # Sukarela
    df_prr_merge['Pencairan Renovasi Rumah x 25%'] = df_prr_merge['JML.PINJAMAN'] * 0.25
    df_prr_merge['Sukarela Sesuai'] = df_prr_merge.apply(lambda row: row['Db Sukarela'] >= row['Pencairan Renovasi Rumah x 25%'], axis=1)
    # Wajib
    df_prr_merge['Pencairan Renovasi Rumah x 1%'] = df_prr_merge['JML.PINJAMAN'] * 0.01    
    df_prr_merge['Wajib Sesuai'] = df_prr_merge.apply(lambda row: row['Db Wajib'] < row['Pencairan Renovasi Rumah x 1%'], axis=1)
    # Penisun
    df_prr_merge['Pencairan Renovasi Rumah x 1% Pensiun'] = df_prr_merge['JML.PINJAMAN'] * 0.01
    df_prr_merge['Pensiun Sesuai'] = df_prr_merge.apply(lambda row: row['Db Pensiun'] < row['Pencairan Renovasi Rumah x 1% Pensiun'], axis=1)

    desired_order = [
         'NO.', 'ID', 'ID.PINJAMAN', 'NAMA LENGKAP', 'CENTER_df_S', 'GROUP', 'JML.PINJAMAN', 'SL', 'TRANS. DATE', 'CEK KRITERIA', 'Pencairan Renovasi Rumah x 25%', 'Db Sukarela', 'Sukarela Sesuai', 'Pencairan Renovasi Rumah x 1%', 'Db Wajib', 'Wajib Sesuai', 'Pencairan Renovasi Rumah x 1% Pensiun', 'Db Pensiun', 'Pensiun Sesuai' 
    ]
    for col in desired_order:
        if col not in df_prr_merge.columns:
            df_prr_merge[col] = ''
    df_prr_merge = df_prr_merge[desired_order]

    rename_dict = {
         'CENTER_df_S':'CENTER'    
    }
    df_prr_merge = df_prr_merge.rename(columns=rename_dict)

    st.write("Anomali PRR:")
    st.write(df_prr_merge)

#---------------------------------- SANITASI --------------------------------#
    desired_order = [
        'NO.','ID', 'ID.PINJAMAN', 'DUMMY', 'NAMA LENGKAP', 'CENTER', 'GROUP', 'PRODUK', 
        'JML.PINJAMAN', 'J.WAKTU', 'TUJUAN PINJAMAN', 'NAMA F.O.'
        ]

    for col in desired_order:
            if col not in df_filter_psa.columns:
                df_filter_psa[col] = ''

#---Buat Kriteria PSA 
    def check_criteria(row):
            if row['PRODUK'] == 'PINJAMAN SANITASI':
                if 1000000 <= row['JML.PINJAMAN'] <= 30000000:
                    return True
                else:
                    return False
            else:
                return False
    
    df_filter_psa['CEK KRITERIA'] = df_filter_psa.apply(check_criteria, axis=1)

#---Merge df_s dan PSA
    merge_column = 'DUMMY'
    df_psa_merge = pd.merge(df_filter_psa, df_S, on=merge_column, suffixes=('_filter_PSA','_df_S'))

    #Kriteria Nabung Sukarela 25%
    df_psa_merge['Pencairan Sanitasi x 25%'] = df_psa_merge['JML.PINJAMAN'] * 0.25
    #--Kriteria jika tujuan pinjaman "AIR", mengahislkan TRUE
    df_psa_merge['Sukarela Sesuai'] = df_psa_merge.apply(lambda row: 
    True if 'AIR' in str(row['TUJUAN PINJAMAN']).upper() 
    else row['Db Sukarela'] >= row['Pencairan Sanitasi x 25%'], 
    axis=1)

    #Pengecekkan Wajib
    df_psa_merge['Pencairan Sanitasi x 1%'] = df_psa_merge['JML.PINJAMAN'] * 0.01    
    df_psa_merge['Wajib Sesuai'] = df_psa_merge.apply(lambda row: row['Db Wajib'] < row['Pencairan Sanitasi x 1%'], axis=1)

    #Pengecekkan Pensiun
    df_psa_merge['Pencairan Sanitasi x 1% Pensiun'] = df_psa_merge['JML.PINJAMAN'] * 0.01
    df_psa_merge['Pensiun Sesuai'] = df_psa_merge.apply(lambda row: row['Db Pensiun'] < row['Pencairan Sanitasi x 1% Pensiun'], axis=1)

    desired_order = [
         'NO.', 'ID', 'ID.PINJAMAN', 'NAMA LENGKAP', 'CENTER_df_S', 'GROUP', 'JML.PINJAMAN', 'SL','TUJUAN PINJAMAN', 'TRANS. DATE', 'CEK KRITERIA', 'Pencairan Sanitasi x 25%', 'Db Sukarela', 'Sukarela Sesuai', 'Pencairan Sanitasi x 1%', 'Db Wajib', 'Wajib Sesuai', 'Pencairan Sanitasi x 1% Pensiun', 'Db Pensiun', 'Pensiun Sesuai' 
    ]
    for col in desired_order:
        if col not in df_psa_merge.columns:
            df_psa_merge[col] = ''
    df_psa_merge = df_psa_merge[desired_order]

    rename_dict = {
         'CENTER_df_S':'CENTER'    
    }
    df_psa_merge = df_psa_merge.rename(columns=rename_dict)

    st.write("Anomali PSA:")
    st.write(df_psa_merge)

#---------- Download links for all files
    for name, df in {
            'Anomali PU.xlsx': df_filter_pu,
            'Anomali PMB.xlsx': df_filter_pmb,
            'Anomali DTP.xlsx': df_filter_ppd,
            'Anomali PSA.xlsx': df_psa_merge,
            'Anomali ARTA.xlsx': df_filter_arta,
            'Anomali PRR.xlsx': df_prr_merge,
            'Anomali PTN.xlsx' : df_filter_ptn
        }.items():
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        buffer.seek(0)
        st.download_button(
            label=f"Unduh {name}",
            data=buffer.getvalue(),
            file_name=name,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

else:
    st.warning("Silakan upload file 'Pinjaman Detail Report.xlsx' dan 'pivot_simpanan.xlsx'")
