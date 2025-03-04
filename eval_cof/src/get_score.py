


import argparse
from typing import Optional
import json
import re




def relaxed_correctness(target: str,
                        prediction: str,
                        max_relative_change: float = 0.05) -> bool:
    """Calculates relaxed correctness.

    The correctness tolerates certain error ratio defined by max_relative_change.
    See https://arxiv.org/pdf/2203.10244.pdf, end of section 5.1:
    “Following Methani et al. (2020), we use a relaxed accuracy measure for the
    numeric answers to allow a minor inaccuracy that may result from the automatic
    data extraction process. We consider an answer to be correct if it is within
    5% of the gold answer. For non-numeric answers, we still need an exact match
    to consider an answer to be correct.”

    Args:
      target: Target string.
      prediction: Predicted string.
      max_relative_change: Maximum relative change.

    Returns:
      Whether the prediction was correct given the specified tolerance.
    """

    def _to_float(text: str) -> Optional[float]:
        try:
            if text.endswith('%'):
                # Convert percentages to floats.
                return float(text.rstrip('%')) / 100.0
            else:
                return float(text)
        except ValueError:
            return None

    prediction_float = _to_float(prediction)
    target_float = _to_float(target)
    if prediction_float is not None and target_float:
        relative_change = abs(prediction_float -
                              target_float) / abs(target_float)
        return relative_change <= max_relative_change
    else:
        return prediction.lower() == target.lower()

def extract_answer(answer):
    '''
    extract answer from response
    '''
    if 'Answer: ' in answer:
        answer = answer.split('Answer: ')[1]
        ### remove { and }
        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
    elif 'answer: ' in answer:
        answer = answer.split('answer: ')[1]
        ### remove { and }
        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
    return answer

def remove_unit(answer):
    '''
    Remove unit from answer
    If the answer is a float/int string with a unit (e.g., '0.1 ton'), remove the unit (e.g., ' ton')
    if unit (0.1 million tons), remove the unit (e.g., ' million tons')
    '''
    # Define a regular expression pattern to match a number followed by a unit
    # pattern = r'^(\d+(\.\d+)?)(\s*[a-zA-Z%]+)?$'
    pattern = r'^(\d+(\.\d+)?)(\s*[a-zA-Z%]+.*)?$'
    match = re.match(pattern, answer)
    if match:
        return match.group(1)  # Return the numeric part without the unit
    return answer  # Return the original answer if no unit is found

def evaluate_pred(pred, gt, task_type):
    '''
    task_type: 'Text' or 'NQA' or 'Binary'
    For NQA, allow 5% margin for numerical answers
    '''
    if task_type == 'Text' or task_type == 'Binary':
        return pred.lower() == gt.lower()
    elif task_type == 'NQA':
        return relaxed_correctness(gt, pred)
    else:
        raise ValueError(f'Invalid task type: {task_type}')
    
def get_score(response_path, output_score_path, original_json_path='chartcof.json'):
    '''
    {"id": 0, "question": "How many unique quarters are represented in the chart displaying the manufacturing financial performance and expense breakdown for 2023, which includes Net Manufacturing Revenue (in dark red), Direct Production Costs (in light green), and Indirect Operational Costs (in purple)?", "answer": "4", "rationale": "The chart presents the financial performance and expense breakdown for manufacturing in each quarter of 2023, showing Net Manufacturing Revenue (in dark red), Direct Production Costs (in light green), and Indirect Operational Costs (in purple). For 2023, the quarters Q1, Q2, Q3, and Q4 are distinctly represented, each with associated financial metrics. Given this breakdown, the number of unique quarters represented in the chart is 4. Final answer: 4", "image_path": "image/3D-Bar/3D-Bar_13_3.png", "step_num": 2, "chart_type": "3D-Bar", "annotation": 0.0, "original_json_path": "/home/v-zijianli/ml-dl/v-zijianli/data/data/ChartT/data/json/2024-12-8-test/3D-Bar_self_instructed_unused_sampled_200/3D-Bar_13_3.json", "original_image_path": "/home/v-zijianli/ml-dl/v-zijianli/data/data/ChartT/data/image/2024-12-8/3D-Bar_self_instructed/3D-Bar_13_3.png", "original_rationale_path": "/home/v-zijianli/ml-dl/v-zijianli/data/data/ChartT/data/json/2024-12-8-test/3D-Bar_self_instructed_unused_sampled_200_rationale_nl_reanswer_1/3D-Bar_13_3_rationale.jsonl", "function_list": "all_object_selection/num_of_arguments/", "task_type": "NQA", "response": "4", "prompt": "<image>\nHow many unique quarters are represented in the chart displaying the manufacturing financial performance and expense breakdown for 2023, which includes Net Manufacturing Revenue (in dark red), Direct Production Costs (in light green), and Indirect Operational Costs (in purple)?\nAnswer the question using a single word or phrase."}

    '''
    response_list = []
    with open(response_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            response_list.append(data)
    
    with open(original_json_path, 'r') as f:
        original_data_ = json.load(f)
        original_data = [original_data_[k] for k in original_data_]
    
    score_list = []
    correct = 0
    total = len(response_list)
    for i, response in enumerate(response_list):

        if 'extracted_answer' in response:
            pred = response['extracted_answer']
        elif 'response' in response:
            pred = response['response']
        else:
            raise ValueError('No extracted answer or response in the response data')

        pred = extract_answer(pred)
        gt = response['answer']
        if 'task_type' not in response:
            assert original_data[i]['question'] == response['question']
            task_type = original_data[i]['task_type']
            response['task_type'] = task_type
        else:
            task_type = response['task_type']
        gt_1 = gt
        if task_type == 'NQA' and gt.endswith('%'):
            gt_1 = gt.rstrip('%')
        
        ### remove the final . if exists
        pred = pred.rstrip('.')

        score = evaluate_pred(pred, gt, task_type) or evaluate_pred(pred, gt_1, task_type)
        score_data = response
        score_data['score'] = score
        score_list.append(score_data)

        if score:
            correct += 1
        else:
            print('pred:', pred, 'gt:', gt)

    assert len(score_list) == total
    accuracy = correct / total
    print(f'Accuracy: {accuracy}')
    with open(output_score_path, 'w') as f:
        for score_data in score_list:
            f.write(json.dumps(score_data) + '\n')




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--response_path', type=str, help='Path to the response jsonl file', required=True)
    args = parser.parse_args()

    output_score_path = args.response_path.replace('.jsonl', '_score.jsonl')
    get_score(args.response_path, output_score_path)