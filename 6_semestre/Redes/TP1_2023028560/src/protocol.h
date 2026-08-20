#define MSG_SIZE 256

typedef enum {
    MSG_INIT,
    MSG_ACTION_REQ,
    MSG_ACTION_RES,
    MSG_BATTLE_RESULT,
    MSG_INVENTORY,
    MSG_GAME_OVER,
    MSG_ESCAPE
} MessageType;

typedef struct {
    int type;
    int client_action;
    int server_action;
    int client_hp;
    int server_hp;
    int client_torpedoes;
    int client_shields;
    char message[MSG_SIZE];
} BattleMessage;