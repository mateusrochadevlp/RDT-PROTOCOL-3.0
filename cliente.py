# Funções que permitem o envio e recebimento de dados (cria a conexão cliente-servidor)
import socket

# data.encode (transforma cada letra do texto em um número)
# sum (faz a soma desses números)
# %256 (retorna o resto da divisão, garantindo que o valor final não ultrapasse 255)
# exemplo: "ABC" -- 65 + 66 + 67 = 198 -- (198 % 256 = 198)
def calc_checksum(data):
    return sum(data.encode()) % 256

# criando um pacote
# seq = 0 ou 1
# corrupt para simular erro de checksum
def pacote(seq, dado, corrupt=False):
    checksum = calc_checksum(dado)
    if corrupt:
        checksum = (checksum + 1) % 256
    return f"{seq}|{checksum}|{dado}"

def start_cliente():
    # Criando canal de comunicação (AF_INET = IPV4) (SOCK_DGRAM = UDP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = ('127.0.0.1', 12345)
    client_socket.setblocking(False) # garante que o programa não vai ficar preso no "recvfrom" caso nenhum pacote chegue

    seq_pacote = 0

    while True:
        print(f"\nAguardando para enviar pacote {seq_pacote}")
        print("Escolha o comportamento de envio do pacote:\n")
        print("1 - Envio Normal\n2 - Corromper Dados (Checksum errado)\n3 - Atrasar Pacote (Timeout)\n4 - Encerrar conexão")

        opcao = input("\nInsira sua escolha --> ")
        
        corrupt = (opcao == "2")
        delay = (opcao == "3")

        if delay:
            print("\nSimulando atraso...")
            client_socket.settimeout(3.0)
            try:
                ack = client_socket.recvfrom(1024)
                print(f"Ack recebido: {ack}")
            except socket.timeout as erro:
                print(f"\n[TIMEOUT] O tempo esgotou, reiniciando conexão...")

        elif opcao == "4":
            print("Encerrando conexão...")
            break
            
        else:
            dado = input("Insira uma mensagem: ")
            pkt = pacote(seq_pacote, dado, corrupt)
            client_socket.sendto(pkt.encode(), addr)

            client_socket.settimeout(3.0)
            try:
                ack, addr = client_socket.recvfrom(1024)
                ack_str = ack.decode()
                ack_seq, msg = ack_str.split('|')
                ack_seq = int(ack_seq)
                    
                if msg == "ACK" and ack_seq == seq_pacote:
                    print(f"[SUCESSO] ACK do pacote: {ack_seq} recebido!")
                    seq_pacote = 1 - seq_pacote # Alterna 0 e 1
                else:
                    print(f"[AVISO] ACK incorreto ou corrompido. Ignorando...")
            except:
                print("[ERRO] Falha ao processar ACK.")

if __name__ == "__main__":
    start_cliente()