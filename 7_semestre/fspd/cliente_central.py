import sys
import grpc

import sistema_pb2
import sistema_pb2_grpc

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
        
    target_central = sys.argv[1]
    
    # Conecta ao servidor centralizador
    channel_central = grpc.insecure_channel(target_central)
    stub_central = sistema_pb2_grpc.ServidorCentralStub(channel_central)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split(',')
        cmd = parts[0]

        try:
            if cmd == 'T':
                resp = stub_central.Termino(sistema_pb2.TerminoCentralRequest())
                print(resp.chaves_registradas)
                break
                
            elif cmd == 'C' and len(parts) == 2:
                ch = int(parts[1])
                
                # 1. Consulta o mapeamento no Servidor Central
                resp_map = stub_central.Mapeamento(sistema_pb2.MapeamentoRequest(chave=ch))
                
                if resp_map.identificador_servico != "":
                    # 2. Achou o servidor de pares! Conecta diretamente nele
                    peer_channel = grpc.insecure_channel(resp_map.identificador_servico)
                    peer_stub = sistema_pb2_grpc.ServidorParesStub(peer_channel)
                    
                    # 3. Faz a consulta RPC ao servidor de pares
                    resp_peer = peer_stub.Consulta(sistema_pb2.ConsultaRequest(chave=ch))
                    
                    # 4. Imprime no formato "Identificador:Valor"
                    print(f"{resp_map.identificador_servico}:{resp_peer.valor}")
                    
        except grpc.RpcError:
            # Tratamento silencioso para manter conformidade com a correção automática
            pass

if __name__ == '__main__':
    main()
