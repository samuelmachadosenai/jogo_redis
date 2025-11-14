from random import randint
import time
import os
import redis

# Conexão Redis
r = redis.Redis(host='127.0.0.1', port=6379, db=0)


def front(state: int, user_credits, user_j = 0, machine_j = 0):
    choi = ["👊", "🖐", "✌", "??"]
    user_j = choi[user_j - 1]
    machine_j = choi[machine_j - 1]
    os.system("cls" if os.name == "nt" else "clear")
    print("+-------------------------------+")
    print(f"+user_credits:{user_credits}\t\t\t+")
    print("+-------------------------------+")
    print("+        ._._.     _|.|_        +")
    if state == 0:
        print("+       (´-_-`)   [´-_-`]       +")
        print("+       \\\\  //     \\\\  //       +")
        print(f"+       [{user_j}]//|     |\\\\[{machine_j}]     +")
    elif state == 1:
        print("+       (´-_-`)   [´-_-`]       +")
        print("+        | \\\\ \\\\  // // |       +")
        print(f"+        +--\\[{user_j}][{machine_j}]/--+       +")
    elif state == 2:
        print("+       (*`_´*) 🖕[ ´-_-]       +")
        print("+     \\\\//   \\\\//  | \\_/|       +")
        print("+        +--+      |+--+|       +")
    elif state == 3:
        print("+       (-_-` )🖕 [*`_´*]       +")
        print("+       |\\_/ |  \\\\//   \\\\//     +")
        print("+        +--+      |+--+|       +")
    print("+       / || \\     / || \\       +")
    print("+_______c_|_|_'___c_|_|_'_______+")

def ui(typee: int = 1, user_credits = 0):
    if typee == 1:
        while True:
            try:
                select = int(input("1) 👊\n2) 🖐\n3) ✌\nDigite sua jogada: "))
                if 1 <= select <= 3:
                    return user_credits, select
            except:
                pass
    elif typee == 2:
        print("+------------------+\n|######  #  #######|\n|# @ #   #  # # @ #|\n|#####  ##  # #####|")
        print("|# ##  # #  # #  ##|\n|##    #   #  ##  #|\n|#   # #    #   #  |\n|##### #   #   #  #|")
        print("|# @ #   #  #    ##|\n|#####  #   ##    #|\n+------------------+\nRealize o pagamento com o QR code!")
        os.system("pause")
        return user_credits + 1, None

def anime(user_credits, user_j, machine_j):
    front(state=0, user_credits=user_credits)
    for ii in range(1, 4):
        front(state=0, user_credits=user_credits, user_j=user_j, machine_j=ii)
        time.sleep(0.5)
    for ii in range(1, 4):
        front(state=0, user_credits=user_credits, user_j=user_j, machine_j=ii)
        time.sleep(0.5)
    front(state=1, user_credits=user_credits, user_j=user_j, machine_j=machine_j)
    time.sleep(3)
    if user_j == machine_j:
        return 0
    else:
        if (user_j == 1 and machine_j == 2) or (user_j == 2 and machine_j == 3) or (user_j == 3 and machine_j == 1):
            front(state=3, user_credits=user_credits)
            time.sleep(3)
            return -1
        else:
            front(state=2, user_credits=user_credits)
            time.sleep(3)
            return 1

def generete_win(choi=1):
    return 1 if choi == 3 else choi + 1

def generete_lost(choi=1):
    return 3 if choi == 1 else choi - 1

if __name__ == '__main__':
    user_credits = 0

    sala = input("Nome da sala: ")
    jogador = input("Você é o jogador 1 ou 2? ")

    # Inicializa sala
    if jogador == "1":
       r.hset(sala, "p1", "")
       r.hset(sala, "p2", "")

    while True:
        front(state=0, user_credits=user_credits)
        user_credits, user_j = ui(1, user_credits)

        # Envia jogada pro Redis
        r.hset(f"sala:{sala}", f"p{jogador}", user_j)
        print("Esperando o outro jogador...")

        # Espera o outro jogar
        while True:
            dados = r.hgetall(f"sala:{sala}")
            if b"p1" in dados and b"p2" in dados:
                if dados[b"p1"] != b"" and dados[b"p2"] != b"":
                    break
            time.sleep(0.5)

        # Pega jogadas
        p1 = int(dados[b"p1"].decode())
        p2 = int(dados[b"p2"].decode())

        # Mostra resultado
        if jogador == "1":
            resul = anime(user_credits, p1, p2)
        else:
            resul = anime(user_credits, p2, p1)

        user_credits += resul

        # Limpa pra próxima rodada
        r.hset(sala, "p1", "")
        r.hset(sala, "p2", "")

        # Deleta a sala
        if user_credits <= 0:
            r.delete(f"sala:{sala}")
            print("Sala deletada automaticamente.")
            break

        print("\nNova rodada começando...\n")
        time.sleep(2)