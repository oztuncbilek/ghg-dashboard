import os

# Kök dizinini bul (EUCentralBank/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Dosya yollarını oluştur
file1 = os.path.join(BASE_DIR, 'data', 'EDGAR_2024_GHG_booklet_2024.xlsx')
file3 = os.path.join(BASE_DIR, 'data', 'CLASS.xlsx')

