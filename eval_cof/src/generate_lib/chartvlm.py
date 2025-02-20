import sys
sys.path.append('/home/v-zijianli/chartagent/')
sys.path.append('/scratch/amlt_code/')
from ChartVLM.tools.ChartVLM import infer_ChartVLM
from tqdm import tqdm

def generate_response(queries, model_path):

    for k in tqdm(queries):
        query = queries[k]['prompt']
        image_path = queries[k]["image_path"]

        result = infer_ChartVLM(image_path, query, model_path)
        queries[k]['response'] = result

        print('query:', query)
        print('response:', result)

    return queries