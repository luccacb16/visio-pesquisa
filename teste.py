# YOLOv8
import ultralytics
from ultralytics import YOLO

import numpy as np
import cv2
import torch
import torch.backends.cudnn as cudnn

import supervision as sv

from collections import defaultdict

print('CUDA disponível' if torch.cuda.is_available() else 'CUDA indisponível')
print(f'Ultralytics: {ultralytics.__version__}')
print(f'Torch: {torch.__version__}')
print(f'supervision: {sv.__version__}')

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(device)

# Carregando o modelo pré-treinado
model = YOLO('yolov8n.pt')
model.fuse()

# Selecionando apenas as classes relevantes pro problema
classes = [2, 7]

# Carrega o vídeo
VIDEO = './dataset/road_video001.mp4'
OUTPUT = 'output_video.mp4'

video_info = sv.VideoInfo.from_video_path(VIDEO)
print(video_info)

# Linha para contagem de carros
START = sv.Point(0, 2*video_info.height//3)
END = sv.Point(video_info.width, 2*video_info.height//3)

carros = 0

# Annotators
line_zone = sv.LineZone(START, END)
line_annotator = sv.LineZoneAnnotator(thickness=2, text_thickness=2, text_scale=1)

box_annotator = sv.BoxAnnotator(thickness=1, text_thickness=1, text_scale=0.5)

byte_tracker = sv.ByteTrack(track_thresh=0.25, track_buffer=30, match_thresh=0.8, frame_rate=video_info.fps)

def callback(frame: np.ndarray, index:int) -> np.ndarray:
    results = model(frame, verbose=False)[0]
        
    detections = sv.Detections.from_ultralytics(results)
    detections = detections[np.isin(detections.class_id, classes)]
    detections = byte_tracker.update_with_detections(detections)
    
    labels = [
        f'#{tracker_id} {model.model.names[class_id]} {confidence:.2f}'
        for _, _, confidence, class_id, tracker_id in detections
    ]
    
    annotated_frame = box_annotator.annotate(
        scene=frame.copy(),
        detections=detections,
        labels=labels
    )
        
    line_zone.trigger(detections)
        
    return line_annotator.annotate(annotated_frame, line_counter=line_zone)

# Processar cafa frame, visualizar e montar o vídeo
with sv.VideoSink(target_path=OUTPUT, video_info=video_info) as sink:
    for frame, index in enumerate(sv.get_video_frames_generator(source_path=VIDEO)):
        annotated_frame = callback(frame, index)
        sink.write_frame(frame=annotated_frame)
        
        # Mostra o vídeo
        cv2.imshow('frame', annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
cv2.destroyAllWindows()

# Contagem dos carros
carros = line_zone.in_count + line_zone.out_count
print(f'Carros: {carros}')