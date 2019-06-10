import time
from concurrent import futures
import grpc
import audio_messages_pb2_grpc
import audio_messages_pb2

class AudioStreamingServiceServicer(audio_messages_pb2_grpc.AudioStreamingServiceServicer):
   
    # Read audio file and send it here
    def GetAudioData(self, request, context):
       print "Sending bell-ringing-01.mp3"
       with open('bell-ringing-01.mp3', 'rb') as audio_data:
           byte = audio_data.read(1)
           while byte != "":
               audio_chunk = audio_messages_pb2.AudioData()
               audio_chunk.audio = byte
               yield audio_chunk
               byte = audio_data.read(1)
       print "Done."

def serve():
    server = grpc.server(futures.ThreadPoolExecutor( max_workers = 10))
    audio_messages_pb2_grpc.add_AudioStreamingServiceServicer_to_server( \
            AudioStreamingServiceServicer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    try:
        while True:
            time.sleep(24*60*60)
    except keyboardInterrupt:
        server.stop_server()


#if __name__ == '__main__':
serve()
