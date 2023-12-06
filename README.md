# Contador de veículos




## Descrição
Através de uma fila do RabbitMQ, o programa recebe um arquivo JSON de keys
- video_ref: nome do arquivo de vídeo;
- op_type: operações que serão realizadas;
- frame_second_index: tempo de vídeo do qual o frame é extraído.

Em seguida extrai e processa o frame especificado

## Exemplos
<img src="https://gitlab.com/luccacb16/dataaugmentation/uploads/7d5c75eea85d77c0b363af6df787e9f6/2.jpg" height=250>

<img src="https://gitlab.com/luccacb16/dataaugmentation/uploads/07e002e53544ca705c52801bf426ed17/9.jpg" height=250>

<img src="https://gitlab.com/luccacb16/dataaugmentation/uploads/ba39e60150b961ce9ce34faacc0f1e6a/20.jpg" height=250>

## Setup
Clone o repositório para sua máquina
```
git clone https://github.com/luccacb16/visio-pesquisa.git
```

Acesse a raiz do projeto
```
cd visio-pesquisa
```

Instale as dependências
```
pip install -r requirements.txt
```

Versão do Python utilizado no projeto: 3.10.12

## Uso
Crie um arquivo .py e importe
```
from video import Video
from tracker import Tracker
from counter import Counter
from video_processor import VideoProcessor
```

Instancie um objeto dessa classe, passando os parâmetros host, port, username, password, queue 
```
augmenter = Augmenter(host, port, username, password, queue)
```

Chame a função .process() do objeto
```
augmenter.process()
```

As imagens serão salvas no diretório 'imgs/', que será criado automaticamente, caso não exista

Para um teste rápido, instale o software de mensageria por fila RabbitMQ, disponível no site <https://www.rabbitmq.com/>

**É importante que os vídeos estejam em uma pasta 'videos' no mesmo diretório do arquivo test.py**

Você pode executar o arquivo test.py, acessando o diretório 'src' do projeto e executando
```
py test.py
```
Os parâmetros de conexão com o RabbitMQ já estão definidos, mas você pode mudá-los. Basta abrir o arquivo test.py e fazer as alterações que desejar
