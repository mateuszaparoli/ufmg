import sys
import time
import threading
from concurrent import futures
import grpc

# importando as dependencias geradas a partir do arquivo proto
import sistema_pb2
import sistema_pb2_grpc

class ServidorCentralServicer(sistema_pb2_grpc.ServidorCentralServicer):
    def __init__(self, servidorInstancia):
        self.servidorInstancia = servidorInstancia
        self.dicionarioChaves = {} # mapeia a chave em inteiro para a string do endereco de rede
        self.travaExclusaoMutua = threading.Lock()

    def Registro(self, request, context):
        with self.travaExclusaoMutua:
            
            # iterando sobre as chaves recebidas para associar ao servidor que fez a chamada
            for chaveAtual in request.chaves:
                
                # em caso de colisao o valor antigo e sobrescrito sem problemas
                self.dicionarioChaves[chaveAtual] = request.identificador_servico

            return sistema_pb2.RegistroResponse(chaves_processadas=len(request.chaves))

    def Mapeamento(self, request, context):
        with self.travaExclusaoMutua:
            
            # procura a chave no dicionario e retorna string vazia se nao houver registro
            enderecoEncontrado = self.dicionarioChaves.get(request.chave, "")
            
            return sistema_pb2.MapeamentoResponse(identificador_servico=enderecoEncontrado)

    def Termino(self, request, context):
        with self.travaExclusaoMutua:
            quantidadeTotal = len(self.dicionarioChaves)

        def tarefaDesligamento():
            # aguardando um segundo de forma assincrona para o pacote de resposta conseguir chegar ao cliente
            time.sleep(1)
            self.servidorInstancia.stop(0)

        threading.Thread(target=tarefaDesligamento).start()
        
        return sistema_pb2.TerminoCentralResponse(chaves_registradas=quantidadeTotal)


def iniciarServidor():
    
    # validando a passagem da porta na linha de comando antes de subir a rede
    if len(sys.argv) < 2: sys.exit(1)

    portaEscolhida = sys.argv[1]

    # alocando um conjunto de dez threads para processar as chamadas concorrentes
    servidorGrpc = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    classeServico = ServidorCentralServicer(servidorGrpc)
    
    sistema_pb2_grpc.add_ServidorCentralServicer_to_server(classeServico, servidorGrpc)

    servidorGrpc.add_insecure_port(f'[::]:{portaEscolhida}')
    servidorGrpc.start()
    
    # trava a execucao principal para manter o servidor escutando requisicoes ativamente
    servidorGrpc.wait_for_termination()


if __name__ == '__main__':
    iniciarServidor()
