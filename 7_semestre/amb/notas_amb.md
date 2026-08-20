Notas aula 1

- Notação:
  - Vetor de entradas: Xnxm
  - Saída: ynx1 ou ynxk
  - Matriz de pesos: W
  - Saída da rede neural: f(W, xi) = ^yi
  - Função de perda: L(yi, ^yi)
- Queremos minimizar a função perda o que corresponde a encontrar a matriz de peso W que minimize essa função


Notas aula 2 (não tem)


Notas aula 3

- Neurônios Artificiais
  - ^y = f(x, w, b) = phi(sum (j=1 até m) wjxj + b)

- Perceptron
  - É garantido que o perceptron converge em n <nmax iterações, desde que as classes sejam linearmente separáveis
  - O algoritmo do perceptron que foi apresentado corrige os pesos de acordo com cada exemplo que é apresentado
  - O uso da função sinal inviabiliza o uso de gradientes


Notas aula 4

- Funções de Ativação
  - Responsável por introduzir não-linearidades em uma rede neural

- Estimador de Máxima Verossimilhança - MLE
  - Maximizar a verossimilhança
  - Minimizar o negativo do log da verossimilhança

- Regressão 
  - saída Gaussiana
      - Ao maximizar a verossimilhança, no caso de um neurônio de saída linear, estamos minimizando o MSE
  - saída Bernoulli 
      - y^= sigma(wh)
      - sigma é a função sigmoide logistica, sigma(x) = 1 / 1 + exp(-x)
  - Multinoulli
      - usamos a softmax


Notas aula 5

- Multilayer Perceprton
  - Usado para separar padrões não linearmnete separáveis
  - Combinamos a saida de 2 ou mais perceptrons
  - Ideia: usamos neurônios para aprender projeções a partir de entradas de forma que o problema fique linearmente separável
  - tanto os neurônios das camadas ocultas como da camada de saida combinam linearmente suas entradas e seus pesos e submetem a soma a uma função de ativação
  - A forma mais simples de combinar neuronios em camads para aprender essas representações latentes consiste em construir camadas de neuronios totalmente conectadas
