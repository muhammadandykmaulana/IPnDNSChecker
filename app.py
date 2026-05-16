from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# TODO: Ganti dengan API Key dari akun AbuseIPDB kamu
API_KEY = '3c706ee818139708e23539d37b9a0e2002c5aa11a84c886390737fe02be68609657684b907b8aaf1'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ip_address = request.form.get('ip_address')

        # Endpoint API AbuseIPDB
        url = 'https://api.abuseipdb.com/api/v2/check'
        
        # Parameter API: verbose=true agar kita dapat list laporan untuk di-looping di HTML
        querystring = {
            'ipAddress': ip_address,
            'maxAgeInDays': '90',
            'verbose': 'true' 
        }
        headers = {
            'Accept': 'application/json',
            'Key': API_KEY
        }

        try:
            # Syarat Tugas: Menggunakan library requests
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status() 
            data = response.json()
            
            # Mengirim data ke file HTML template Flask
            return render_template('result.html', data=data['data'])
            
        except Exception as e:
            error_msg = "Gagal mengambil data dari API atau IP tidak valid."
            return render_template('index.html', error=error_msg)

    # Menampilkan halaman form awal jika request adalah GET
    return render_template('index.html')

if __name__ == '__main__':
    # Berjalan di port 5000 untuk Codespace
    app.run(debug=True, host='0.0.0.0', port=5000)