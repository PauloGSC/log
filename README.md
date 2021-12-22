# AT2: Log

- CCR: Banco de Dados II
- Acadêmico: Paulo Gabriel Sena Comasetto

## Requisitos de sistema

Assegure-se de que `python3` e `pip` estejam instalados.

É necessário possuir o SGBD `PostgreSQL` instalado.

Clone o repositório:

```shell
rm -rf log
git clone --depth 1 https://github.com/PauloGSC/log.git
cd log
```

## Requisitos de Python

O programa requer as bibliotecas listadas em `requirements.txt`.

Recomenda-se usar um ambiente virtual para instalar as bibliotecas.

Comandos para criar o ambiente e instalar as bibliotecas:

```shell
rm -rf .venv-log
python3 -m venv .venv-log
source .venv-log/bin/activate
python3 -m pip install -U pip
pip install -U setuptools wheel
pip install -r requirements.txt
deactivate
```

## Execução

- Ative o ambiente virtual criado anteriormente:

```shell
source .venv-log/bin/activate
```

- Posicione o arquivo de entrada dentro do diretório `entrada`

- Preferencialmente, crie um usuário de teste somente para rodar este programa,
com nome `postgres` e senha `postgres`.
Além disso, crie um novo banco de dados com o nome `log`

- Execute o programa com o comando abaixo (onde `<arquivo>` é o nome do arquivo):

```shell
python3 log.py entrada/<arquivo>
```

- É possível, ao invés disso, fornecer usuário, senha e banco de dados quaisquer;
todavia, será necessário explicitá-los ao executar o programa (`<banco>`, `<usuario>` e `<senha>` são, respectivamento, o banco, usuário e senha personalizados):

```shell
python3 log.py entrada/<arquivo> --banco <banco> --usuario <usuario> --senha <senha>
```

- Quando terminar de usar o programa, desative o ambiente virtual:

```shell
deactivate
```
