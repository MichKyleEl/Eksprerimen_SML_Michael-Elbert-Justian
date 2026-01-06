
def muat_data(path):
    """Memuat data dari file CSV"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} tidak ditemukan.")
    df = pd.read_csv(path)
    print(f"Data dimuat dari {path}. Ukuran: {df.shape}")
    return df

def preprocessing_otomatis(df):
    """
    Melakukan cleaning dan scaling sesuai eksperimen:
    1. Imputasi Missing Values berdasarkan rata-rata kelas (Potability)
    2. Hapus Duplikat
    3. Scaling Standar
    """
    df_clean = df.copy()
    
    # 1. Handling Missing Values (Group Mean Imputation)
    kolom_missing = ['ph', 'Sulfate', 'Trihalomethanes']
    for kolom in kolom_missing:
        if kolom in df_clean.columns:
            df_clean[kolom] = df_clean[kolom].fillna(
                df_clean.groupby('Potability')[kolom].transform('mean')
            )
    
    # 2. Hapus Duplikat
    df_clean.drop_duplicates(inplace=True)
    
    # 3. Scaling
    # Pisahkan target
    target_col = 'Potability'
    X = df_clean.drop(target_col, axis=1)
    y = df_clean[target_col]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Gabungkan kembali
    df_result = pd.DataFrame(X_scaled, columns=X.columns)
    df_result[target_col] = y.reset_index(drop=True)
    
    print("Preprocessing selesai. Data siap digunakan.")
    return df_result

if __name__ == "__main__":
    # Ganti path ini sesuai lokasi file asli Anda nanti
    input_path = "water_potability.csv" 
    output_path = "water_potability_clean_auto.csv"
    
    try:
        df_raw = muat_data(input_path)
        df_clean = preprocessing_otomatis(df_raw)
        df_clean.to_csv(output_path, index=False)
        print(f"File hasil disimpan di: {output_path}")
    except Exception as e:
        print(f"Terjadi error: {e}")
