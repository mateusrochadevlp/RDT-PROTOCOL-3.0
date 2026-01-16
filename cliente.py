# Funções que permitem o envio e recebimento de dados (cria a conexão cliente-servidor)
import socket
# funções que cuidam do timeout e espera
import time

import select

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

def enviar(dado_lista):
    # Criando canal de comunicação (AF_INET = IPV4) (SOCK_DGRAM = UDP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = ('127.0.0.1', 12345)
    client_socket.setblocking(False) # garante que o programa não vai ficar preso no "recvfrom" caso nenhum pacote chegue

    seq_pacote = 0
    timeout_tempo = 3.0

    # percorre a lista com as mensagens que irão ser enviadas
    for dado in dado_lista:
        ack_recebimento = False

        while not ack_recebimento:
            print(f"\nAguardando para enviar pacote {seq_pacote}")
            print("Escolha o comportamento de envio do pacote:\n")
            print("1 - Envio Normal\n2 - Corromper Dados (Checksum errado)\n3 - Atrasar Pacote (Timeout)")

            opcao = input("Insira sua escolha --> ")
            corrupt = (opcao == "2")
            delay = (opcao == "3")

            if delay:
                print(f"Simulando atraso... Esperando timeout")

            else:
                pkt = pacote(seq_pacote, dado, corrupt)
                client_socket.sendto(pkt.encode(), addr)
            
            ready = select.select([client_socket], [], [], timeout_tempo)

            if ready[0]:
                # Recebeu algo antes do timeout
                ack_data, _ = client_socket.recvfrom(1024)
                ack_str = ack_data.decode()
                
                try:
                    ack_seq, msg = ack_str.split('|')
                    ack_seq = int(ack_seq)
                    
                    if msg == "ACK" and ack_seq == seq_pacote:
                        print(f"[SUCESSO] ACK {ack_seq} recebido!")
                        ack_recebimento = True
                        seq_pacote = 1 - seq_pacote # Alterna 0 e 1
                    else:
                        print(f"[AVISO] ACK incorreto ou corrompido. Ignorando...")
                except:
                    print("[ERRO] Falha ao processar ACK.")
            else:
                # Ocorreu Timeout
                print(f"\n[TIMEOUT] O tempo esgotou! Retransmitindo pacote {seq_pacote}...")

    
if __name__ == "__main__":
    mensagens = ["Ola", "Mundo", "Redes", "RDT3.0"]
    enviar(mensagens)