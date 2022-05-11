{
  "pattern": "^\\s*((/\\* js: )|(// js: )|(/\\* )|(/\\*\\*\\n)|(// ))",
  "model": {
    "engine": "code-davinci-002",
    "temperature": 0.0,
    "top_p": 1,
    "max_tokens": 1000,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "stop": "\n\n"
  }
}

/* I start with a blank HTML page, and incrementally modify it via <script> injection. Written for Chrome. */

/* js: Add "Hello World", by adding an HTML DOM node */
const helloWorld = document.createElement('div')
helloWorld.innerHTML = 'Hello World'
document.body.appendChild(helloWorld)

// js: Clear the page.
while (document.body.firstChild) {
  document.body.removeChild(document.body.firstChild)
}

