from toy_grpc_pb2_grpc import MediaServiceServicer, add_MediaServiceServicer_to_server
from toy_grpc_pb2 import MediaType, GetMediaByIdRequest, MediaResponse

import grpc
import concurrent.futures
import logging

class MediaService(MediaServiceServicer):
    def GetMediaById(self, request, context):
        if request.id == 1:
            return MediaResponse(id=1, title="The Hitchhiker's Guide to the Galaxy", type=MediaType.MEDIA_TYPE_BOOK)
        else:
            return MediaResponse(id=1)

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    add_MediaServiceServicer_to_server(MediaService(), server)
    server.add_insecure_port("localhost:3000")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()