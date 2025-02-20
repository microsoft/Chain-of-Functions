import torch
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer
import os


def generate_response(queries, model_path):

    model_path = os.path.expanduser(model_path)

    tokenizer = AutoTokenizer.from_pretrained(
                                model_path,
                                trust_remote_code=True
                                )
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
        device_map="auto").eval()

    for k in queries:
        query = queries[k]['prompt']
        query = query.replace('<image>\n', '')
        query = f"Human:{query}"
        image_path = queries[k]["image_path"]
        image = Image.open(image_path).convert('RGB')

        input_by_model = model.build_conversation_input_ids(
                tokenizer,
                query=query,
                history=[],
                images=[image],
                template_version='chat'
            )

        inputs = {
            'input_ids': input_by_model['input_ids'].unsqueeze(0).to("cuda"),
            'token_type_ids': input_by_model['token_type_ids'].unsqueeze(0).to("cuda"),
            'attention_mask': input_by_model['attention_mask'].unsqueeze(0).to("cuda"),
            'images': [[input_by_model['images'][0].to("cuda").to(torch.bfloat16)]] if image is not None else None,
        }

        gen_kwargs = {
            "max_new_tokens": 4096,
            "pad_token_id": 128002,  
        }

        with torch.no_grad():
            outputs = model.generate(**inputs, **gen_kwargs)
            outputs = outputs[:, inputs['input_ids'].shape[1]:]
            response = tokenizer.decode(outputs[0])
            response = response.split("<|end_of_text|>")[0]
            print("\nCogVLM2:", response)

        queries[k]['response'] = response

    return queries