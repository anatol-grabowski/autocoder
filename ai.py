import openai

class Ai:
    def __init__(self, openai_api_key):
        openai.api_key = openai_api_key
        if (openai.api_key is None or openai.api_key == ''):
            raise BaseException('no openai.api_key')

    def complete(self, eng, prompt, suffix=None, stop=None):
        response = openai.Completion.create(
            engine='code-davinci-002' if eng == 'code' else 'text-davinci-002',
            prompt=prompt,
            suffix=suffix,
            temperature=0 if eng == 'code' else 0.7,
            top_p=1,
            max_tokens=1000,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop,
            stream=True,
        )
        for part in response:
            if part["choices"][0]["finish_reason"] is not None: return
            yield part["choices"][0]["text"]

    def edit(self, eng, prompt, instruction):
        response = openai.Edit.create(
            engine='code-davinci-edit-001' if eng == 'code' else 'text-davinci-edit-001',
            input=prompt,
            instruction=instruction,
            temperature=0 if eng == 'code' else 0.7,
            top_p=1,
        )
        yield response["choices"][0]["text"]
