# AT2: Log

- CCR: Banco de Dados II
- Acadêmico: Paulo Gabriel Sena Comasetto

## Requisitos de sistema

Assegure-se de que `python3` e `pip` estejam instalados.

É necessário possuir o SGBD `PostgreSQL` instalado.

Clone o repositório:

```shell
git clone --depth 1 https://github.com/PauloGSC/log.git
cd log
```

## Requisitos de Python

O programa requer as bibliotecas listadas em `requirements.txt`.

Recomenda-se usar um ambiente virtual para instalar as bibliotecas.

Configuração e uso de um ambiente virtual:

- Crie o ambiente virtual e instale alguns recursos básicos:

```shell
python3 -m venv .venv-log
source .venv-log/bin/activate
python3 -m pip install -U pip
pip install -U setuptools wheel
deactivate
```

- Ative o ambiente virtual:

```shell
source .venv-log/bin/activate
```

- Instale as bibliotecas requeridas:

```shell
pip install -r requirements.txt
```

## Execução

Posicione o arquivo de entrada dentro do diretório `entrada`.

Preferencialmente, crie um usuário de teste somente para rodar este programa,
com nome `postgres` e senha `postgres`.
Além disso, crie um novo banco de dados com o nome `log`.

Execute o programa com o comando abaixo (onde `<arquivo>` é o nome do arquivo):

```shell
python3 log.py entrada/<arquivo>
```

É possível, ao invés disso, fornecer usuário, senha e banco de dados quaisquer;
todavia, será necessário explicitá-los ao executar o programa (`<banco>`, `<usuario>` e `<senha>` são, respectivamento, o banco, usuário e senha personalizados):

```shell
python3 log.py entrada/<arquivo> --banco <banco> --usuario <usuario> --senha <senha>
```

## Desativando o ambiente virtual

Quando terminar de usar o programa, desative o ambiente virtual:

```shell
deactivate
```
