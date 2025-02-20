import sys
sys.path.append('ChartMoE')
from chartmoe import ChartMoE_Robot
import torch
from tqdm import tqdm


def generate_response(queries, model_path):

    robot = ChartMoE_Robot(model_path)

    for k in tqdm(queries):
        query = queries[k]['prompt']
        query = query.replace('<image>\n', '')
        image_path = queries[k]["image_path"]

        history = ""
        with torch.cuda.amp.autocast():
            response, history = robot.chat(image_path=image_path, question=query, history=history)

        queries[k]['response'] = response

    return queries