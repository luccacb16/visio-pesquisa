import cv2

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
        self.TOTAL_FRAMES = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
    def read(self) -> tuple:
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