
import torch
from transformers import AutoModel, AutoTokenizer
from tqdm import tqdm
import os

def generate_response(queries, model_path):

    model_path = os.path.expanduser(model_path)
    model = AutoModel.from_pretrained(
                model_path,
                torch_dtype=torch.bfloat16,
                trust_remote_code=True,
                device_map="auto").eval()

    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model.tokenizer = tokenizer

    for k in tqdm(queries):
        query = queries[k]['prompt']
        image_path = queries[k]["image_path"]
        image_list = [image_path]

        with torch.autocast(device_type='cuda', dtype=torch.float16):
            response, _ = model.chat(tokenizer, query, image_list, do_sample=False, max_new_tokens=4096)
        print(response)

        queries[k]['response'] = response

    return queries