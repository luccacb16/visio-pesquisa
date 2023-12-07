from ultralytics import YOLO
import cv2

class Tracker:
    '''
    Utiliza o modelo YOLO para rastrear objetos em frames de um vídeo.

    Args:
        - model (str): Caminho para o modelo YOLO para detecção e rastreamento de objetos.
        - tracker (str): Caminho para o arquivo de configuração do tracker.
        - classes (list): Lista de classes a serem rastreadas.
    '''
    def __init__(self, model: str, classes: list, tracker: str = 'bytetrack.yaml'):
        self._model = YOLO(model)
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