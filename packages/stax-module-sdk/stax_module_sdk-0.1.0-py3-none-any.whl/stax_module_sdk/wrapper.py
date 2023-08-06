# See LICENSE.md file in project root directory

import os
import json
import shutil
import signal
import traceback
from datetime import datetime
from retry_requests import retry

from .Stax import Stax

sess = retry()

def log(*args):
    print("[" + str(datetime.now()) + "]", *args)

def result(obj):
    with open('response.json', 'w') as f:
        json.dump(obj, f)

# Define module wrapper decorator
def def_module(module_id:str, module_key:str):
    def wrapper(app):
        def inner(*args, **kwargs):
            TEST = "test" in kwargs and kwargs["test"]

            # Setup keyboard interrupt handler (if worker is killed)
            signal.signal(signal.SIGINT, signal.default_int_handler)

            # Load request.json file
            if not os.path.exists('request.json'):
                raise Exception("Missing request.json file.")

            with open('request.json') as f:
                req = json.load(f)

            try:
                job:str = req["jobId"]
                team:str = req["teamId"]
                document:str = req["documentId"]
                stack:str = req["stackId"]
                step:str = req["stepId"]
                stepN:str = req["step"]
                config:list[dict] = req["config"]

            except:
                raise Exception("Missing required fields in request.json.")

            # Step identifier to report status to the Stax.ai API
            report = {
                "step": stepN,
                "stepId": step,
                "stack": stack,
            }

            # Instantiate a Stax.ai API object
            stax = Stax(
                module_id=module_id,
                module_key=module_key,
                team_id=team,
                document=document,
                api_url=os.getenv('STAX_API_URL', default='https://api.stax.ai')
            )

            try:
                # Create tmp working directory
                if not os.path.exists('./tmp'):
                    os.mkdir('./tmp')

                log("Started job:", job)
                
                # Call module/app function
                count = app(stax, document, stack, team, config)

                # Finished job, post result to Stax.ai API
                result({ "status": "Complete", "units": count })
                if not TEST:
                    stax.post('/job/complete/' + job, {
                        **report,
                        "count": count
                    })

                log("Completed job:", job)

            except KeyboardInterrupt:
                log("SIGINT Received. Stopping job:", job)
                result({ "status": "Killed" })

                # Let the Stax.ai API know what happened so it can handle it
                if not TEST:
                    stax.post('/job/complete/' + job, {
                        **report,
                        "error": "Automate module worker was stopped. This job should be retried shortly."
                    })

                exit()

            except Exception as e:
                log("Error in job:", job)
                trace = traceback.format_exc()
                print(trace)

                error = {
                    "error": str(e),
                    "traceback": str(trace)
                }
                result({ "status": "Error", **error })

                # Report error to the Stax.ai API
                if not TEST:
                    stax.post('/job/complete/' + job, {
                        **report,
                        **error
                    })

            finally:
                # Delete tmp working directory
                if os.path.exists('./tmp'):
                    shutil.rmtree('./tmp')

        return inner
    return wrapper