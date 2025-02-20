import torch
# from transformers import AutoModel, AutoTokenizer, AutoConfig
from tqdm import tqdm
import os
from PIL import Image
from modelscope import AutoModel, AutoTokenizer, AutoConfig

def generate_response(queries, model_path):

    model_path = os.path.expanduser(model_path)
    # model_path = 'iic/mPLUG-Owl3-2B-241101'
    config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
    print(config)
    model = AutoModel.from_pretrained(model_path, attn_implementation='flash_attention_2', torch_dtype=torch.bfloat16, trust_remote_code=True).eval().cuda()

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    processor = model.init_processor(tokenizer)

    for k in tqdm(queries):
        query = queries[k]['prompt']
        query = query.replace('<image>\n', '')
        image_path = queries[k]["image_path"]
        image = Image.open(image_path).convert('RGB')

        messages = [
            {"role": "user", "content": f"<|image|> {query}"},
            {"role": "assistant", "content": ""}
        ]

        inputs = processor(messages, images=[image], videos=None)

        inputs.to('cuda')
        inputs.update({
            'tokenizer': tokenizer,
            'max_new_tokens':100,
            'decode_text':True,
        })

        with torch.no_grad():
            response = model.generate(**inputs)
            print("\nMPLUG-Owl3:", response)
            queries[k]['response'] = response

    return queries