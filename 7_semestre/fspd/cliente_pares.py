import sys
import grpc
import sistema_pb2
import sistema_pb2_grpc

def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    target = sys.argv[1]
    
    # Conecta ao servidor gRPC
    channel = grpc.insecure_channel(target)
    stub = sistema_pb2_grpc.ServidorParesStub(channel)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split(',', 2)
        cmd = parts[0]

        try:
            if cmd == 'I' and len(parts) == 3:
                ch = int(parts[1])
                val = parts[2]
                resp = stub.Insercao(sistema_pb2.InsercaoRequest(chave=ch, valor=val))
                print(resp.status)

            elif cmd == 'C' and len(parts) >= 2:
                ch = int(parts[1])
                resp = stub.Consulta(sistema_pb2.ConsultaRequest(chave=ch))
                # Imprime o valor (seja ele o texto ou a string vazia exigida)
                print(resp.valor)

            elif cmd == 'A' and len(parts) >= 2:
                ident = parts[1]
                resp = stub.Activacao(sistema_pb2.ActivacaoRequest(identificador_servico=ident))
                print(resp.status)

            elif cmd == 'T':
                resp = stub.Termino(sistema_pb2.TerminoParesRequest())
                print(resp.chaves_definidas)
                break
                
        except grpc.RpcError as e:
            # Ignora erros de RPC silenciosamente conforme diretriz de saída padrão limpa
            pass

if __name__ == '__main__':
    main()
