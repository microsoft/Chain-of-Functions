
import os
import argparse
from gpt_extract_answer import generate_response
from tqdm import tqdm
import json


def extract_answer(quries):
    for k in tqdm(range(len(quries))):
        question = quries[k]['question']
        response = quries[k]['response']
        extracted_answer = generate_response(question, response)
        quries[k]['extracted_answer'] = extracted_answer
    return quries


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--response_path", type=str, required=True)

    args = parser.parse_args()

    output_path = args.response_path.replace(".jsonl", "_extracted_answer.jsonl")

    quries = []
    with open(args.response_path, "r") as f:
        for line in f:
            quries.append(json.loads(line))
    quries = extract_answer(quries)

    with open(output_path, "w") as f:
        for query in quries:
            f.write(json.dumps(query) + "\n")