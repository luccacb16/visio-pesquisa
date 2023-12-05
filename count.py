# Imports necessários
from ultralytics import YOLO
import cv2
import time

# Misc
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Ignorar warnings do TensorFlow sobre CUDA

class Point:
    '''
    Representa um ponto.

    Args:
        - x (int): Coordenada x do ponto.
        - y (int): Coordenada y do ponto.
    '''
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        
class Video:
    '''
    Carrega e gerencia o fluxo de vídeo a partir de um caminho de arquivo.

    Args:
        - video_path (str): Caminho para o arquivo de vídeo.
    '''
    def __init__(self, video_path: str):
        self._cap = cv2.VideoCapture(video_path)
        
        self.WIDTH = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.HEIGHT = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.FPS = int(self._cap.get(cv2.CAP_PROP_FPS))
        
    def read_frame(self) -> tuple:
        '''
        Lê o próximo frame do vídeo.

        Returns:
            - Tuple[bool, cv2.Mat]: Flag de sucesso e o frame do vídeo.
        '''
        return self._cap.read()
    
    def release(self) -> None:
        '''
        Libera o recurso de vídeo.
        '''
        self._cap.release()

class Counter:
    '''
    Conta e mantém um registro dos objetos únicos identificados.
    '''
    def __init__(self):
        self.count = 0
        self.counter = set()
        
    def add(self, id: int) -> None:
        '''
        Adiciona um novo objeto à contagem.

        Args:
            - id (int): Identificador único do objeto.
        '''
        self.counter.add(id)
        self.count = len(self.counter)
            
class Tracker:
    '''
    Utiliza o modelo YOLO para rastrear objetos em frames de um vídeo.

    Args:
        - model (YOLO): Modelo YOLO para detecção e rastreamento de objetos.
        - tracker (str): Caminho para o arquivo de configuração do tracker.
        - classes (list): Lista de classes a serem rastreadas.
    '''
    def __init__(self, model: YOLO, classes: list, tracker: str = 'bytetrack.yaml'):
        self._model = model
        self._tracker = tracker
        self._classes = classes
        
    def track(self, frame: cv2.Mat, verbose: bool = False) -> object:
        '''
        Rastreia objetos no frame passado.

        Args:
            - frame (cv2.Mat): Frame de vídeo a ser processado.
            - verbose (bool): Verbosidade: a cada frame exibe informações sobre a detecção.

        Returns:
            - Resultado do rastreamento.
        '''        
        return self._model.track(frame, classes=self._classes, persist=True, tracker=self._tracker, verbose=verbose)
    
class VideoProcessor:
    '''
    Rastrea e conta objetos em um frame.
    Não passar os argumentos start e end resulta em contagem global.

    Args:
        - video (Video): Instância da classe Video.
        - tracker (Tracker): Instância da classe Tracker.
        - counter (Counter): Instância da classe Counter.
        - output_path (str): Caminho para salvar o vídeo processado.
        - start (Tuple[int, int]): Ponto inicial da linha de contagem.
        - end (Tuple[int, int]): Ponto final da linha de contagem.
    '''
    def __init__(self, video: Video, tracker: Tracker, counter: Counter, output_path: str, start: tuple = None, end: tuple = None):
        self._video = video
        self._tracker = tracker
        self._counter = counter
        self._output_path = output_path
        
        if start is not None and end is not None:
            self._start = Point(start[0], start[1])
            self._end = Point(end[0], end[1])
        
        self._linha = start is not None and end is not None
        
        self._out = cv2.VideoWriter(self._output_path, cv2.VideoWriter_fourcc(*'mp4v'), self._video.FPS, (self._video.WIDTH, self._video.HEIGHT))
        
    def process(self) -> None:
        '''
        Processa o vídeo, rastreando e contando objetos.
        '''
        # Inicia o contador de tempo
        start_time = time.time()
        
        while True:
            ret, frame = self._video.read_frame()
            if not ret: break

            results = self._tracker.track(frame, verbose=False)
            
            if results[0].boxes.id is not None:
                boxes = results[0].boxes.xywh.cpu()
                tracks_ids = results[0].boxes.id.int().cpu().tolist()
                
                annotated_frame = results[0].plot()
                                        
                for box, track_id in zip(boxes, tracks_ids):
                    x, y, w, h = box
                    cv2.rectangle(annotated_frame, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 2)
                    
                    if self._linha:
                        if self._start.x < x < self._end.x and abs(y - self._start.y) < 5:
                            self._counter.add(track_id)
                    else:
                        self._counter.add(track_id)
        
            if self._linha:  
                cv2.line(annotated_frame, (self._start.x, self._start.y), (self._end.x, self._end.y), (0, 0, 255), 2)
            
            cv2.putText(annotated_frame, f'Veiculos: {self._counter.count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            self._out.write(annotated_frame)

        self._video.release()
        self._out.release()
        
        self.time = time.time() - start_time
            
if __name__ == '__main__':
    video_path = 'dataset/road_video001.mp4'
    output_path = 'outputs/solid.mp4'
    
    # Carrega o vídeo
    video = Video(video_path)
        
    # Carrega o modelo e seleciona as classes
    tracker = Tracker(YOLO('yolov8n.pt'), classes=[2, 7], tracker='bytetrack.yaml')
    
    # Inicializa o contador
    counter = Counter()
    
    # Define a linha de contagem
    start = (0, int(video.WIDTH * 2/3))
    end = (video.WIDTH, int(video.HEIGHT * 2/3))
    
    '''
    # Processa um vídeo
    video_processor = VideoProcessor(video, tracker, counter, output_path) # Não passando start e end para obter a contagem global
    video_processor.process()
    '''
    
    # Processando múltiplos vídeos    
    for i in range(1, 6):
        video_path = f'dataset/road_video00{i}.mp4'
        output_path = f'outputs/road_video00{i}.mp4'
        
        # Inicializa o contador
        counter = Counter()
        
        # Processa o vídeo
        video_processor = VideoProcessor(Video(video_path), tracker, counter, output_path)
        video_processor.process()
        
        # Benchmark
        print(f'\n{video_path} - {counter.count} veículos detectados em {video_processor.time:.2f} segundos.')
        print(f'Resultado salvo em {output_path}')