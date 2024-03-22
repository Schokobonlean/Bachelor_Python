from transformers import AutoTokenizer, AutoModelForCausalLM
loaded_tokenizer = AutoTokenizer.from_pretrained("components\model_and_tokenizer")
loaded_model = AutoModelForCausalLM.from_pretrained("components\model_and_tokenizer")

def infer(prompt):
    input_ids = loaded_tokenizer(prompt, return_tensors="pt")
    output = loaded_model.generate(input_ids["input_ids"], max_new_tokens = 120, attention_mask=input_ids["attention_mask"], pad_token_id = loaded_tokenizer.eos_token_id,  no_repeat_ngram_size=2)
    response = loaded_tokenizer.decode(output[0], no_repeat_ngram_size=2, skip_special_tokens=True)
    response = response[response.find("\n"):].strip()
    if response.rfind(".") != -1:
        response = response[:response.rfind(".")]+"."
    return response