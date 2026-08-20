import sys
import time
import threading
from concurrent import futures
import grpc

import sistema_pb2
import sistema_pb2_grpc

class ServidorCentralServicer(sistema_pb2_grpc.ServidorCentralServicer):
    def __init__(self, server):
        self.server = server
        self.mapa = {}  # Mapeia: chave -> identificador_servico
        self.lock = threading.Lock()

    def Registro(self, request, context):
        with self.lock:
            # Associa (ou sobrescreve) cada chave recebida ao servidor de pares
            for chave in request.chaves:
                self.mapa[chave] = request.identificador_servico
            
            return sistema_pb2.RegistroResponse(chaves_processadas=len(request.chaves))

    def Mapeamento(self, request, context):
        with self.lock:
            # Retorna o identificador se existir, senão retorna string vazia
            addr = self.mapa.get(request.chave, "")
            return sistema_pb2.MapeamentoResponse(identificador_servico=addr)

    def Termino(self, request, context):
        with self.lock:
            total_chaves = len(self.mapa)
            
        def shutdown_task():
            time.sleep(1)
            self.server.stop(0)
            
        threading.Thread(target=shutdown_task).start()
        return sistema_pb2.TerminoCentralResponse(chaves_registradas=total_chaves)

def serve():
    if len(sys.argv) < 2:
        sys.exit(1)
        
    port = sys.argv[1]
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = ServidorCentralServicer(server)
    sistema_pb2_grpc.add_ServidorCentralServicer_to_server(servicer, server)
    
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
