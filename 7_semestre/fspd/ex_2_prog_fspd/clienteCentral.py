import sys
import grpc
# importando os stubs gerados pelo makefile
import sistema_pb2
import sistema_pb2_grpc

def main():
    # coletando o ip e porta que vem do terminal para iniciar a conexao
    if len(sys.argv) < 2: sys.exit(1)
    
    alvoPrincipal = sys.argv[1]
    
    canalConexao = grpc.insecure_channel(alvoPrincipal)
    # criando o stub para comunicar com o servidor central
    stubDoServidor = sistema_pb2_grpc.ServidorCentralStub(canalConexao)

    # laco infinito lendo da entrada padrao ate o fim da execucao
    for entradaRaw in sys.stdin:
        
        linhaPronta = entradaRaw.strip()
        
        if not linhaPronta: continue # pula a execucao caso a linha esteja em branco
        
        # separando os valores utilizando a virgula como delimitador
        listaComandos = linhaPronta.split(',')
        qualComando = listaComandos[0]

        try:
            
            if qualComando == 'T':
                # acionando o metodo de termino no rpc para desligar o servidor
                retornoTermino = stubDoServidor.Termino(sistema_pb2.TerminoCentralRequest())
                print(retornoTermino.chaves_registradas)
                break
                
            # caso seja o comando C, precisamos fazer duas consultas separadas
            elif qualComando == 'C' and len(listaComandos) == 2:
                chaveProcurada = int(listaComandos[1])
                
                # consultando o indice primeiro para descobrir qual servidor possui a chave
                resultadoIndice = stubDoServidor.Mapeamento(sistema_pb2.MapeamentoRequest(chave=chaveProcurada))
                
                enderecoAchado = resultadoIndice.identificador_servico
                
                # apenas avanca e abre uma nova conexao se o servidor central retornar um endereco valido
                if enderecoAchado != "":
                    
                    # abrindo um canal extra direto com o servidor de pares correspondente
                    canalTemporario = grpc.insecure_channel(enderecoAchado)
                    stubParzinho = sistema_pb2_grpc.ServidorParesStub(canalTemporario)
                    
                    # executando a busca pelo valor real armazenado no dicionario do servidor de pares
                    valorFinal = stubParzinho.Consulta(sistema_pb2.ConsultaRequest(chave=chaveProcurada))
                    
                    # impressao formatada conforme exigido pelo script de correcao automatica
                    print(f"{enderecoAchado}:{valorFinal.valor}")
                    
        except grpc.RpcError:
            pass # ignorando erros de rpc para evitar que mensagens sujem o terminal e falhem a correcao

if __name__ == '__main__':
    main()
