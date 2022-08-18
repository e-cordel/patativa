## Configurando o ambiente do projeto


- Crie um ambiente virtual via venv do python
```
python3 -m venv venv

```

- Habilitar o ambiente virtual virtual 

```
source venv/bin/activate
```


## Configuração: URL Da API

No arquivo config.py setar a variável API_URL


## Configurar o .env com usuario e senha da api
- Setar o usuário e senha no ambiente
 ```
    $export `cat .env`
```

## rodar o main.py

    python main.py



# Utilizando um novo Repositório

Para criar um novo repositório de cordel, é necessário:
- Implementar a interface RepositoryInterface no arquivo repository_interface.py. 
- Substuir a instância desse novo repositório no [ main.py ](./main.py) na raiz do projeto

## Sobre a interface
A implementação da interface deve obrigatóriamente retornar uma lista dos cordeis no formato do objeto Cordel, com todos os atributos já preenchidos, inclusive o autor.