import sys
import time
import threading
import socket
from concurrent import futures
import grpc

import sistema_pb2
import sistema_pb2_grpc

class ServidorParesServicer(sistema_pb2_grpc.ServidorParesServicer):
    def __init__(self, mode, port, server):
        self.mode = mode
        self.port = port
        self.server = server
        self.store = {}
        self.lock = threading.Lock()

    def Insercao(self, request, context):
        with self.lock:
            if request.chave in self.store:
                return sistema_pb2.InsercaoResponse(status=-1)
            else:
                self.store[request.chave] = request.valor
                return sistema_pb2.InsercaoResponse(status=0)

    def Consulta(self, request, context):
        with self.lock:
            valor = self.store.get(request.chave, "")
            return sistema_pb2.ConsultaResponse(valor=valor)

    def Activacao(self, request, context):
        if self.mode == 1:
            # Modo 1: Comportamento independente
            return sistema_pb2.ActivacaoResponse(status=0)
        else:
            # Modo 2: Integração com o Servidor Central
            identificador_central = request.identificador_servico
            
            # Descobre o próprio host para criar a string "host:porto"
            meu_host = socket.getfqdn()
            meu_identificador = f"{meu_host}:{self.port}"
            
            # Coleta todas as chaves armazenadas no momento
            with self.lock:
                minhas_chaves = list(self.store.keys())

            try:
                # Conecta-se ao servidor centralizador
                channel_central = grpc.insecure_channel(identificador_central)
                stub_central = sistema_pb2_grpc.ServidorCentralStub(channel_central)
                
                # Faz a chamada RPC de Registro
                req_registro = sistema_pb2.RegistroRequest(
                    identificador_servico=meu_identificador,
                    chaves=minhas_chaves
                )
                resp_registro = stub_central.Registro(req_registro)
                
                # Retorna ao cliente a quantidade de chaves que foram registradas
                return sistema_pb2.ActivacaoResponse(status=resp_registro.chaves_processadas)
            
            except grpc.RpcError:
                # Se falhar a comunicação com o central, retorna 0
                return sistema_pb2.ActivacaoResponse(status=0)


    def Termino(self, request, context):
        with self.lock:
            chaves_definidas = len(self.store)
        
        # Cria uma thread para desligar o servidor após 1 segundo
        # Garantindo que a resposta atual seja enviada ao cliente com sucesso.
        def shutdown_task():
            time.sleep(1)
            self.server.stop(0)
            
        threading.Thread(target=shutdown_task).start()
        return sistema_pb2.TerminoParesResponse(chaves_definidas=chaves_definidas)

def serve():
    if len(sys.argv) < 3:
        sys.exit(1)

    mode = int(sys.argv[1])
    port = sys.argv[2]

    # Inicializa o servidor gRPC com um pool de threads
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Acopla a nossa implementação ao servidor
    servicer = ServidorParesServicer(mode, port, server)
    sistema_pb2_grpc.add_ServidorParesServicer_to_server(servicer, server)

    # Abre a porta para conexões inseguras (sem SSL/TLS, padrão para o trabalho)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    # Mantém o processo vivo até o server.stop() ser chamado
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
