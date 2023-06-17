## Configurando o ambiente do projeto


- Requisitos
    - Python 3.11
    - Pip
    - Virtualenv
    - tesseract-ocr
    - selenium (webdriver) v 0.33, disponivel neste link  https://selenium-python.readthedocs.io/installation.html#drivers
        - neste projeto utilizamos o firefox.



# 
- Crie um ambiente virtual via venv do python
```
python3 -m venv venv

```

- Habilitar o ambiente virtual virtual 

```
source venv/bin/activate
```

- Se você estiver utilizando o windows, o comando para habilitar o ambiente virtual é diferente

```
venv\Scripts\activate.bat
```

- Instalar as dependências do projeto

```
pip install -r requirements.txt
```



## Configuração: URL Da API

No arquivo config.py setar a variável API_URL


## Configurar o .env com usuario e senha da api

- Renomeie o arquivo .env-template para .env
 ```
    $mv .env-template .env
```
- Abra o arquivo e preencha os campos com o usuário e senha da API


- Setar o usuário e senha nas variáveis de ambiente
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