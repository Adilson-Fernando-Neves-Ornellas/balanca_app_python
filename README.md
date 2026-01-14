🧾 Balança App

Aplicação desenvolvida em Python + Flask para leitura de peso de balanças seriais (USB / RS232) e disponibilização das informações através de uma API HTTP.

Ideal para rodar em Raspberry Pi ou PC (Windows / Linux), permitindo que outros sistemas como Web, ERP, PDV ou automações consumam o peso da balança pela rede local.

🚀 Funcionalidades

🔌 Detecção automática da porta serial da balança

⚖️ Leitura dos dados enviados pela balança via comunicação serial

🌐 API REST simples e leve usando Flask

🔓 CORS habilitado (acesso permitido por qualquer frontend)

🧠 Compatível com Raspberry Pi, Windows e Linux

📡 Acesso via rede local (LAN)

🛠️ Tecnologias Utilizadas

Python 3.8+

Flask

Flask-CORS

PySerial

📦 Requisitos
Sistema Operacional

Raspberry Pi OS

Linux

Windows

Software

Python 3 instalado (caso utilize a versão em Python)

Hardware

Balança com saída serial RS232

Cabo RS232 → USB

Cabo Null Modem (troca os pinos 2 ↔ 3)

🔌 ⚠️ ATENÇÃO: TIPO DE CABO SERIAL (MUITO IMPORTANTE)

⚠️ Este ponto é essencial para o funcionamento da aplicação.

A maioria das balanças utiliza comunicação RS232, onde os sinais de TX e RX são invertidos em relação ao computador.

👉 Por isso, é obrigatório utilizar um cabo que faça a troca dos pinos 2 e 3 (TX ↔ RX), também conhecido como:

Cabo Null Modem

Cabo serial com TX/RX cruzado

Adaptador DB9 com pinos 2 e 3 invertidos

📌 Fluxo correto de conexão
Balança

   ↓
   
Cabo que troca os pinos 2 ↔ 3 (Null Modem)

   ↓
   
Cabo RS232 → USB (cabo comprado)

   ↓
   
Computador ou Raspberry Pi


📎 Importante:
O cabo RS232 → USB, por si só, normalmente NÃO faz a troca dos pinos.
Sem o cabo null modem, a porta é detectada, mas nenhum dado é recebido.

❌ Sintomas de cabo incorreto

Porta serial aparece (/dev/ttyUSB0, COM3, etc)

Endpoint /status funciona normalmente

Endpoint /peso sempre retorna erro

Nenhum dado aparece nos testes de leitura serial

✅ Soluções recomendadas

Utilizar um cabo Null Modem entre a balança e o adaptador

Utilizar um adaptador RS232 → USB que já informe TX/RX cruzado

Utilizar um adaptador DB9 Fêmea–Fêmea cruzado

⚠️ Nem todo adaptador USB–RS232 faz essa troca automaticamente.
Sempre verifique a descrição técnica do produto.

📥 Instalação
▶️ Windows (Executável)

Dentro da pasta dist existe um arquivo .exe que pode ser baixado e executado diretamente no Windows, sem necessidade de instalar Python.

Basta executar o arquivo para iniciar a aplicação.

▶️ Execução

Ao iniciar a aplicação, a seguinte mensagem será exibida no console:

🚀 Balança App iniciado
🌐 Servidor em http://0.0.0.0:3333

🌐 Endpoints da API
🔍 Status da aplicação
GET /status

Resposta:
{
  "success": true,
  "app": "Balanca App Raspberry",
  "porta": "/dev/ttyUSB0"
}

⚖️ Ler peso da balança
GET /peso

Resposta (erro):
{
  "success": false,
  "message": "Não foi possível ler a balança"
}


⚠️ Observação:
Atualmente o endpoint retorna os dados brutos enviados pela balança.
O parser pode ser ajustado conforme o protocolo do fabricante, para retornar apenas o valor do peso.

🔌 Porta Serial

A aplicação detecta automaticamente a primeira porta serial disponível no sistema.

Exemplos comuns:

Linux / Raspberry Pi:
/dev/ttyUSB0, /dev/ttyACM0

Windows:
COM3, COM4

🔧 Configurações Iniciais

No início do arquivo balanca_app.py:

BAUDRATE = 9600
TIMEOUT = 1


Esses valores devem ser ajustados conforme o manual da balança utilizada.
