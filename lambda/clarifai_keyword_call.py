from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

# Your PAT (Personal Access Token) can be found in the portal under Authentification
PAT = 'f40cd9f14e1f44218ff433e6518a9e13'
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = 'openai'
APP_ID = 'chat-completion'
# Change these to whatever model and text URL you want to use
MODEL_ID = 'GPT-3_5-turbo'
MODEL_VERSION_ID = 'a82b2ece788e4dafac85ca6f8c8cd0f2'
RAW_TEXT = "Give me a maximum of 3 keywords from the following text separated by commas: "
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

metadata = (('authorization', 'Key ' + PAT),)

userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

class Keyword_giver:
    def __init__(self, input_str):
        self.input = input_str
    
    def get_keywords(self):
        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
                model_id=MODEL_ID,
                version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw= RAW_TEXT + self.input
                                # url=TEXT_FILE_URL
                                # raw=file_bytes
                            )
                        )
                    )
                ]
            ),
            metadata=metadata
        )

        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            return [] # just return an empty list

        # Since we have one input, one output will exist here
        output = post_model_outputs_response.outputs[0].data.text.raw
        li = list(output.split(", "))
        for item in li:
            if not item.isalpha()
                return [] #we only want one word and english alphabet letters only
        return li