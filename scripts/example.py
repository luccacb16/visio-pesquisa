from video import Video
from tracker import Tracker
from counter import Counter
from video_processor import VideoProcessor

if __name__ == '__main__':
    video_path = 'dataset/road_video001.mp4'
    output_path = 'outputs/road_video001.mp4'
    
    # Carrega o vídeo
    video = Video(video_path)
        
    # Carrega o modelo e seleciona as classes
    tracker = Tracker('yolov8n.pt', classes=[2, 7], tracker='bytetrack.yaml')
    
    # Inicializa o contador
    counter = Counter()
    
    # Define a linha de contagem
    start = (0, int(video.HEIGHT * 2/3))
    end = (video.WIDTH, int(video.HEIGHT * 2/3))
    
    '''
    # Processa um vídeo
    video_processor = VideoProcessor(video, tracker, counter, 'outputs/road_video001_linha.mp4', start, end)
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
        print(f'Frames processados por segundo: {video_processor.fps:.2f}')
        print(f'Resultado salvo em {output_path}')