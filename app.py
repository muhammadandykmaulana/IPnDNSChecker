from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# TODO: Masukkan API Key kamu di sini
ABUSEIPDB_API_KEY = '3c706ee818139708e23539d37b9a0e2002c5aa11a84c886390737fe02be68609657684b907b8aaf1'
VIRUSTOTAL_API_KEY = '85f8e268895acd6d99a328741f4ac9045bb2f44d9cdd5a6b5cdc3c2c2581fc7d'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        target = request.form.get('target_input')
        search_type = request.form.get('search_type') # 'ip' atau 'domain'

        try:
            if search_type == 'ip':
                # --- LOGIC UNTUK ABUSEIPDB (IP) ---
                url = 'https://api.abuseipdb.com/api/v2/check'
                querystring = {'ipAddress': target, 'maxAgeInDays': '90', 'verbose': 'true'}
                headers = {'Accept': 'application/json', 'Key': ABUSEIPDB_API_KEY}
                
                response = requests.get(url, headers=headers, params=querystring)
                response.raise_for_status()
                data = response.json()
                
                return render_template('result.html', search_type='ip', data=data['data'], target=target)

            elif search_type == 'domain':
                # --- LOGIC UNTUK VIRUSTOTAL (DOMAIN) ---
                url = f"https://www.virustotal.com/api/v3/domains/{target}"
                headers = {"x-apikey": VIRUSTOTAL_API_KEY}
                
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                vt_data = response.json()
                
                return render_template('result.html', search_type='domain', data=vt_data['data']['attributes'], target=target)

        except requests.exceptions.HTTPError as err:
            # Menangkap error jika IP/Domain tidak valid atau API Key salah
            return render_template('index.html', error=f"Terjadi kesalahan API: {err}")
        except Exception as e:
            return render_template('index.html', error="Gagal mengambil data. Pastikan format IP/Domain benar.")

    # Jika GET request, tampilkan form awal
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)