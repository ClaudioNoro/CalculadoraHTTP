from flask import Flask, request, jsonify
import socket
import threading
import os

app = Flask(__name__)

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.get_json()
    if not data:
        error_message = 'Nenhum dado enviado'
        print("Erro:", error_message)
        return jsonify({'error': error_message}), 400

    num1 = data.get('num1')
    num2 = data.get('num2')
    operacao = data.get('operacao')

    if num1 is None or num2 is None or operacao is None:
        error_message = 'Os campos num1, num2 e operacao são obrigatórios.'
        print("Erro:", error_message)
        return jsonify({'error': error_message}), 400

    try:
        num1 = float(num1)
        num2 = float(num2)
    except ValueError:
        error_message = 'num1 e num2 devem ser números.'
        print("Erro:", error_message)
        return jsonify({'error': error_message}), 400

    if operacao == 'soma':
        resultado = num1 + num2
    elif operacao == 'subtracao':
        resultado = num1 - num2
    elif operacao == 'multiplicacao':
        resultado = num1 * num2
    elif operacao == 'divisao':
        if num2 == 0:
            error_message = 'Divisão por zero não é permitida.'
            print("Erro:", error_message)
            return jsonify({'error': error_message}), 400
        resultado = num1 / num2
    else:
        error_message = 'Operação inválida. Utilize: soma, subtracao, multiplicacao ou divisao.'
        print("Erro:", error_message)
        return jsonify({'error': error_message}), 400

    # Exibe o resultado no terminal
    print(f"Operação: {operacao} | {num1} e {num2} = {resultado}")
    return jsonify({'resultado': resultado})

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    ip = get_local_ip()
    rota = f"http://{ip}:5000/calcular"
    print("Acesse a API em:", rota)
    
    # Inicia o servidor Flask em uma thread separada
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Loop infinito para manter a aplicação ativa
    while True:
        print("Pressione 0 para encerrar a aplicação.")
        opcao = input("Sua opção: ").strip()
        if opcao == '0':
            print("Encerrando a aplicação...")
            os._exit(0)
