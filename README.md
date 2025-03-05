
# ChartCoF
📄[Paper](xxx)

This repository contains the code to evaluate models on CharXiv from the paper [Chain of Functions: A Programmatic Pipeline for Fine-Grained Chart
Reasoning Data](xxx).


## Evaluation
Here we present how to evaluate the model on ChartCoF dataset. Since there are different environments for models, you need to set up different environments accoding to the model you want to evaluate. Here we provide the example of evaluation code InternVL-2.5-8B. If you want to evaluate on your own models, you need to write customized output functions on `eval_cof/src/generate_lib`.

## Installation

```
conda create -n cof python=3.9
conda activate cof
cd InternVL/
pip install -r requirements.txt
pip install flash-attn==2.3.6 --no-build-isolation
```

Please follow the instructions in the [InternVL documentation](https://internvl.readthedocs.io/en/latest/get_started/installation.html) to install the required dependencies.

## Run
We first generate the answer files. We provide the prompts for directly outputting the answer `input_option=only_answer` and CoT `input_option=cot`. You can also use your custermized output functions by modifying the `eval_cof/src/query_utils.py`.

```
python src/evaluate.py \
    --model_path path-to-internvl25_8b \
    --model_name internvl25 \
    --directory ./ \
    --question_path ./chartcof.json \
    --answers_path ./results/chartcof_internvl25_8b_only_answer.jsonl \
    --temperature 0.0 \
    --top_p 1.0 \
    --num_beams 1 \
    --input_option only_answer \
    --batch_size 1
```

Evaluate the generated answer files.

```
python eval_cof/src/get_score.py \
    --response_path results/chartcof_internvl25_8b_only_answer.jsonl
```

Optional: For those models with weak instruction-following capabilities we provide question extraction using GPT-4o.

```
python eval_cof/src/extract_answer.py \
    --response_path results/chartcof_internvl25_8b_only_answer.jsonl
```

Compute the statistics for the models with respect to the question type, Annotation, and chart type.

```
python eval_cof/src/get_stat_basic.py \
    --score_path results/chartcof_internvl25_8b_only_answer_score.jsonl
```

Compute the adavaned statistics for the models with respect to the Step Number, and Function Chains.

```
python eval_cof/src/get_stat.py \
    --score_path results/chartcof_internvl25_8b_only_answer_score.jsonl
```


# Project

> This repo has been populated by an initial template to help get you started. Please
> make sure to update the content to build a great experience for community-building.

As the maintainer of this project, please make a few updates:

- Improving this README.MD file to provide a great experience
- Updating SUPPORT.MD with content about this project's support experience
- Understanding the security reporting process in SECURITY.MD
- Remove this section from the README

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
