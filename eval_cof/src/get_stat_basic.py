import argparse
from typing import Optional
import json

TASK_TYPE = ['NQA', 'Text', 'Binary']
ANNOTATION = [True, False]
REG_TYPE = ['line_multi', 'line_single', 'bar_multi', 'bar_single', 'bar_stacked', 'pie_single']

def get_stat_basic(score_path, meta_path='chartcof.json'):
    '''
    {"id": 0, "question": "How many unique quarters are represented in the chart displaying the manufacturing financial performance and expense breakdown for 2023, which includes Net Manufacturing Revenue (in dark red), Direct Production Costs (in light green), and Indirect Operational Costs (in purple)?", "answer": "4", "rationale": "The chart presents the financial performance and expense breakdown for manufacturing in each quarter of 2023, showing Net Manufacturing Revenue (in dark red), Direct Production Costs (in light green), and Indirect Operational Costs (in purple). For 2023, the quarters Q1, Q2, Q3, and Q4 are distinctly represented, each with associated financial metrics. Given this breakdown, the number of unique quarters represented in the chart is 4. Final answer: 4", "image_path": "image/3D-Bar/3D-Bar_13_3.png", "step_num": 2, "chart_type": "3D-Bar", "annotation": 0.0, "original_json_path": "/home/v-zijianli/ml-dl/v-zijianli/data/data/ChartT/data/json/2024-12-8-test/3D-Bar_self_instructed_unused_sampled_200/3D-Bar_13_3.json", "original_image_path": "/home/v-zijianli/ml-dl/v-zijianli/data/data/ChartT/data/image/2024-12-8/3D-Bar_self_instructed/3D-Bar_13_3.png", "original_rationale_path": "/home/v-zijianli/ml-dl/v-zijianli/data/data/ChartT/data/json/2024-12-8-test/3D-Bar_self_instructed_unused_sampled_200_rationale_nl_reanswer_1/3D-Bar_13_3_rationale.jsonl", "function_list": "all_object_selection/num_of_arguments/", "task_type": "NQA", "response": "4", "prompt": "<image>\nHow many unique quarters are represented in the chart displaying the manufacturing financial performance and expense breakdown for 2023, which includes Net Manufacturing Revenue (in dark red), Direct Production Costs (in light green), and Indirect Operational Costs (in purple)?\nAnswer the question using a single word or phrase.", "score": true}
    '''

    output_path = score_path.replace(".jsonl", "_stat.txt")

    with open(score_path, 'r') as f:
        quries = [json.loads(line) for line in f]

    with open(meta_path, 'r') as f:
        meta_data = json.load(f)

    task_type_num = {}
    task_type_acc_num = {}
    annotation_num = {}
    annotation_acc_num = {}
    chart_type_num = {}
    chart_type_acc_num = {}
    overall_num = 0
    overall_acc_num = 0

    for k in range(len(quries)):
        task_type = quries[k]['task_type']
        # annotation = quries[k]['annotation']
        annotation = meta_data[str(k)]['annotation']
        chart_type = quries[k]['chart_type']
        score = quries[k]['score']

        overall_num += 1
        overall_acc_num += score

        if task_type not in task_type_num:
            task_type_num[task_type] = 0
            task_type_acc_num[task_type] = 0
        task_type_num[task_type] += 1
        task_type_acc_num[task_type] += score

        if annotation not in annotation_num:
            annotation_num[annotation] = 0
            annotation_acc_num[annotation] = 0
        annotation_num[annotation] += 1
        annotation_acc_num[annotation] += score

        if chart_type in REG_TYPE:
            chart_type = 'REG'
        else:
            chart_type = 'EXTRA'
        if chart_type not in chart_type_num:
            chart_type_num[chart_type] = 0
            chart_type_acc_num[chart_type] = 0
        chart_type_num[chart_type] += 1
        chart_type_acc_num[chart_type] += score


    task_type_acc = {k: task_type_acc_num[k] / task_type_num[k] for k in task_type_num}
    annotation_acc = {k: annotation_acc_num[k] / annotation_num[k] for k in annotation_num}
    chart_type_acc = {k: chart_type_acc_num[k] / chart_type_num[k] for k in chart_type_num}

    ### print all the results
    with open(output_path, 'w') as f:
        f.write(f'Task Type:\n')
        for k in task_type_num:
            f.write(f'{k}: Total {task_type_num[k]}, Accurate number {task_type_acc_num[k]}, Accuracy {task_type_acc[k]}\n')
        f.write(f'===========================================================================')
        f.write(f'\nAnnotation:\n')
        for k in annotation_num:
            f.write(f'{k}: Total {annotation_num[k]}, Accurate number {annotation_acc_num[k]}, Accuracy {annotation_acc[k]}\n')
        f.write(f'===========================================================================')
        f.write(f'\nChart Type:\n')
        for k in chart_type_num:
            f.write(f'{k}: Total {chart_type_num[k]}, Accurate number {chart_type_acc_num[k]}, Accuracy {chart_type_acc[k]}\n')
        f.write(f'===========================================================================')
        f.write(f'\nOverall:\n')
        f.write(f'Total {overall_num}, Accurate number {overall_acc_num}, Accuracy {overall_acc_num / overall_num}\n')




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--score_path', type=str, default='/home/v-zijianli/ml-dl/v-zijianli/chartagent_results/evaluate/qwen2VL_cof/cof_2_only_answer_score.jsonl')

    parser.add_argument('--score_path', type=str, default='/home/v-zijianli/Chain-of-Functions/results/chartcof_internvl25_8b_only_answer.jsonl')
    args = parser.parse_args()

    get_stat_basic(args.score_path)
