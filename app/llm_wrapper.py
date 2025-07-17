# llm_wrapper.py

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# Load tokenizer + model
print("🔄 Loading Phi-2 model...")
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/phi-2",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)

# Set up generation pipeline
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1
)

def generate_response(prompt: str, max_tokens=1000):
    print("⚡ Generating Sarathi's response...")
    output = generator(
        prompt,
        max_new_tokens=max_tokens,
        do_sample=True,
        temperature=0.7,
        top_p=0.95,
        repetition_penalty=1.1,
    )
    return output[0]['generated_text'].replace(prompt, "").strip()
