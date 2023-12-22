from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

# Your PAT (Personal Access Token) can be found in the portal under Authentification
PAT = '31a06969c8ef455fb2690ed7e0c76788'
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = 'openai'
APP_ID = 'chat-completion'
# Change these to whatever model and text URL you want to use
MODEL_ID = 'GPT-3_5-turbo'
MODEL_VERSION_ID = 'a82b2ece788e4dafac85ca6f8c8cd0f2'
RAW_TEXT = "Give me one a one-word category for the following news title: "
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

metadata = (('authorization', 'Key ' + PAT),)

userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

class Keyword_giver:
    def __init__(self, input_arr):
        self.input_arr = []
        for i in input_arr:
            self.input_arr.append(
                resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=RAW_TEXT + i
                            )
                        )
                    )
            )

    
    def get_keywords(self):
        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
                model_id=MODEL_ID,
                version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
                inputs=self.input_arr
            ),
            metadata=metadata
        )

        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            return []

        output_arr = post_model_outputs_response.outputs
        retval = []
        for output in output_arr:
            raw = output.data.text.raw
            if raw.isalpha():
                retval.append(raw)
            else:
                retval.append("")
        return retval