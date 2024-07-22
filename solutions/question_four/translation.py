from transformers import T5ForConditionalGeneration, T5Tokenizer

def translate_to_english(text, source_lang):
    model_name = "t5-base"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    input_text = f"translate {source_lang} to English: {text}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    outputs = model.generate(input_ids, max_length=100, num_beams=4, early_stopping=True)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return translated_text
