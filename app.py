from flask import Flask, request, jsonify  # Importa Flask para criar a aplicação web e request/jsonify para tratar requisições e respostas JSON
import socket  # Importa o módulo socket para operações de rede, como obter o IP local
import threading  # Importa o módulo threading para executar tarefas simultaneamente (rodar o Flask em uma thread separada)
import os  # Importa o módulo os para interagir com o sistema operacional (usado para encerrar o programa)

app = Flask(__name__)  # Cria uma instância da aplicação Flask utilizando o nome do módulo atual

# Define uma rota '/calcular' que aceita requisições HTTP POST
@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.get_json()  # Obtém o corpo da requisição no formato JSON
    if not data:  # Verifica se nenhum dado foi enviado
        error_message = 'Nenhum dado enviado'  # Define mensagem de erro
        print("Erro:", error_message)  # Imprime o erro no terminal
        return jsonify({'error': error_message}), 400  # Retorna uma resposta JSON com o erro e status 400 (Bad Request)

    num1 = data.get('num1')  # Extrai o valor associado à chave 'num1' do JSON
    num2 = data.get('num2')  # Extrai o valor associado à chave 'num2' do JSON
    operacao = data.get('operacao')  # Extrai o valor associado à chave 'operacao' do JSON

    # Verifica se os campos obrigatórios foram enviados
    if num1 is None or num2 is None or operacao is None:
        error_message = 'Os campos num1, num2 e operacao sao obrigatorios.'
        print("Erro:", error_message)  # Imprime o erro no terminal
        return jsonify({'error': error_message}), 400  # Retorna uma resposta JSON com o erro e status 400

    try:
        num1 = float(num1)  # Converte o valor de num1 para float
        num2 = float(num2)  # Converte o valor de num2 para float
    except ValueError:  # Trata a exceção caso a conversão falhe (valores não numéricos)
        error_message = 'num1 e num2 devem ser números.'
        print("Erro:", error_message)  # Imprime o erro no terminal
        return jsonify({'error': error_message}), 400  # Retorna uma resposta JSON com o erro e status 400

    # Executa a operação matemática conforme o valor de 'operacao'
    if operacao == 'soma':
        resultado = num1 + num2  # Realiza a soma dos dois números
    elif operacao == 'subtracao':
        resultado = num1 - num2  # Realiza a subtração dos dois números
    elif operacao == 'multiplicacao':
        resultado = num1 * num2  # Realiza a multiplicação dos dois números
    elif operacao == 'divisao':
        if num2 == 0:  # Verifica se a divisão por zero está sendo solicitada
            error_message = 'Divisão por zero não é permitida.'
            print("Erro:", error_message)  # Imprime o erro no terminal
            return jsonify({'error': error_message}), 400  # Retorna uma resposta JSON com o erro e status 400
        resultado = num1 / num2  # Realiza a divisão dos dois números
    else:
        error_message = 'Operação inválida. Utilize: soma, subtracao, multiplicacao ou divisao.'
        print("Erro:", error_message)  # Imprime o erro no terminal
        return jsonify({'error': error_message}), 400  # Retorna uma resposta JSON com o erro e status 400

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
        print("Pressione 0 para encerrar a aplicação.")  # Informa ao usuário como encerrar a aplicação
        opcao = input("Sua opção: ").strip()  # Lê a opção digitada pelo usuário, removendo espaços em branco
        if opcao == '0':  # Se a opção for '0', o programa será encerrado
            print("Encerrando a aplicação...")  # Imprime mensagem de encerramento no terminal
            os._exit(0)  # Encerra imediatamente o processo, finalizando todas as threads
