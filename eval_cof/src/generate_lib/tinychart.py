import sys
sys.path.append('/scratch/amlt_code/')
from tinychart.model.builder import load_pretrained_model
from tinychart.mm_utils import get_model_name_from_path
from tinychart.eval.run_tiny_chart import inference_model
from tinychart.eval.eval_metric import parse_model_output, evaluate_cmds
from PIL import Image
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration
import torch
from tqdm import tqdm


def generate_response(queries, model_path):
    # Load Model
    # model = PaliGemmaForConditionalGeneration.from_pretrained(model_path, torch_dtype=torch.float16)
    # processor = AutoProcessor.from_pretrained(model_path)

    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # model = model.to(device)

    # model_path = "mPLUG/TinyChart-3B-768"
    tokenizer, model, image_processor, context_len = load_pretrained_model(
        model_path, 
        model_base=None,
        model_name=get_model_name_from_path(model_path),
        device="cuda"
    )

    for k in tqdm(queries):
        image_path = queries[k]['image_path']
        input_text = queries[k]['prompt'].replace('<image>\n', '')


        response = inference_model([image_path], input_text, model, tokenizer, image_processor, context_len, conv_mode="phi", max_new_tokens=1024)

        # Process Inputs
        # image = Image.open(image_path).convert('RGB')
        # inputs = processor(text=input_text, images=image, return_tensors="pt")
        # prompt_length = inputs['input_ids'].shape[1]
        # inputs = {k: v.to(device) for k, v in inputs.items()}

        # # Generate
        # generate_ids = model.generate(**inputs, num_beams=4, max_new_tokens=512)
        # output_text = processor.batch_decode(generate_ids[:, prompt_length:], skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        queries[k]['response'] = response

    return queries

