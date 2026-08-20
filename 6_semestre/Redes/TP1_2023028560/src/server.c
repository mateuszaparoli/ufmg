#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <time.h>
#include "protocol.h"

static int send_message(int dedicatedSocket, const BattleMessage *message);
void gameLogic(int dedicatedSocket);

int main(int argc, char *argv[]) {
    if (argc != 3){
        printf("Quantidade incorreta de argumentos.\n");
        return 1;
    }
    
    int ipType = strcmp(argv[1], "v4") == 0 ? AF_INET : strcmp(argv[1], "v6") == 0 ? AF_INET6 : -1;
    if (ipType == -1){
        printf("Tipo de IP inválido.\n");
        return 1;
    }
    
    int generalSocket = socket(ipType, SOCK_STREAM, 0);
    if (generalSocket == -1){
        printf("Não foi possível criar o socket.\n");
        return 1;
    }
    
    int port = atoi(argv[2]);
    if (ipType == AF_INET) {
        struct sockaddr_in address;
        memset(&address, 0, sizeof(address));

        address.sin_family = AF_INET;
        address.sin_port = htons(port);
        address.sin_addr.s_addr = INADDR_ANY;

        if (bind(generalSocket, (struct sockaddr*)&address, sizeof(address)) == -1) {
            printf("Erro na etapa de bind");
            return 1;
        }
    } else {
        struct sockaddr_in6 address;
        memset(&address, 0, sizeof(address));
        
        address.sin6_family = AF_INET6;
        address.sin6_port = htons(port);
        address.sin6_addr = in6addr_any;
        
        if (bind(generalSocket, (struct sockaddr*)&address, sizeof(address)) == -1) {
            printf("Erro na etapa de bind");
            return 1;
        }
    }

    if (listen(generalSocket, 1) == -1) {
        printf("Erro na etapa de listen");
        return 1;
    }

    while (1) {
        int dedicatedSocket = accept(generalSocket, 0, 0);
        if (dedicatedSocket == -1) {
            printf("Erro na etapa de accept\n");
            continue;
        }

        gameLogic(dedicatedSocket);
        close(dedicatedSocket);
    }

    close(generalSocket);

    return 0;
}

static int send_message(int dedicatedSocket, const BattleMessage *message) {
    ssize_t sent = send(dedicatedSocket, message, sizeof(*message), 0);
    if (sent <= 0) {
        printf("Erro ao enviar mensagem ao cliente\n");
        return -1;
    }
    return 0;
}

void gameLogic(int dedicatedSocket) {
    int client_hp = 100;
    int server_hp = 100;
    int client_torpedoes = 0;
    int client_shields = 0;
    int turns = 0;

    BattleMessage message;
    memset(&message, 0, sizeof(message));

    message.type = MSG_INIT;
    message.client_hp = client_hp;
    message.server_hp = server_hp;
    message.client_torpedoes = client_torpedoes;
    message.client_shields = client_shields;
    strcpy(message.message, "Conectado ao servidor.\nSua nave: SS-42 Voyager (HP: 100)");

    if (send_message(dedicatedSocket, &message) == -1) {
        return;
    }

    srand((unsigned)time(0));

    while (client_hp > 0 && server_hp > 0){
        turns++;
        memset(&message, 0, sizeof(message));
        message.type = MSG_ACTION_REQ;
        strcpy(message.message, "\nEscolha sua ação:\n0 - Laser Attack\n1 - Photon Torpedo\n2 - Shields Up\n3 - Cloaking\n4 - Hyper Jump\n");

        if (send_message(dedicatedSocket, &message) == -1) {
            return;
        }

        BattleMessage answerMessage;
        memset(&answerMessage, 0, sizeof(answerMessage));

        ssize_t received = recv(dedicatedSocket, &answerMessage, sizeof(answerMessage), 0);
        if (received <= 0) {
            printf("Cliente desconectado durante a partida\n");
            return;
        }

        int playerAction = answerMessage.client_action;

        if (playerAction < 0 || playerAction > 4) {
            memset(&message, 0, sizeof(message));
            message.type = MSG_BATTLE_RESULT;
            strcpy(message.message, "Erro: escolha inválida!\nPor favor selecione um valor entre 0 a 4.\n");
            if (send_message(dedicatedSocket, &message) == -1) {
                return;
            }
            continue;
        }
        
        if(playerAction == 1){
            client_torpedoes++;
        } else if (playerAction == 2){
            client_shields++;
        }

        int serverAction = rand() % 5;

        if (playerAction == 4 || serverAction == 4) {
            if (playerAction == 4 && serverAction == 4){
                memset(&message, 0, sizeof(message));
                message.type = MSG_ESCAPE;
                strcpy(message.message, "Ambos acionaram o Hyper Jump!\nFuga mútua para o hiperespaço.\n");
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
            } else if (playerAction == 4) {
                memset(&message, 0, sizeof(message));
                message.type = MSG_ESCAPE;
                strcpy(message.message, "Você acionou o Hyper Jump!\nSua nave escapou para o hiperespaço.\n");
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
            } else {
                memset(&message, 0, sizeof(message));
                message.type = MSG_ESCAPE;
                strcpy(message.message, "O servidor acionou o Hyper Jump!\nA nave dele escapou para o hiperespaço.\n");
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
            }
            
            memset(&message, 0, sizeof(message));
            message.type = MSG_GAME_OVER;
            sprintf(message.message, "Inventário final:\n- HP restante: %d\n- HP inimigo: %d\n- Torpedos usados: %d\n- Escudos usados: %d\n- Turnos jogados: %d\nObrigado por jogar!", client_hp, server_hp, client_torpedoes, client_shields, turns);
            if (send_message(dedicatedSocket, &message) == -1) {
                return;
            }
            return;
        }

        if (playerAction == 0) {
            if (serverAction == 0) {
                client_hp -= 20;
                server_hp -= 20;
                memset(&message, 0, sizeof(message));
                message.type = MSG_BATTLE_RESULT;
                message.client_hp = client_hp;
                message.server_hp = server_hp;
                sprintf(message.message, "Você disparou um Laser!\nServidor disparou um Laser.\nResultado: Ambos receberam 20 de dano!\nPlacar: Você %d x %d Inimigo", client_hp, server_hp);
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
                continue;
            } else if (serverAction == 1) {
                client_hp -= 20;
                memset(&message, 0, sizeof(message));
                message.type = MSG_BATTLE_RESULT;
                message.client_hp = client_hp;
                message.server_hp = server_hp;
                sprintf(message.message, "Você disparou um Laser!\nServidor disparou um Photon Torpedo.\nResultado: Você recebeu 20 de dano!\nPlacar: Você %d x %d Inimigo", client_hp, server_hp);
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
                continue;
            } else if (serverAction == 2) {
                memset(&message, 0, sizeof(message));
                message.type = MSG_BATTLE_RESULT;
                message.client_hp = client_hp;
                message.server_hp = server_hp;
                sprintf(message.message, "Você disparou um Laser!\nServidor ativou Escudos!\nResultado: Seu ataque foi bloqueado!\nPlacar: Você %d x %d Inimigo", client_hp, server_hp);
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
                continue;
            } else if (serverAction == 3) {
                server_hp -= 20;
                memset(&message, 0, sizeof(message));
                message.type = MSG_BATTLE_RESULT;
                message.client_hp = client_hp;
                message.server_hp = server_hp;
                sprintf(message.message, "Você disparou um Laser!\nServidor ativou Cloaking!\nResultado: Acerto! Nave inimiga perdeu 20 HP!\nPlacar: Você %d x %d Inimigo", client_hp, server_hp);
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
                continue;
            }
        }

        if (playerAction == 1) {
            if (serverAction == 0) {
                server_hp -= 20;
                memset(&message, 0, sizeof(message));
                message.type = MSG_BATTLE_RESULT;
                message.client_hp = client_hp;
                message.server_hp = server_hp;
                sprintf(message.message, "Você disparou um Photon Torpedo!\nServidor disparou um Laser!\nResultado: Acerto! Nave inimiga perdeu 20 HP!\nPlacar: Você %d x %d Inimigo", client_hp, server_hp);
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
                continue;
            } else if (serverAction == 1) {
                client_hp -= 20;
                server_hp -= 20;
                memset(&message, 0, sizeof(message));
                message.type = MSG_BATTLE_RESULT;
                message.client_hp = client_hp;
                message.server_hp = server_hp;
                sprintf(message.message, "Você disparou um Photon Torpedo!\nServidor disparou um Photon Torpedo!\nResultado: Ambos receberam 20 de dano!\nPlacar: Você %d x %d Inimigo", client_hp, server_hp);
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
                continue;
            } else if (serverAction == 2) {
                memset(&message, 0, sizeof(message));
                message.type = MSG_BATTLE_RESULT;
                message.client_hp = client_hp;
                message.server_hp = server_hp;
                sprintf(message.message, "Você disparou um Photon Torpedo!\nServidor ativou Escudos!\nResultado: Seu ataque foi bloqueado!\nPlacar: Você %d x %d Inimigo", client_hp, server_hp);
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
                continue;
            } else if (serverAction == 3) {
                memset(&message, 0, sizeof(message));
                message.type = MSG_BATTLE_RESULT;
                message.client_hp = client_hp;
                message.server_hp = server_hp;
                sprintf(message.message, "Você disparou um Photon Torpedo!\nServidor ativou Cloaking!\nResultado: Servidor evitou o ataque\nPlacar: Você %d x %d Inimigo", client_hp, server_hp);
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
                continue;
            }
        }

        if (playerAction == 2) {
            if (serverAction == 0){
                memset(&message, 0, sizeof(message));
                message.type = MSG_BATTLE_RESULT;
                message.client_hp = client_hp;
                message.server_hp = server_hp;
                sprintf(message.message, "Você ativou Escudos!\nServidor disparou um Laser!\nResultado: Ataque inimigo bloqueado!\nPlacar: Você %d x %d Inimigo", client_hp, server_hp);
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
                continue;
            } else if (serverAction == 1) {
                memset(&message, 0, sizeof(message));
                message.type = MSG_BATTLE_RESULT;
                message.client_hp = client_hp;
                message.server_hp = server_hp;
                sprintf(message.message, "Você ativou Escudos!\nServidor disparou um Photon Torpedo!\nResultado: Ataque inimigo bloqueado!\nPlacar: Você %d x %d Inimigo", client_hp, server_hp);
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
                continue;
            } else if (serverAction == 2) {
                memset(&message, 0, sizeof(message));
                message.type = MSG_BATTLE_RESULT;
                message.client_hp = client_hp;
                message.server_hp = server_hp;
                sprintf(message.message, "Você ativou Escudos!\nServidor ativou Escudos!\nResultado: Nenhum dano causado!\nPlacar: Você %d x %d Inimigo", client_hp, server_hp);
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
                continue;
            } else if (serverAction == 3) {
                memset(&message, 0, sizeof(message));
                message.type = MSG_BATTLE_RESULT;
                message.client_hp = client_hp;
                message.server_hp = server_hp;
                sprintf(message.message, "Você ativou Escudos!\nServidor ativou Cloaking!\nResultado: Nenhum dano causado!\nPlacar: Você %d x %d Inimigo", client_hp, server_hp);
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
                continue;
            }
        }

        if (playerAction == 3) {
            if (serverAction == 0) {
                client_hp -= 20;
                memset(&message, 0, sizeof(message));
                message.type = MSG_BATTLE_RESULT;
                message.client_hp = client_hp;
                message.server_hp = server_hp;
                sprintf(message.message, "Você ativou Cloaking!\nServidor disparou um Laser!\nResultado: Você recebeu 20 de dano!\nPlacar: Você %d x %d Inimigo", client_hp, server_hp);
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
                continue;
            } else if (serverAction == 1) {
                memset(&message, 0, sizeof(message));
                message.type = MSG_BATTLE_RESULT;
                message.client_hp = client_hp;
                message.server_hp = server_hp;
                sprintf(message.message, "Você ativou Cloaking!\nServidor disparou um Photon Torpedo!\nResultado: Ataque inimigo falhou!\nPlacar: Você %d x %d Inimigo", client_hp, server_hp);
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
                continue;
            } else if (serverAction == 2) {
                memset(&message, 0, sizeof(message));
                message.type = MSG_BATTLE_RESULT;
                message.client_hp = client_hp;
                message.server_hp = server_hp;
                sprintf(message.message, "Você ativou Cloaking!\nServidor ativou os Escudos!\nResultado: Nenhum dano causado!\nPlacar: Você %d x %d Inimigo", client_hp, server_hp);
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
                continue;
            } else if (serverAction == 3) {
                memset(&message, 0, sizeof(message));
                message.type = MSG_BATTLE_RESULT;
                message.client_hp = client_hp;
                message.server_hp = server_hp;
                sprintf(message.message, "Você ativou Cloaking!\nServidor ativou Cloaking!\nResultado: Nenhum dano causado!\nPlacar: Você %d x %d Inimigo", client_hp, server_hp);
                if (send_message(dedicatedSocket, &message) == -1) {
                    return;
                }
                continue;
            }
        }
    }

    memset(&message, 0, sizeof(message));
    message.type = MSG_GAME_OVER;
    message.client_hp = client_hp;
    message.server_hp = server_hp;
    message.client_torpedoes = client_torpedoes;
    message.client_shields = client_shields;

    if (client_hp <= 0 && server_hp <= 0) {
        sprintf(message.message, "\nFim de jogo!\nInventário final:\n- HP restante: %d\n- HP inimigo: %d\n- Torpedos usados: %d\n- Escudos usados: %d\n- Turnos jogados: %d\nEmpate! Ambas as naves foram destruídas!", client_hp, server_hp, client_torpedoes, client_shields, turns);
    } else if (client_hp <= 0) {
        sprintf(message.message, "\nFim de jogo!\nInventário final:\n- HP restante: %d\n- HP inimigo: %d\n- Torpedos usados: %d\n- Escudos usados: %d\n- Turnos jogados: %d\nSua nave foi destruída!", client_hp, server_hp, client_torpedoes, client_shields, turns);
    } else {
        sprintf(message.message, "\nFim de jogo!\nInventário final:\n- HP restante: %d\n- HP inimigo: %d\n- Torpedos usados: %d\n- Escudos usados: %d\n- Turnos jogados: %d\nVocê derrotou a frota inimiga!", client_hp, server_hp, client_torpedoes, client_shields, turns);
    }

    send_message(dedicatedSocket, &message);
}