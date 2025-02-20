
import os
import json

REMOTE_MODEL = [
    'gpt4o'
]


def transfer_jsonl_to_dict(jsonl_path):
    data = {}
    with open(jsonl_path, 'r') as f:
        for line in f:
            d = json.loads(line)
            if "image" in d:
                d['image_path'] = d.pop('image')
            data[d['question_id']] = d
    return data

def build_queries(data, image_dir, model_type, input_option='only_answer'):
    '''
    data = {
                "question_id": index,
                "prompt": prompt,
                "figure_path": image_path,
                "response": output_text,
                "answer": row["answer"], 
                "answer_id": ans_id,
                "model_id": model_path,
            }
    '''
    queries = {}
    for index, d in data.items():
        image_path = os.path.join(image_dir, f"{d['image_path']}")
        question = d['question']
        if model_type in REMOTE_MODEL:
            if input_option == 'only_answer':
                prompt = f"{question}\nAnswer the question using a single word, number, or phrase."
            elif input_option == 'cot':
                prompt = f"{question}\nThink step by step to generate the rationales, and then answer the question using a single word, number, or phrase. The putput format is Rationale: rationale\nAnswer: answer"
            else:
                raise ValueError(f"Invalid input_option: {input_option}")
        
        else:
            if input_option == 'only_answer':
                prompt = f"<image>\n{question}\nAnswer the question using a single word or phrase."
            elif input_option == 'cot':
                prompt = f"<image>\n{question}\nThink step by step to generate the rationales, and then answer the question using a single word or phrase. The putput format is Rationale: rationale\nAnswer: answer"
            else:
                raise ValueError(f"Invalid input_option: {input_option}")
        query = d
        query['prompt'] = prompt
        query['image_path'] = image_path
        queries[index] = query
    return queries