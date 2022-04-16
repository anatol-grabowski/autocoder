import openai

class Ai:
    def __init__(self, openai_api_key):
        openai.api_key = openai_api_key
        if (openai.api_key is None or openai.api_key == ''):
            raise BaseException('no openai.api_key')

    def complete(self, params):
        params['stream'] = True
        response = openai.Completion.create(**params)
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
