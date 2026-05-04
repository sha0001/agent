import sys 
import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions
from functions.call_function import call_function

#initializing API
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None: 
    raise RuntimeError ('Environment variable api_key not found')

client = genai.Client(api_key=api_key)

#parsing arguments

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt") 
parser.add_argument("--verbose", action ="store_true", help="Enable verbose output")
args = parser.parse_args()
#now we can access args.user_prompt

prompt = args.user_prompt

## define the user prompt with context 

messages  = [types.Content(role="user", parts=[types.Part(text=prompt)])]

##### Start the loop here#####

for _ in range(20): 

    # generate a response to the prompt, with access to a set list of functions. 
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents = messages ,
        config = types.GenerateContentConfig(
            system_instruction = system_prompt, 
            tools = [available_functions]
            ))

    # check for missing metadata
    if response.usage_metadata == None: 
        raise RuntimeError('missing usage_metadata - failed API request?')
    else: 

    # check the candidates property of the response: 
        if response.candidates != None: 
            if response.candidates != []: 
                candidates = response.candidates
        #append to messages 
                for candidate in candidates: 
                    messages.append(candidate.content)
            

    #checking for verbose flag 
        if args.verbose:

            #print verbose output text

            print(f'User prompt: {prompt}')

            print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}') 
            print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

        #create a list of function calls 
        function_calls = response.function_calls
        function_results = []

        if not function_calls : 
                
        #if the function call list is empty, just print the response
            print(f'Response: \n {response.text}')
            break
        else: 

            # call each function call in the list with a message. 
            for function_call in function_calls: 



                print(f'Calling function: {function_call.name}({function_call.args})')
                
                function_call_result = call_function(function_call,verbose = False)
    
                if not function_call_result.parts : 
                    raise Exception(f'function_call_result.parts is empty or None') 
                function_results.append(function_call_result.parts[0])
                
                
                if args.verbose: 
                    print(f"-> {function_call_result.parts[0].function_response.response}")


        #append the function results to messages
        messages.append(types.Content(role="user",parts = function_results))
# if we make it here, the max iterations has passed - break
else: 
    print('Loop maxxed out. Bailing') 
#sys call to exit with error code 1
    sys.exit(1)



