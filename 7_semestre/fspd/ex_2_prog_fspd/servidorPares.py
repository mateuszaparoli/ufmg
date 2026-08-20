import sys
import time
import threading
import socket
from concurrent import futures
import grpc

# importando os arquivos gerados pela compilação do protocolo
import sistema_pb2
import sistema_pb2_grpc

class ServidorParesServicer(sistema_pb2_grpc.ServidorParesServicer):
    def __init__(self, modoExecucao, portaEscolhida, servidorInstancia):
        self.modoExecucao = modoExecucao
        self.portaEscolhida = portaEscolhida
        self.servidorInstancia = servidorInstancia
        self.dicionarioValores = {}
        self.travaExclusaoMutua = threading.Lock()

    def Insercao(self, request, context):
        with self.travaExclusaoMutua:
            
            # verificando se a chave já existe no dicionário para não sobrescrever
            if request.chave in self.dicionarioValores:
                return sistema_pb2.InsercaoResponse(status=-1)
            else:
                self.dicionarioValores[request.chave] = request.valor
                return sistema_pb2.InsercaoResponse(status=0)

    def Consulta(self, request, context):
        with self.travaExclusaoMutua:
            
            # buscando o valor associado à chave ou retornando uma string vazia caso não exista
            valorEncontrado = self.dicionarioValores.get(request.chave, "")
            
            return sistema_pb2.ConsultaResponse(valor=valorEncontrado)

    def Activacao(self, request, context):
        if self.modoExecucao == 1:
            # no modo um o comportamento é independente e o servidor apenas retorna zero
            return sistema_pb2.ActivacaoResponse(status=0)
            
        else:
            # no modo dois precisamos realizar a integração com o servidor centralizador
            enderecoCentral = request.identificador_servico

            # descobrindo o próprio nome na rede para montar o endereço completo dinamicamente
            meuNomeHost = socket.getfqdn()
            meuEnderecoCompleto = f"{meuNomeHost}:{self.portaEscolhida}"

            # coletando todas as chaves que estão armazenadas de forma segura
            with self.travaExclusaoMutua:
                listaChavesAtuais = list(self.dicionarioValores.keys())

            try:
                # abrindo a conexão direta com o servidor central
                canalConexaoCentral = grpc.insecure_channel(enderecoCentral)
                stubDoCentral = sistema_pb2_grpc.ServidorCentralStub(canalConexaoCentral)

                # executando a chamada de procedimento remoto para registrar a lista de chaves
                requisicaoRegistro = sistema_pb2.RegistroRequest(
                    identificador_servico=meuEnderecoCompleto,
                    chaves=listaChavesAtuais
                )
                respostaRegistro = stubDoCentral.Registro(requisicaoRegistro)

                # retornando a quantidade exata de chaves que foram processadas com sucesso
                return sistema_pb2.ActivacaoResponse(status=respostaRegistro.chaves_processadas)

            except grpc.RpcError:
                # em caso de falha na comunicação com o centralizador retornamos zero
                return sistema_pb2.ActivacaoResponse(status=0)


    def Termino(self, request, context):
        with self.travaExclusaoMutua:
            quantidadeChaves = len(self.dicionarioValores)

        def tarefaDesligamento():
            # aguardando o tempo necessário para que o pacote de resposta seja enviado ao cliente
            time.sleep(1)
            self.servidorInstancia.stop(0)

        # iniciando uma thread separada para não bloquear o retorno imediato do procedimento
        threading.Thread(target=tarefaDesligamento).start()
        
        return sistema_pb2.TerminoParesResponse(chaves_definidas=quantidadeChaves)


def iniciarServidorPares():
    
    # conferindo se o modo de operação e a porta foram passados corretamente via terminal
    if len(sys.argv) < 3: sys.exit(1)

    modoExecucao = int(sys.argv[1])
    portaEscolhida = sys.argv[2]

    # criando o servidor com o pool de threads para gerenciar as requisições concorrentes
    servidorGrpc = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # instanciando a nossa classe de serviço e conectando ao servidor principal
    classeServico = ServidorParesServicer(modoExecucao, portaEscolhida, servidorGrpc)
    sistema_pb2_grpc.add_ServidorParesServicer_to_server(classeServico, servidorGrpc)

    # liberando a porta para receber conexões externas sem criptografia
    servidorGrpc.add_insecure_port(f'[::]:{portaEscolhida}')
    servidorGrpc.start()

    # mantendo a aplicação ativa até receber o sinal de encerramento do cliente
    servidorGrpc.wait_for_termination()


if __name__ == '__main__':
    iniciarServidorPares()
