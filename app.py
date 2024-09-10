desired_order = [
    'NO.', 'ID', 'ID.PINJAMAN', 'DUMMY', 'NAMA LENGKAP', 'CENTER', 'GROUP', 'PRODUK', 'JML.PINJAMAN','J.WAKTU', 'NAMA F.O.', 'PINJ.KE', 'J.WAKTU', 'TUJUAN PINJAMAN'
    ]

for col in desired_order:
    if col not in df_filter_ptn.columns:
        df_filter_ptn[col] = ''

df_filter_ptn = df_filter_ptn[desired_order]

#Buat Kriteria Pertanian 
def check_pertanian_criteria(row):
    if 500000 <= row['JML.PINJAMAN'] <= 10000000:
        if row['TUJUAN PINJAMAN'] == 'PERTANIAN PADI' and row['J.WAKTU'] == 25:
            return True
        elif row['TUJUAN PINJAMAN'] == 'PERTANIAN SAYURAN' and row['J.WAKTU'] == 16:
            return True
        elif row['TUJUAN PINJAMAN'] == 'PERTANIAN PALAWIJA' and row['J.WAKTU'] == 33:
            return True
        else:
            return False
    else:
        return False

df_filter_ptn['CEK KRITERIA'] = df_filter_ptn.apply(check_pertanian_criteria, axis=1)

st.write("Anomali PTN:")
st.write(df_filter_ptn)
