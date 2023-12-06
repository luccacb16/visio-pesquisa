from ultralytics import YOLO
import cv2
import time

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Ignorar warnings do TensorFlow sobre CUDA

from counter import *
from tracker import *
from video import *
from point import *

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
            
            self._linha = True
        else:
            self._linha = False
        
        self._out = cv2.VideoWriter(self._output_path, cv2.VideoWriter_fourcc(*'mp4v'), self._video.FPS, (self._video.WIDTH, self._video.HEIGHT))
        
    def process(self) -> None:
        '''
        Processa o vídeo, rastreando e contando objetos.
        '''
        # Inicia o contador de tempo
        start_time = time.time()
        
        while True:
            ret, frame = self._video.read()
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
        self.fps = self._video.TOTAL_FRAMES / self.time