# Autocoder

Get GPT-3 completions or edits in any app.

## Start

- sign up for [openai API](https://beta.openai.com/account/api-keys)
  - email and phone number verification is required
  - engines used by the app should be available: `code-davinci-002`, `text-davinci-002`, `code-davinci-edit-001`, `text-davinci-edit-001`
- add `OPENAI_API_KEY` to `.env` file
- `pipenv install`
- `pipenv shell`
- `sudo -E python main.py`
  - running as root is required (only on Linux?) for keyboard hooks to work
  - `-E` flag is required to pass `OPENAI_API_KEY` to the root shell

## Usage

- copy some text, all operations are performed on text in the clipboard
- put the cursor where you want the result to be inserted
- press `alt gr, alt gr` (right alt key twice)
  - the result will be inserted at cursor (using `right shift+ins`)
  - hold `esc` to cancel if needed

The app matches copied text by regular expression to one of the prompts in `./prompts/` directory.
The text of the prompt is then concatenated with the copied text and send to the OpenAI API.
The API response is inserted into the input.

### Examples

- #### JS completion

  Clipboard:

  ```
  /* A js function that adds two numbers and returns the result */
  ```

  Output:

  ```
  function add(a, b) {
    return a + b
  }
  ```
