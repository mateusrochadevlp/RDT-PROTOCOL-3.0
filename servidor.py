# Funções que permitem o envio e recebimento de dados (cria a conexão cliente-servidor)
import socket

# data.encode (transforma cada letra do texto em um número)
# sum (faz a soma desses números)
# %256 (retorna o resto da divisão, garantindo que o valor final não ultrapasse 255)
# exemplo: "ABC" -- 65 + 66 + 67 = 198 -- (198 % 256 = 198)
def checksum (data):
    return sum(data.encode()) % 256

def start_server():
    # Criando canal de comunicação (AF_INET = IPV4) (SOCK_DGRAM = UDP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Vincula o endereço e porta com o canal de comunicação (socket)
    server_socket.bind(('', 12345)) #porta igual ou abaixo de 1024 é reservado para o sistema

    seq_esperada = 0

    print("\nSERVIDOR RDT 3.0 INICIADO")
    print("Aguardando envio de pacotes...\n")

    # o loop mantém o servidor ligado
    while True: 
        # pacote = '0|198|ABC'
        # addr = ('127.0.0.1', 12345)
        pacote, addr = server_socket.recvfrom(1024)
        pacote_texto = pacote.decode()

        # tratamento de exeções
        try:
            # split corta a string onde encontra | e distribui as partes entre as váriaveis
            seq_str, checksum_str, dado = pacote_texto.split('|',2)
            # tranformando alguns dados em tipo INT
            seq_enviada = int(seq_str)
            checksum_recebido = int(checksum_str)
            checksum_calculado = checksum(dado)

            print(f"Pacote {seq_enviada} recebido!")

            # Verifica se dados foram corrompidos (atráves do checksum)
            if checksum_calculado != checksum_recebido:
                print(f"--> CORRUPÇÃO DETECTADA! (checksum esperado: {checksum_recebido}, obtido: {checksum_calculado})")
                print("-->Ignorando pacote (Aguardando timeout do emissor).")
                continue
            
            # Verifica se o pacote foi enviado mais de uma vez
            if seq_enviada != seq_esperada:
                print(f"--> PACOTE DUPLICADO! (pacote esperado: {seq_esperada}, recebido: {seq_enviada})")
                ack = f"{seq_enviada}|ACK"
                server_socket.sendto(ack.encode(), addr)
                print(f"--> RETORNANDO ACK RECEBIDO: {seq_enviada}, sincronizando...")
            
            # Se tudo der certo
            else:
                print(f"--> DADOS RECEBIDOS: {dado}")
                ack = f"{seq_enviada}|ACK"
                server_socket.sendto(ack.encode(), addr)
                print(f"--> RETORNANDO ACK RECEBIDO: {seq_enviada}, sincronizando...")

                # alterna a sequência esperada entre 0 e 1
                seq_esperada = 1 - seq_esperada

        # caso ocorra algum envio incorreto dos dados
        except ValueError:
            print("Formato de pacote inválido.")

# Se estiver sendo importado uma função específica por outro arquivo, ele não inicia o servidor sem querer.
if __name__ == "__main__":
    start_server()
