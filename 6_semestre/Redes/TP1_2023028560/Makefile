CC = gcc
CFLAGS = -Wall -Wextra -std=c11
SRC_DIR = src
BIN_DIR = bin

all: $(BIN_DIR)/server $(BIN_DIR)/client

$(BIN_DIR)/server: $(SRC_DIR)/server.c
	mkdir -p $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@

$(BIN_DIR)/client: $(SRC_DIR)/client.c
	mkdir -p $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf $(BIN_DIR)