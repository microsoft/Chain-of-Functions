from openai import AzureOpenAI
from openai import OpenAI
from azure.identity import DefaultAzureCredential, ChainedTokenCredential, AzureCliCredential, get_bearer_token_provider
import re
import os
import base64
import json



### https://github.com/IDEA-FinAI/ChartBench/blob/main/Stat/gpt_filter.py
SYSTEM_MESSAGE = """
Please extract the answer from the model response and type it.

Note:
1. The responses may be a phrase, a number, or a sentence.
2. If the content of the responses is not understandable, return "FAILED".
3. If the content of the responses is understandable, extract the numerical value from it.
4. If the responses is a yes or no judgment, return yes or no.

Special requirements: ** Only numbers, short texts, "FAILED", or yes/no are allowed to be returned for each response, please do not return anything else! **

Please read the following example. 

Question 1: Which number is missing?
Model response: The number missing in the sequence is 14.

Question 2: What is the fraction of females facing the camera?
Model response: The fraction of females facing the camera is 0.6, which means that six out of ten females in the group are facing the camera.

Question 3: How much money does Luca need to buy a sour apple candy and a butterscotch candy? (Unit: $)
Model response: Ax00 Ax00 Ax00 Ax00 Ax00 Ax00 Ax00 Ax00 Ax00 Ax00 Ax00. 

Question 4: In the chart titled \"Quarterly Sales Breakdown by Product Category\", if we identify the product category with the second lowest sales value for Q1 2023, what is the color associated with that category?
Model response: The product category with the second lowest sales value for Q1 2023 is Jewelry. The color associated with that category is gray.

Question 5: Which month shows the smallest difference in visitors between mobile devices and desktop devices?
Model response: The difference in visitors between mobile devices and desktop devices is the smallest in Apr.

Your answer: 
14
0.6
FAILED
gray
Apr
"""

USER_MESSAGE = """ 
Please extract the answer from the model response and type it.

Note:
1. The responses may be a phrase, a number, or a sentence.
2. If the content of the responses is not understandable, return "FAILED".
3. If the content of the responses is understandable, extract the numerical value from it.
4. If the responses is a yes or no judgment, return yes or no.
5. If the answer contains a unit, please exclude the unit and only return the numerical value.

Special requirements: ** Only numbers, short texts, "FAILED", or yes/no are allowed to be returned for each response, please do not return anything else! **

Please read the following example. 

Question 1: Which number is missing?
Model response: The number missing in the sequence is 14.

Question 2: What is the fraction of females facing the camera?
Model response: The fraction of females facing the camera is 0.6, which means that six out of ten females in the group are facing the camera.

Question 3: How much money does Luca need to buy a sour apple candy and a butterscotch candy? (Unit: $)
Model response: Ax00 Ax00 Ax00 Ax00 Ax00 Ax00 Ax00 Ax00 Ax00 Ax00 Ax00. 

Question 4: In the chart titled \"Quarterly Sales Breakdown by Product Category\", if we identify the product category with the second lowest sales value for Q1 2023, what is the color associated with that category?
Model response: The product category with the second lowest sales value for Q1 2023 is Jewelry. The color associated with that category is gray.

Question 5: Which month shows the smallest difference in visitors between mobile devices and desktop devices?
Model response: The difference in visitors between mobile devices and desktop devices is the smallest in Apr.

Your answer: 
14
0.6
FAILED
gray
Apr

Question: {}
Model response: {}
Expected answer:
"""


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def generate_response(question, response, api_key=None):
    curr_retries = 0
    max_tokens = 256
    max_retries = 10
    while curr_retries < max_retries:
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
            response = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": USER_MESSAGE.format(question, response),
                            }
                        ],
                        model="gpt-4o-2024-05-13",
                        response_format={"type": "json_object"},
                        n=1,
                        max_tokens=1049,
                        temperature=0,
                        top_p=1,
                        seed=42,
                    ).choices[0].message.content
            response_content = json.loads(response)
        except Exception as e:
            curr_retries += 1
            if curr_retries >= max_retries:
                print(f"Error: {e}")
                return "FAILED"
            continue
        break

    return response_content


if __name__ == "__main__":
    image_path = './bar_43_3.png'
    question = "How many quarters are shown in the chart for the sales performance of the category represented by the dark blue color?"
    response = "The chart shows 7 quarters for the sales performance represented by the dark blue color."
    model_path = deployment_name
    response = generate_response(question, response)
    print(response)

