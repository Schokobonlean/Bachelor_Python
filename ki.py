from transformers import AutoTokenizer, AutoModelForCausalLM

def infer(prompt):
    loaded_tokenizer = AutoTokenizer.from_pretrained("components\model_and_tokenizer")
    loaded_model = AutoModelForCausalLM.from_pretrained("components\model_and_tokenizer")
    input_ids = loaded_tokenizer(prompt, return_tensors="pt")
    output = loaded_model.generate(input_ids["input_ids"], max_new_tokens = 40, attention_mask=input_ids["attention_mask"], pad_token_id = loaded_tokenizer.eos_token_id)
    response = loaded_tokenizer.decode(output[0], no_repeat_ngram_size=2, skip_special_tokens=True)
    return response