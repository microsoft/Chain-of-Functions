
### Follow ChartXiv

import time
from tqdm import tqdm


def generate_response_remote_wrapper(generate_fn, 
        queries, model_path,  init_sleep=1, 
        max_retries=10, sleep_factor=1.6, batch_size=1, start_idx=0):
    for k in tqdm(queries):
        # if float(k) < start_idx:
        #     continue
        sleep_time = init_sleep
        query = queries[k]['prompt']
        image = queries[k]["image_path"]
        curr_retries = 0
        result = None
        while curr_retries < max_retries and result is None:
            try:
                result = generate_fn(image, query, model_path)
            except Exception as e:
                print(f"Error: {e}")
                print(f"Error {curr_retries}, sleeping for {sleep_time} seconds...")
                time.sleep(sleep_time)
                curr_retries += 1
                sleep_time *= sleep_factor
        if result is None:
            result = "Error in generating response."
            print(f"Error in generating response for {k}")
        queries[k]['response'] = result
        print('query:', query)
        print('response:', result)

    return queries

def generate_response_local_wrapper(generate_fn, queries, model_path, batch_size=1):
    
    pass


def get_generate_fn(model_name):
    if 'gpt4o' in model_name:
        from .gpt4o_ms import generate_response
        return generate_response
    elif 'gpt4v' in model_name:
        from .gpt4v_ms import generate_response
        return generate_response
    elif 'gemini' in model_name:
        from .gpt_api import generate_response
        return generate_response
    elif 'qwen2vl' in model_name:
        from .qwen2vl import generate_response
        return generate_response
    elif 'internvl25' in model_name:
        from .internvl25 import generate_response
        return generate_response
    elif 'llava16' in model_name:
        from .llava16 import generate_response
        return generate_response
    elif 'internlm_xcomposer25' in model_name:
        from .internlm_xcomposer25 import generate_response
        return generate_response
    elif 'cogvlm2' in model_name:
        from .cogvlm2 import generate_response
        return generate_response
    elif 'mplug_owl3' in model_name:
        from .mplug_owl3 import generate_response
        return generate_response
    elif 'deepseek_vl2' in model_name:
        from .deepseekvl2 import generate_response
        return generate_response
    elif 'chartmoe' in model_name:
        from .chartmoe import generate_response
        return generate_response
    elif 'chartllama' in model_name:
        from .chartllama import generate_response
        return generate_response
    elif 'chartinstruct' in model_name:
        from .chartinstruct import generate_response
        return generate_response
    elif 'chartgemma' in model_name:
        from .chartgemma import generate_response
        return generate_response
    elif 'chartvlm' in model_name:
        from .chartvlm import generate_response
        return generate_response
    elif 'tinychart' in model_name:
        from .tinychart import generate_response
        return generate_response
    else:
        raise ValueError(f"Model {model_name} not supported.")