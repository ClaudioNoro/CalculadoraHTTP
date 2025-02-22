from flask import Flask, request, jsonify  # Importa Flask para criar a aplicação web e request/jsonify para tratar requisições e respostas JSON
import socket  # Importa o módulo socket para operações de rede, como obter o IP local
import threading  # Importa o módulo threading para executar tarefas simultaneamente (rodar o Flask em uma thread separada)
import os  # Importa o módulo os para interagir com o sistema operacional (usado para encerrar o programa)

app = Flask(__name__)  # Cria uma instância da aplicação Flask utilizando o nome do módulo atual

# Define uma rota '/calcular' que aceita requisições HTTP POST
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

    # Utilizando o match-case para selecionar a operação
    match operacao:
        case 'soma':
            resultado = num1 + num2  # Realiza a soma dos dois números
        case 'subtracao':
            resultado = num1 - num2  # Realiza a subtração dos dois números
        case 'multiplicacao':
            resultado = num1 * num2  # Realiza a multiplicação dos dois números
        case 'divisao':
            if num2 == 0:  # Verifica se a divisão por zero está sendo solicitada
                error_message = 'Divisao por zero nao exite num intervalo real.'
                print("Erro:", error_message)
                return jsonify({'error': error_message}), 400
            resultado = num1 / num2  # Realiza a divisão dos dois números
        case _:
            error_message = 'Operacao invalida. Utilize: soma, subtracao, multiplicacao ou divisao.'
            print("Erro:", error_message)
            return jsonify({'error': error_message}), 400

    # Exibe o resultado da operação no terminal para monitoramento
    print(f"Operação: {operacao} | {num1} e {num2} = {resultado}")
    return jsonify({'resultado': resultado})  # Retorna uma resposta JSON contendo o resultado da operação


# Função para obter o IP local da máquina
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Cria um socket UDP
    try:
        s.connect(('10.255.255.255', 1))  # Tenta se conectar a um IP arbitrário para determinar o IP local
        ip = s.getsockname()[0]  # Obtém o IP local utilizado para a conexão
    except Exception:
        ip = '127.0.0.1'  # Se houver erro, define o IP como localhost
    finally:
        s.close()  # Fecha o socket para liberar recursos
    return ip  # Retorna o IP local

# Função que inicia o servidor Flask
def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)  # Inicia o Flask para escutar em todas as interfaces na porta 5000

# Bloco principal que é executado quando o script é iniciado diretamente
if __name__ == '__main__':
    ip = get_local_ip()  # Chama a função para obter o IP local da máquina
    rota = f"http://{ip}:5000/calcular"  # Define a rota completa para acessar a API
    print("Acesse a API em:", rota)  # Imprime no terminal a URL para acesso à API
    
    # Inicia o servidor Flask em uma thread separada para que o programa principal continue rodando
    flask_thread = threading.Thread(target=run_flask)  # Cria uma thread que executará a função run_flask
    flask_thread.daemon = True  # Define a thread como daemon, permitindo que ela seja finalizada automaticamente ao encerrar o programa
    flask_thread.start()  # Inicia a thread do servidor Flask

    # Loop infinito para manter o programa ativo e permitir a entrada do usuário para encerramento
    while True:
        print("Pressione 0 para encerrar a aplicacao.")  # Informa ao usuário como encerrar a aplicação
        opcao = input("Sua opcao: ").strip()  # Lê a opção digitada pelo usuário, removendo espaços em branco
        if opcao == '0':  # Se a opção for '0', o programa será encerrado
            print("Encerrando a aplicacao...")  # Imprime mensagem de encerramento no terminal
            os._exit(0)  # Encerra imediatamente o processo, finalizando todas as threads
