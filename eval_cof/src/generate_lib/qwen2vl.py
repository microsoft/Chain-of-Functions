import argparse
import os
import pandas as pd
from PIL import Image
import torch
import torchvision.transforms as T
from torchvision.transforms.functional import InterpolationMode
import json
import shortuuid
from tqdm import tqdm
from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info


def generate_response(queries, model_path):
    model_path = os.path.expanduser(model_path)
    model = Qwen2VLForConditionalGeneration.from_pretrained(
                model_path, 
                torch_dtype=torch.bfloat16,
                low_cpu_mem_usage=True,
                attn_implementation="flash_attention_2",
                trust_remote_code=True,
                device_map="auto").eval()
    processor = AutoProcessor.from_pretrained(model_path)

    for k in tqdm(queries):
        # if float(k) < start_idx:
        #     continue
        query = queries[k]['prompt']
        image = queries[k]["image_path"]

        message = [ {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": [
                            {"type": "image", "image": image},
                            {"type": "text", "text": query},
                        ],
                    }
                ]
        
        message_batch = [message]
        texts = [
                processor.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
                for msg in message_batch
            ]
        
        image_inputs, video_inputs = process_vision_info(message_batch)
        inputs = processor(
            text=texts,
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to("cuda")

        with torch.no_grad():
            do_sample = False
            generated_ids = model.generate(**inputs, max_new_tokens=4096, do_sample=do_sample)
            generated_ids_trimmed = [
                out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]
            output_text_batch = processor.batch_decode(
                generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )

            queries[k]['response'] = output_text_batch[0]

    return queries

def main(model_path, query, image_path):
    '''
    one query, one image
    '''
    model_path = os.path.expanduser(model_path)
    model = Qwen2VLForConditionalGeneration.from_pretrained(
                model_path, 
                torch_dtype=torch.bfloat16,
                low_cpu_mem_usage=True,
                attn_implementation="flash_attention_2",
                trust_remote_code=True,
                device_map="auto").eval()

    processor = AutoProcessor.from_pretrained(model_path)

    message = [ {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image_path},
                        {"type": "text", "text": query},
                    ],
                }
            ]
    
    message_batch = [message]

    texts = [
            processor.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
            for msg in message_batch
        ]
    
    image_inputs, video_inputs = process_vision_info(message_batch)

    inputs = processor(
        text=texts,
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )

    inputs = inputs.to("cuda")

    with torch.no_grad():
        do_sample = False
        generated_ids = model.generate(**inputs, max_new_tokens=4096, do_sample=do_sample)
        generated_ids_trimmed = [
            out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text_batch = processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )

    return output_text_batch[0]

if __name__ == "__main__":

    query = "Is (0.6A, 75V) within this area?"

    image_path = '/home/v-zijianli/chartagent/image.png'

    model_path = '/home/v-zijianli/ml-dl/v-zijianli/models/Qwen2-VL-7B-Instruct'

    print(main(model_path, query, image_path))
    

