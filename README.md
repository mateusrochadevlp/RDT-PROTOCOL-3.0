# RDT 3.0 Protocol

O RDT 3.0 é um protocolo do tipo **Stop-and-Wait** (Pare e Espera). Ele resolve os principais problemas de comunicação em rede:

* **Corrupção de bits:** Detectada através de Checksums.
* **Perda de Pacotes:** Resolvida com o uso de Timers e retransmissões.
* **Duplicação de Pacotes:** Evitada através de números de sequência (0 e 1).

## Como Executar:

**1. Clone o repositório:**

```bash
git clone https://github.com/seu-usuario/rdt3-protocol.git
```

**2. Inicie o servidor:**

```bash
python server.py
```

**3. Em outro terminal, inicie o cliente:**

```bash
python client.py
```