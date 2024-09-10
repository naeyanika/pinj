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
