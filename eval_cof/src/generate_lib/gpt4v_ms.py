from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, ChainedTokenCredential, AzureCliCredential, get_bearer_token_provider
import re
import os
import base64

scope = "api://trapi/.default"
credential = get_bearer_token_provider(ChainedTokenCredential(
    AzureCliCredential(),
    DefaultAzureCredential(
        exclude_cli_credential=True,
        # Exclude other credentials we are not interested in.
        exclude_environment_credential=True,
        exclude_shared_token_cache_credential=True,
        exclude_developer_cli_credential=True,
        exclude_powershell_credential=True,
        exclude_interactive_browser_credential=True,
        exclude_visual_studio_code_credentials=True,
        # DEFAULT_IDENTITY_CLIENT_ID is a variable exposed in
        # Azure ML Compute jobs that has the client id of the
        # user-assigned managed identity in it.
        # See https://learn.microsoft.com/en-us/azure/machine-learning/how-to-identity-based-service-authentication#compute-cluster
        # In case it is not set the ManagedIdentityCredential will
        # default to using the system-assigned managed identity, if any.
        managed_identity_client_id=os.environ.get("DEFAULT_IDENTITY_CLIENT_ID"),
    )
),scope)

api_version = '2024-10-21'  # Ensure this is a valid API version see: https://learn.microsoft.com/en-us/azure/ai-services/openai/api-version-deprecation#latest-ga-api-release
model_name = 'gpt-4'  # Ensure this is a valid model name
model_version = 'vision-preview'  # Ensure this is a valid model version
deployment_name = re.sub(r'[^a-zA-Z0-9-_]', '', f'{model_name}_{model_version}')  # If your Endpoint doesn't have harmonized deployment names, you can use the deployment name directly: see: https://aka.ms/trapi/models
instance = 'gcr/shared' # See https://aka.ms/trapi/models for the instance name, remove /openai (library adds it implicitly) 
endpoint = f'https://trapi.research.microsoft.com/{instance}'

client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=credential,
    api_version=api_version,
)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def generate_response(image_path, query, model_path, api_key=None):
    
    base64_image = encode_image(image_path)
    
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query,
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ]

    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        max_tokens=1049,
        temperature=0.0,
        top_p=1.0
    )
    response_content = response.choices[0].message.content
    return response_content


if __name__ == "__main__":
    image_path = '/home/v-zijianli/chartagent/bar_43_3.png'
    query = "What is in this image?"
    model_path = deployment_name
    response = generate_response(image_path, query, model_path)
    print(response)

# image_path = '/home/v-zijianli/chartagent/bar_43_3.png'
# base64_image = encode_image(image_path)

# messages=[
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "What is in this image?",
#                 },
#                 {
#                     "type": "image_url",
#                     "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
#                 },
#             ],
#         }
#     ]

# # messages = [
# #         {
# #             "role": "user",
# #             "content": "hello",
# #         }
# # ]

# response = client.chat.completions.create(
#     model=deployment_name,
#     messages=messages
# )
# response_content = response.choices[0].message.content
# print(response_content)