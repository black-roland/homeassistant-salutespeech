# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from custom_components.salutespeech.api.grpc import recognition_pb2 as custom__components_dot_salutespeech_dot_api_dot_grpc_dot_recognition__pb2


class SmartSpeechStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Recognize = channel.stream_stream(
                '/smartspeech.recognition.v2.SmartSpeech/Recognize',
                request_serializer=custom__components_dot_salutespeech_dot_api_dot_grpc_dot_recognition__pb2.RecognitionRequest.SerializeToString,
                response_deserializer=custom__components_dot_salutespeech_dot_api_dot_grpc_dot_recognition__pb2.RecognitionResponse.FromString,
                )


class SmartSpeechServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Recognize(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SmartSpeechServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Recognize': grpc.stream_stream_rpc_method_handler(
                    servicer.Recognize,
                    request_deserializer=custom__components_dot_salutespeech_dot_api_dot_grpc_dot_recognition__pb2.RecognitionRequest.FromString,
                    response_serializer=custom__components_dot_salutespeech_dot_api_dot_grpc_dot_recognition__pb2.RecognitionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'smartspeech.recognition.v2.SmartSpeech', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SmartSpeech(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Recognize(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/smartspeech.recognition.v2.SmartSpeech/Recognize',
            custom__components_dot_salutespeech_dot_api_dot_grpc_dot_recognition__pb2.RecognitionRequest.SerializeToString,
            custom__components_dot_salutespeech_dot_api_dot_grpc_dot_recognition__pb2.RecognitionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
