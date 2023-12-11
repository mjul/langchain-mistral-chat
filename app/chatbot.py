from accelerate import infer_auto_device_map, init_empty_weights
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
from transformers import pipeline

model_id = "mistralai/Mistral-7B-v0.1"
# Some smaller models to try for faster iteration if you are on limited hardware:
#model_id = "bert-large-cased"
#model_id = "TinyLlama/TinyLlama-1.1B-Chat-v0.6"

config = AutoConfig.from_pretrained(model_id)
with init_empty_weights():
    model = AutoModelForCausalLM.from_config(config)

device_map = infer_auto_device_map(model,
                                   no_split_module_classes=["OPTDecoderLayer"],
                                   dtype="float16"
                                   )

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map=device_map)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=30)
hf = HuggingFacePipeline(pipeline=pipe)

template = """What is a good name for a company that makes {product}?"""
prompt = PromptTemplate.from_template(template)

chain = prompt | hf
