# ===============LICENSE_START=======================================================
# Apache-2.0
# ===================================================================================
# Copyright (C) 2019 AT&T Intellectual Property  All rights reserved.
# ===================================================================================
# This software file is distributed by AT&T
# under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============LICENSE_END=========================================================

import requests
import time
from requests import ConnectionError
from acumos.wrapped import load_model, _pack_pb_msg
from google.protobuf.json_format import MessageToJson, MessageToDict


# What's the deal with this script!?

# When you want to re-use functionality, you can make a package, a library, or just another importable script. 
# We chose the latter solution here to keep it simple yet allow quick imports into other notebooks for 
# easy display of results in those respective environments.

## Model Score calls
# This quick function allows us to generically call a model with a set of inputs.  We provide
# the model and input features and the system will either execute it locally or forward that
# call to a remote url (if provided)
def score_model(wrapped_model, item_values=[], verbose=False, url_remote=None):
    if verbose:
        print(wrapped_model.classify)
    TransIn = wrapped_model.classify._input_type
    TransOut = wrapped_model.classify._output_type

    # start the clock for runtime ellapsed
    time_start = time.time()

    res_list = []
    for i in range(len(item_values)):
        x = item_values[i]
        trans_in = TransIn(*x)
        # trans_out = TransOut(*out)
        print(trans_in)

        # pack into protobuf message
        trans_in_pb = _pack_pb_msg(trans_in, wrapped_model.classify._module)
        # trans_out_pb = _pack_pb_msg(trans_out, wrapped_model.transform._module)

        # save to protobuf bytes? if you wanted to send via direct HTTP request?
        trans_in_pb_bytes = trans_in_pb.SerializeToString()
        # trans_out_pb_bytes = trans_out_pb.SerializeToString()

        trans_in_dict = MessageToDict(trans_in_pb)
        # trans_out_dict = MessageToDict(trans_out_pb)
        if verbose and i==0:
            print(trans_in_dict)

        # trans_in_json = MessageToJson(trans_in_pb, indent=0)
        # trans_out_json = MessageToJson(trans_out_pb, indent=0)
        # if verbose and i==0:
        #      print(trans_in_dict)
        
        print(wrapped_model.classify.from_pb_msg)
        if url_remote is None:   # no where to go
            resp = wrapped_model.classify.from_pb_msg(trans_in_pb)
        else:   # go to a remote URL
            resp = None
            # url = self.resolve_method(method_name)
            pb_output = method.pb_output_type()
            pb_output.ParseFromString(resp_data)
            resp = requests.post(url_remote, data=trans_in_pb_bytes)
            resp.raise_for_status()
        print(resp)

    print("Evaluation time for {} items, {:0.3f} sec".format(len(item_values), time.time()-time_start))
    if verbose:
        print("---- Help and Input Type Description ----")
        print(help(TransIn))
       