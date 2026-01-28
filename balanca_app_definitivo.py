from flask import Flask, jsonify
from flask_cors import CORS
import serial
import serial.tools.list_ports
import re
import time
import sys
import threading
import requests

# =========================
# CONFIGURAÇÕES
# =========================
BAUDRATE = 9600
TIMEOUT = 1
porta_detectada = None

API_URL = "https://admin.timeclean.hml.hotztec.com/api/balanca/um"  # <<< SUA API
INTERVALO_LEITURA = 0.5  # segundos
VARIACAO_MINIMA = 0.001  # evita ruído
peso_atual = None
ultimo_peso_enviado = None

# =========================
# FLASK
# =========================
app = Flask(__name__)
CORS(app)


# =========================
# SERIAL
# =========================
def detectar_porta_balanca():
    global porta_detectada

    if porta_detectada:
        return porta_detectada

    portas = list(serial.tools.list_ports.comports())

    for porta in portas:
        if porta.device.startswith("/dev/ttyUSB"):
            porta_detectada = porta.device
            print(f"✅ Porta da balança detectada: {porta_detectada}")
            return porta_detectada

    print("❌ Nenhuma balança USB detectada")
    return None

def ler_peso_balanca():
    porta = detectar_porta_balanca()

    if not porta:
        return None

    try:
        ser = serial.Serial(
            port=porta,
            baudrate=BAUDRATE,
            timeout=0.5
        )

        time.sleep(0.5)

        dados = ser.read(ser.in_waiting or 100)
        ser.close()

        texto = dados.decode('latin-1', errors='ignore')

        # Exemplo recebido:
        # "= 001.000= 001.000= 001.000"
        # Vamos extrair TODOS os números
        pesos = re.findall(r'(\d+\.\d+)', texto)

        if not pesos:
            return None

    # Usa o último valor (mais recente)
        peso = float(pesos[-1])
        return round(peso, 3)

    except Exception as e:
        return None

def enviar_peso_api(peso):
    try:
        payload = {
            "peso": peso,
            "timestamp": int(time.time())
        }

        requests.post(API_URL, json=payload, timeout=2)
        print(f"📡 Peso enviado para API: {peso}")

    except Exception as e:
        print("❌ Erro ao enviar para API:", e)

def monitorar_balanca():
    global peso_atual, ultimo_peso_enviado

    while True:
        peso = ler_peso_balanca()

        if peso is not None:
            peso_atual = peso

            if (
                ultimo_peso_enviado is None or
                abs(peso - ultimo_peso_enviado) >= VARIACAO_MINIMA
            ):
                enviar_peso_api(peso)
                ultimo_peso_enviado = peso

        time.sleep(INTERVALO_LEITURA)

# =========================
# ROTAS
# =========================
@app.route('/peso')
def peso():
    global peso_atual

    if peso_atual is None:
        return jsonify({
            'success': False,
            'message': 'Não foi possível ler a balança'
        })

    return jsonify({
        'success': True,
        'peso': peso_atual
    })

@app.route('/status')
def status():
    porta = detectar_porta_balanca()

    return jsonify({
        'success': True,
        'app': 'Balanca App Raspberry',
        'porta': porta if porta else 'não detectada'
    })
    
@app.after_request
def cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

# =========================
# MAIN
# =========================
if __name__ == '__main__':
    print("🚀 Balanca App iniciado no Raspberry Pi")
    print("🌐 Servidor em http://0.0.0.0:3333")

    # Thread da balança
    t = threading.Thread(target=monitorar_balanca, daemon=True)
    t.start()

    try:
        app.run(
            host='0.0.0.0',
            port=3333,
            debug=False,
            use_reloader=False
        )
    except Exception as e:
        print("❌ Erro crítico:", e)
        sys.exit(1)