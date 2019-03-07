# Machine Learning em Produção
O Machine Learning to production tem como principal funcao "emular" como um grande projeto seria colocado em produção.

Possui os seguintes componentes:

* <b>process</b>: Processamento dos dados.
* <b>database</b>: Configuracoes e ingestoes do Banco de Dados MongoDB.
* <b>config</b>: Possui arquivos shell que preparam o ambiente.
* <b>model</b>: Criacao do modelo de Machine Learning.
* <b>api</b>: Criacao de uma API a partir de um modelo ja treinado.
   
## Fluxo
![alt text](https://i.imgur.com/Vf05NSa.jpg)

## Configuração do Ambiente
1. Executar o arquivo config/config.sh que fará a criação do container mongo3 com a imagem do MongoDB.
```./config/config.sh```
2. Editar a o arquivo config/export_env.sh com seus caminhos para as variaveis de ambiente e executar o arquivo.
```. ./config/export_env.sh```
3. Executar o arquivo database/insert_mongo.py para a injestão dos dados no MongoDB.
```python /database/insert_mongo.py```

## Execução
Excutar o arquivo <b>main.py</b> que fará a excução de todos os processos.

## MongoDB
Para acessar o Banco de Dados é só executar:
```docker exec -it mongo3 mongo``` 

O nome do banco em que os dados são salvos é <b>monsters</b>

As collections que estão no banco são:

* <b>train</b>: Dados de treino.
* <b>test</b>: Dados de teste.
* <b>target_map</b>: Dados para o mapeamento da label.
* <b>model</b>: Dados sobre o modelo: parametros, variaveis usadas.
* <b>results</b>: Resultado da classificação.

## API
Para iniciar o servidor da API é só executar o arquivo api/api.py
```python api.py```

exemplo query: http://127.0.0.1:5000/classify?id=1&list=0.38821714681781627,0.3826677466918563,0.8331249304393347,0.3049219006847556,0,0,1,0,0
