import torch
from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration
from tqdm import tqdm
from PIL import Image
import os


def generate_response(queries, model_path):

    model_path = os.path.expanduser(model_path)
    processor = LlavaNextProcessor.from_pretrained(model_path)
    model = LlavaNextForConditionalGeneration.from_pretrained(model_path, 
        torch_dtype=torch.float16, low_cpu_mem_usage=True).to('cuda:0').eval()

    if 'llava-v1.6-mistral-7b' in model_path:
        max_tokens, prompt_prefix = 4096, "[/INST]"
    # elif 'llava-v1.6-34b-hf' in model_path:
    #     max_tokens, prompt_prefix = 100, "<|im_start|> assistant"
    else:
        raise ValueError(f"Model {model_path} not supported.")
    
    for k in tqdm(queries):
        query = queries[k]['prompt']
        image_path = queries[k]["image_path"]
        image = Image.open(image_path)
        if 'llava-v1.6-mistral-7b' in model_path:
            prompt = f"[INST] {query} [/INST]"
        # elif 'llava-v1.6-34b-hf' in model_path:
        #     prompt = f"<|im_start|>system\nAnswer the questions.<|im_end|><|im_start|>user\n<image>\n{queries[k]['question']}<|im_end|><|im_start|>assistant\n"
        else:
            raise ValueError(f"Model {model_path} not supported.")
        
        question = query.replace('<image>\n', '')
        
        conversation = [
            {

            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {"type": "image"},
                ],
            },
        ]

        try:
            prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
            inputs = processor(images=image, text=prompt, return_tensors="pt").to("cuda:0")
            output = model.generate(**inputs, max_new_tokens=500, do_sample=False)
            response = processor.decode(output[0], skip_special_tokens=True)
            response = response.split(prompt_prefix)[1].strip() # remove the prompt
        except:
            response = "Generation Error"

    
        # try:
        #     inputs = processor(prompt, image, return_tensors="pt").to("cuda:0")
        #     output = model.generate(**inputs, max_new_tokens=max_tokens, do_sample=False)
        #     response = processor.decode(output[0], skip_special_tokens=True)
        #     response = response.split(prompt_prefix)[1].strip() # remove the prompt
        # except:
        #     response = "Generation Error"
        queries[k]['response'] = response

    return queries