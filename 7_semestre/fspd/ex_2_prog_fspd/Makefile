# Comandos base do python
PY = python3
PIP = pip3
PROTOC = -m grpc_tools.protoc

all: stubs

# Quebra a proteção do pip do debian nas maquinas do lab para instalar o grpc
install_deps:
	$(PIP) install --user grpcio grpcio-tools --break-system-packages

# Compila o arquivo .proto pra gerar as dependencias do grpc
stubs: sistema.proto
	$(PY) $(PROTOC) -I. --python_out=. --grpc_python_out=. sistema.proto

# Limpa a sujeira do grpc e cache do python
clean:
	rm -f *_pb2.py *_pb2_grpc.py
	rm -rf __pycache__

# Cliente do armazenamento simples
run_cli_pares: stubs
	$(PY) clientePares.py $(arg)

# Servidor que só armazena 
run_serv_pares_1: stubs
	$(PY) servidorPares.py 1 $(arg)

# Servidor que se conecta no servicor centralizador
run_serv_pares_2: stubs
	$(PY) servidorPares.py 2 $(arg)

# Servidor central 
run_serv_central: stubs
	$(PY) servidorCentral.py $(arg)

# Cliente que busca a chave no servidor central
run_cli_central: stubs
	$(PY) clienteCentral.py $(arg)
