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
#       easy display of results in those respective environments.

# NOTE: The interface of Acumos-wrapped models will change in the future.  Check back (or follow
#       developments at https://www.acumos.org/) to track version changes.  Additionally, for a sneak
#       of the new model runner, check out the already published pypi package 'python-model-runner'
#       (https://pypi.org/project/acumos-model-runner/), which already includes swagger and JSON compatibility.

## Model Score calls
# This quick function allows us to generically call a model with a set of inputs.  We provide
#       the model and input features and the system will either execute it locally or forward that
#       call to a remote url (if provided)
def score_model(wrapped_model, item_values=[], verbose=False, url_remote=None, version_legacy=True, name_function="classify"):
    if not version_legacy:
        print("This software does not currently support the non-legacy (e.g. v2) version of model encapsulation.")
        return None    
    
    obj_func = getattr(wrapped_model, name_function)
    if verbose:
        print(obj_func)
    TransIn = obj_func._input_type
    TransOutPb = obj_func.pb_output_type

    # start the clock for runtime ellapsed
    time_start = time.time()

    res_list = []
    for i in range(len(item_values)):
        x = item_values[i]
        trans_in = TransIn(*x)   # transform from raw dict/list item into format
        # print("----------- x -----------")
        # print(*x)
        # print("----------- trans_in -----------")
        # print(trans_in)

        # pack into protobuf message
        trans_in_pb = _pack_pb_msg(trans_in, obj_func._module)
        # print("----------- trans_in_pb -----------")
        # print(trans_in_pb)

        # save to protobuf bytes? if you wanted to send via direct HTTP request?
        trans_in_pb_bytes = trans_in_pb.SerializeToString()
        # trans_out_pb_bytes = trans_out_pb.SerializeToString()

        trans_in_dict = MessageToDict(trans_in_pb)
        if verbose and i==0:
            print(trans_in_dict)

        # trans_in_json = MessageToJson(trans_in_pb, indent=0)
        # trans_out_json = MessageToJson(trans_out_pb, indent=0)
        # if verbose and i==0:
        #      print(trans_in_dict)
        
        if url_remote is None:   # no where to go
            # print("----------- pb_msg -----------")
            # print(wrapped_model.classify.from_pb_msg)
            resp_wrap = obj_func.from_pb_msg(trans_in_pb)
            print(resp_wrap)
            dict_res = resp_wrap.as_dict()
            # print(resp)
        else:   # go to a remote URL
            resp = None
            # url = self.resolve_method(method_name)
            resp_data = requests.post("{}/{}".format(url_remote, name_function), data=trans_in_pb_bytes)
            resp_data.raise_for_status()
            # print("----------- from_pb_bytes -----------")
            # print(wrapped_model.classify.from_pb_bytes)
            resp = TransOutPb.FromString(resp_data.content)
            dict_res = MessageToDict(resp)
        res_list.append(dict_res)
        if (i % 250)==0 and i>0:
            print("Sample {}...".format(i))

    print("Evaluation time for {} items, {:0.3f} sec".format(len(item_values), time.time()-time_start))
    if verbose:
        print("---- Help and Input Type Description ----")
        print(help(TransIn))
    return res_list

# main/reusable function
def main(config={}):
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
        description='a wrapped model caller',
        epilog="Call to execute a single review sample or a textual sample \n" \
                "  (review)   python util_call.py -m data/model -u \"http://localhost:8884\"\n" \
                "    (text)   python util_call.py -t -m data/model2 -u \"http://localhost:8884\"\n ")
    submain = parser.add_argument_group('main execution and evaluation functionality')
    submain.add_argument('-m', '--model_path', type=str, default='data/model2b-review-text', help="path to dumped model (for protobuf definitions)")
    submain.add_argument('-u', '--url_host', type=str, default=None, help="URL to target model (without function url, e.g. http://localhost:8884)")
    submain.add_argument('-n', '--function_name', type=str, default='classify', help="name of primary function to execute")
    submain.add_argument('-t', '--text_only-only', dest='text_only', action='store_true', default=False, help='run a text-only dataframe')
    submain.add_argument('-v', '--version_updated', dest='version_updated', action='store_true', default=False, help='run in an updated model version')
    config.update(vars(parser.parse_args())) # pargs, unparsed = parser.parse_known_args()    
    
    # load model from disk, see that it is a nicely "wrapped" model
    wrapped_model = load_model(config['model_path'])
    print("----- Wrapped Model -------")
    print(wrapped_model)
    
    # create data frame
    if config['text_only']:
        X = [["I didn't like it much. It was such a rubbery item"]]
    else:
        X = [[[0,0], "I've had better", "not much", int(time.time()), ["office products"], "rubbery item"]]
    print("----- Dataframe -------")
    print(X)
        
    # score model with sample dataframe
    res_list = score_model(wrapped_model, X, config['version_updated'], config['url_host'], config['function_name']) #, )
    print("----- Result -------")
    print(res_list)
    
if __name__ == "__main__":
    # execute only if run as a script
    main()
   