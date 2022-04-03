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
  - running as root is required for keyboard hooks to work
  - `-E` flag is required to pass `OPENAI_API_KEY` to the root shell

## Usage

- copy some text, all operations are performed on text in the clipboard*
- put the cursor where you want the result to be inserted
- press `alt gr, alt gr` (right alt key twice)
  - the result will be inserted at cursor (using `right shift+ins`)
  - hold `esc` to cancel if needed

The app detects what kind of text is in the clipboard (`text`, `js`, `python`) and what kind of action is required (`completion`, `edit` or `insert`) based on the presence of comments or `___` and `!!!` sequences. Then it uses the most appropriate settings to call the OpenAI API.

### Examples

- #### JS completion
  Clipboard:
  ```
  /* Make a js function that adds two numbers and returns the result */
  ```
  Output:
  ```
  function add(a, b) {
    return a + b
  }
  ```

- #### JS edit
  Clipboard:
  ```
  function add(a, b) {
    return a + b
  }
  // !!! rename function to summ
  // !!! add third argument
  ```
  Output:
  ```
  function summ(a, b, c) {
    return a + b + c
  }
  ```

- #### JS insert
  Clipboard:
  ```
  /* Make a js function that adds two numbers and returns the result */
  function add(a, b) {
    ___
  }
  ```
  Output:
  ```
    return a + b;
  }
  ```

- #### Text (e.g. email) edit
  Clipboard:
  ```
  Send me the docs
  !!! Rewrite this message to John in a more wordy and polite manner
  ```
  Output:
  ```
  Dear John,

  Please send the new documents over to me.

  Thank you,

  Susan
  ```
