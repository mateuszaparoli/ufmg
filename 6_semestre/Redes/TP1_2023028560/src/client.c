#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include "protocol.h"

int main(int agrc, char* argv[]) {
    if (agrc != 3){
        printf("Quantidade incorreta de argumentos\n");
        return 1;
    }

    char *ipAddress = argv[1];
    int port = atoi(argv[2]);

    int ipType = AF_INET;
    for (int i = 0; ipAddress[i] != '\0'; i++) {
        if (ipAddress[i] == ':') {
            ipType = AF_INET6;
            break;
        }
    }

    int generalSocket = socket(ipType, SOCK_STREAM, 0);

    if (generalSocket == -1) {
        printf("Erro na etapa de criação de socket do cliente");
        return 1;
    }

    if (ipType == AF_INET){
        struct sockaddr_in address;
        memset(&address, 0, sizeof(address));
        address.sin_family = AF_INET;
        address.sin_port = htons(port);
        inet_pton(AF_INET, ipAddress, &address.sin_addr);

        if (connect(generalSocket, (struct sockaddr*)&address, sizeof(address)) == -1) {
            printf("Erro na etapa de conexão do cliente");
            close(generalSocket);
            return 1;
        }
    } else {
        struct sockaddr_in6 address;
        memset(&address, 0, sizeof(address));
        address.sin6_family = AF_INET6;
        address.sin6_port = htons(port);
        inet_pton(AF_INET6, ipAddress, &address.sin6_addr);

        if (connect(generalSocket, (struct sockaddr*)&address, sizeof(address)) == -1) {
            printf("Erro na etapa de conexão do cliente");
            close(generalSocket);
            return 1;
        }
    }

    BattleMessage message;

    while(1){
        ssize_t receiveFromServer = recv(generalSocket, &message, sizeof(message), 0);

        if (receiveFromServer <= 0) {
            break;
        }

        printf("%s\n", message.message);

        if (message.type == MSG_GAME_OVER) {
            break;
        }

        if (message.type == MSG_ACTION_REQ) {
            int choice;
            printf("> ");
            if (scanf("%d", &choice) != 1) {
                break;
            }

            BattleMessage response;
            memset(&response, 0, sizeof(response));
            response.type = MSG_ACTION_RES;
            response.client_action = choice;
            send(generalSocket, &response, sizeof(response), 0);
        }
    }

    close(generalSocket);
    return 0;
}