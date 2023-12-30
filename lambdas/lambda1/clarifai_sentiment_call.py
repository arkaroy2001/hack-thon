
######################################################################################################
# In this section, we set the user authentication, user and app ID, model details, and the URL of 
# the text we want as an input. Change these strings to run your own example.
######################################################################################################

# Your PAT (Personal Access Token) can be found in the portal under Authentification

# To use a hosted text file, assign the url variable
# TEXT_FILE_URL = 'https://samples.clarifai.com/negative_sentence_12.txt'
# Or, to use a local text file, assign the url variable
# TEXT_FILE_LOCATION = 'YOUR_TEXT_FILE_LOCATION_HERE'

############################################################################
# YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
############################################################################

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

PAT = '31a06969c8ef455fb2690ed7e0c76788'
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = 'clarifai'
APP_ID = 'main'
# Change these to whatever model and text URL you want to use
MODEL_ID = 'social-media-sentiment-english'
MODEL_VERSION_ID = 'fa9e29cb33f841b2832508cb41b30b44'


channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

metadata = (('authorization', 'Key ' + PAT),)

userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

# To use a local text file, uncomment the following lines
# with open(TEXT_FILE_LOCATION, "rb") as f:
#    file_bytes = f.read()
class Sentiment_giver:
    def __init__(self, input_arr):
        self.input_arr = []
        for curr_str in input_arr:
            self.input_arr.append(resources_pb2.Input(data=resources_pb2.Data(text=resources_pb2.Text(raw=curr_str))))


    #will return a list of vlaues from 0 to 1 [positive, neutral, negative]
    def get_sentiments(self):
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
            #print(post_model_outputs_response.status)
            #raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)
            return []

        # Since we have one input, one output will exist here
        output_arr = post_model_outputs_response.outputs

        retval = []
        for output in output_arr:    
            for c in output.data.concepts:
                if c.name == "positive":
                    pos = c.value
                elif c.name == "negative":
                    neg = c.value
            retval.append(pos - neg) #positive value minus negative value
        return retval