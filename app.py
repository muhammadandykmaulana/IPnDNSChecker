from flask import Flask, render_template, request
import requests
import json # Di-import untuk fitur debug print JSON

# [SOAL 3c] Struktur project Flask disusun dengan baik
app = Flask(__name__)

# [SOAL 1a] Pilih 1 Public API yang relevan (Disini memakai 2: AbuseIPDB & VirusTotal)
# Masukkan API Key di sini
ABUSEIPDB_API_KEY = '3c706ee818139708e23539d37b9a0e2002c5aa11a84c886390737fe02be68609657684b907b8aaf1'
VIRUSTOTAL_API_KEY = '85f8e268895acd6d99a328741f4ac9045bb2f44d9cdd5a6b5cdc3c2c2581fc7d'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # [PERBAIKAN] Menyesuaikan nama "name" dengan form di index.html
        target = request.form.get('target')
        search_type = request.form.get('target_type') # 'ip' atau 'domain'

        try:
            # [SOAL 3b] Fitur Pengolahan Data: Pencarian sederhana berdasarkan Tipe
            if search_type == 'ip':
                # --- LOGIC UNTUK ABUSEIPDB (IP) ---
                # [SOAL 1b & 3a] Request data API menggunakan requests
                url = 'https://api.abuseipdb.com/api/v2/check'
                querystring = {'ipAddress': target, 'maxAgeInDays': '90', 'verbose': 'true'}
                headers = {'Accept': 'application/json', 'Key': ABUSEIPDB_API_KEY}
                
                response = requests.get(url, headers=headers, params=querystring)
                response.raise_for_status()
                
                # [SOAL 3a] Parsing data JSON
                data = response.json()
                
                # ==== DEBUGGING JSON ABUSEIPDB ====
                print("=== DEBUG JSON ABUSEIPDB ===")
                print(json.dumps(data, indent=4))
                # ==================================

                # [SOAL 1b] Ambil minimal 10 data (reports mengembalikan puluhan histori)
                if 'data' in data and 'reports' in data['data']:
                    # [SOAL 3b] Fitur Pengolahan Data (Sorting): 
                    # Mengurutkan data laporan IP berdasarkan tingkat kepercayaan (confidence score) tertinggi ke terendah
                    reports = data['data']['reports']
                    sorted_reports = sorted(reports, key=lambda x: x.get('abuseConfidenceScore', 0), reverse=True)
                    data['data']['reports'] = sorted_reports
                
                # [SOAL 3a] Pengiriman data dari Flask ke template HTML
                # [PERBAIKAN] Menggunakan result.html agar sesuai dengan file lokal
                return render_template('result.html', result_type='ip', data=data['data'], target=target)

            elif search_type == 'domain':
                # --- LOGIC UNTUK VIRUSTOTAL (DOMAIN) ---
                url = f"https://www.virustotal.com/api/v3/domains/{target}"
                headers = {"x-apikey": VIRUSTOTAL_API_KEY}
                
                # [SOAL 1b & 3a] Request data API menggunakan requests
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                
                # [SOAL 3a] Parsing data JSON
                vt_data = response.json()
                
                # ==== DEBUGGING JSON VIRUSTOTAL ====
                # Hapus tanda '#' pada 2 baris di bawah ini untuk melihat struktur JSON di terminal
                print("=== DEBUG JSON VIRUSTOTAL ===")
                print(json.dumps(vt_data, indent=4))
                # ==================================

                # [SOAL 3b] Fitur Pengolahan Data (Sorting): 
                # Memisahkan engine dengan kategori 'malicious/suspicious' agar berada di urutan atas list
                stats = {}
                sorted_engines = []
                
                if 'data' in vt_data and 'attributes' in vt_data['data']:
                    attributes = vt_data['data']['attributes']
                    stats = attributes.get('last_analysis_stats', {})
                    results = attributes.get('last_analysis_results', {})
                    
                    malicious_engines = []
                    safe_engines = []
                    
                    for engine_name, result_data in results.items():
                        # Membentuk dictionary format baru agar sesuai dengan for loop di result.html
                        engine_info = {
                            'engine_name': engine_name,
                            'category': result_data.get('category', 'undetected'),
                            'result': result_data.get('result', '')
                        }
                        
                        if engine_info['category'] in ['malicious', 'suspicious']:
                            malicious_engines.append(engine_info)
                        else:
                            safe_engines.append(engine_info)
                            
                    # Gabungkan (Bahaya di atas, Aman di bawah)
                    sorted_engines = malicious_engines + safe_engines

                # [SOAL 3a] Pengiriman data dari Flask ke template HTML
                # [PERBAIKAN] Menggunakan result.html
                return render_template('result.html', result_type='domain', stats=stats, sorted_engines=sorted_engines, target=target)

        except requests.exceptions.HTTPError as err:
            # Menangkap error jika IP/Domain tidak valid atau API Key salah
            return render_template('index.html', error=f"Terjadi kesalahan API: {err}")
        except Exception as e:
            # [PERBAIKAN] Pesan error dibuat lebih informatif jika ada template yang hilang
            error_str = str(e)
            if "html" in error_str:
                return render_template('index.html', error=f"Error Template: File '{error_str}' tidak ditemukan di folder 'templates'. Pastikan nama file sudah benar.")
            
            return render_template('index.html', error=f"Gagal mengambil data. Pastikan format IP/Domain benar. (Detail: {error_str})")

    # Jika GET request, tampilkan form awal
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)