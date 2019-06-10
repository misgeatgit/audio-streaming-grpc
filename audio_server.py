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
           audio_chunk = audio_messages_pb2.AudioDataSeq()
           while byte != "":
               audio_chunk.audio.append(byte)
               if len(audio_chunk.audio) == 1024:
                   yield audio_chunk
                   global audio_chunk
                   audio_chunk = audio_messages_pb2.AudioDataSeq()
               byte = audio_data.read(1)
           
           if len(audio_chunk.audio) > 0:
               yield audio_chunk
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
