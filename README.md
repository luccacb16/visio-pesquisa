# Contador de veículos




## Descrição
O programa recebe um vídeo de uma rodovia e conta quantos veículos passaram por ela.

## Exemplos
<img src="./media/road_video001.gif" width="640" height="360" />

<img src="./media/road_video001_output.gif" width="640" height="360" />

<img src="./media/road_video001_output_linha.gif" width="640" height="360" />

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

Instancie um objeto de cada classe, passando os parâmetros necessários. Você pode também definir dois pontos para a linha de contagem.
```
video_path = 'dataset/road_video001.mp4'
output_path = 'outputs/road_video001.mp4'

video = Video(video_path)

tracker = Tracker('yolov8n.pt', classes=[2, 7], tracker='bytetrack.yaml')

counter = Counter()

start = (0, int(video.HEIGHT * 2/3))
end = (video.WIDTH, int(video.HEIGHT * 2/3))

video_processor = VideoProcessor(video, tracker, counter, 'outputs/road_video001_linha.mp4', start, end)
```

Chame a função .process() do objeto de VideoProcessor
```
video_processor.process()
```

Não passar os atributos 'start' e 'end' fará com que a contagem seja global, ou seja, todos os veículos que forem detectados serão contabilizados.

Um exemplo com esse código pode ser encontrado em /scripts/example.py. Basta mover o diretório dataset/ e o arquivo para o diretório src/ e executá-lo.
