import argparse
import os
import pandas as pd
from PIL import Image
import torch
import torchvision.transforms as T
from torchvision.transforms.functional import InterpolationMode
import json
# import shortuuid
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel
from query_utils import build_queries, transfer_jsonl_to_dict
from generate_lib.utils import get_generate_fn, generate_response_remote_wrapper


if __name__ == '__main__':
    # Creating the parser

    parser = argparse.ArgumentParser(description='Process a directory path.')
    parser.add_argument("--model_path", type=str, help="the path to the model", required=True)
    parser.add_argument("--model_name", type=str, default="internvl25")
    parser.add_argument("--model_base", type=str, default=None)
    parser.add_argument('--directory', type=str, help='The path to the directory', default='./')
    parser.add_argument("--question_path", type=str, default="./chartcof.json")
    parser.add_argument("--answers_path", type=str, default="./results/chartcof_internvl25_8b_only_answer.jsonl")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--top_p", type=float, default=1.0)
    parser.add_argument("--num_beams", type=int, default=1)
    parser.add_argument("--input_option", type=str, default='only_answer')
    parser.add_argument("--batch_size", type=int, default=4)

    # Parsing the arguments
    args = parser.parse_args()

    if os.path.dirname(args.answers_path):
        os.makedirs(os.path.dirname(args.answers_path), exist_ok=True)

    ### if question_path is a jsonl file
    if args.question_path.endswith('.jsonl'):
        data = transfer_jsonl_to_dict(args.question_path)
    else:
        with open (args.question_path, 'r') as f:
            data = json.load(f)

    queries = build_queries(data, args.directory, args.model_path, input_option=args.input_option)

    generate_fn = get_generate_fn(args.model_name)
    if 'gpt4o' in args.model_name or 'gpt4v' in args.model_name or 'gemini' in args.model_name:
        queries_with_output = generate_response_remote_wrapper(generate_fn, queries, model_path=args.model_path)
    else:
        if args.model_base is not None:
            queries_with_output = generate_fn(queries, args.model_path, model_base = args.model_base)
        else:
            queries_with_output = generate_fn(queries, args.model_path)

    with open(args.answers_path, 'a') as f:
        for _, data in queries_with_output.items():
            f.write(json.dumps(data) + '\n')