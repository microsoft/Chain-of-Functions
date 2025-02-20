from transformers import AutoModel, AutoTokenizer
from tqdm import tqdm


def generate_response(queries, model_path):


    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True, use_fast=False, padding_side="right")
    model = AutoModel.from_pretrained(model_path, trust_remote_code=True, low_cpu_mem_usage=True, device_map='cuda')
    model = model.eval().cuda()

    for k in tqdm(queries):
        query = queries[k]['prompt']
        image_path = queries[k]["image_path"]

        res = model.chat(tokenizer, image_path, reliable_check=True)