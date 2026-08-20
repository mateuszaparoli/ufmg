import sys
import grpc
# importando as classes geradas automaticamente pela compilacao do arquivo proto
import sistema_pb2
import sistema_pb2_grpc

def main():
    # verificando se o endereco do servidor foi passado nos argumentos do terminal
    if len(sys.argv) < 2: sys.exit(1)

    alvoPrincipal = sys.argv[1]

    # estabelecendo a conexao insegura exigida pelo trabalho
    canalConexao = grpc.insecure_channel(alvoPrincipal)
    stubParzinho = sistema_pb2_grpc.ServidorParesStub(canalConexao)

    # laco de repeticao lendo os comandos diretamente da entrada padrao
    for entradaRaw in sys.stdin:
        
        linhaPronta = entradaRaw.strip()
        
        # se a linha for vazia o laco apenas continua para a proxima iteracao
        if not linhaPronta: continue

        # limitando a divisao em tres partes para garantir que os espacos do valor sejam preservados
        listaComandos = linhaPronta.split(',', 2)
        qualComando = listaComandos[0]

        try:
            
            # execucao do comando de insercao no dicionario
            if qualComando == 'I' and len(listaComandos) == 3:
                chaveEscolhida = int(listaComandos[1])
                valorEscolhido = listaComandos[2]
                
                # disparando a chamada rpc para armazenar o valor
                respostaInsercao = stubParzinho.Insercao(sistema_pb2.InsercaoRequest(chave=chaveEscolhida, valor=valorEscolhido))
                print(respostaInsercao.status)

            # execucao do comando de consulta de uma chave especifica
            elif qualComando == 'C' and len(listaComandos) >= 2:
                chaveProcurada = int(listaComandos[1])
                
                respostaConsulta = stubParzinho.Consulta(sistema_pb2.ConsultaRequest(chave=chaveProcurada))
                
                # a saida sera o texto encontrado ou uma string vazia caso a chave nao exista
                print(respostaConsulta.valor)

            # execucao do comando de ativacao para enviar as chaves ao servidor central
            elif qualComando == 'A' and len(listaComandos) >= 2:
                enderecoCentral = listaComandos[1]
                
                respostaAtivacao = stubParzinho.Activacao(sistema_pb2.ActivacaoRequest(identificador_servico=enderecoCentral))
                print(respostaAtivacao.status)

            # execucao do comando de termino que encerra o servidor e este script
            elif qualComando == 'T':
                respostaTermino = stubParzinho.Termino(sistema_pb2.TerminoParesRequest())
                print(respostaTermino.chaves_definidas)
                break

        except grpc.RpcError as erroDeRede:
            # ocultando erros de conexao intencionalmente para satisfazer os requisitos do corretor automatico
            pass

if __name__ == '__main__':
    main()
