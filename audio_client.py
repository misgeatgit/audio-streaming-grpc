import grpc
import audio_messages_pb2_grpc
import audio_messages_pb2
import sys


channel = grpc.insecure_channel('localhost:50051')
stub = audio_messages_pb2_grpc.AudioStreamingServiceStub(channel)

audio_info = audio_messages_pb2.AudioInfo()
audio_info.id = 232
for audio_chunk in stub.GetAudioData(audio_info):
    # This how you print on stdout withou any newline or space
    for byte in audio_chunk.audio:
        sys.stdout.write(byte)
