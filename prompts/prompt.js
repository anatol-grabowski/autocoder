/* I start with a blank HTML page, and incrementally modify it via <script> injection. Written for Chrome. */

/* Add "Hello World", by adding an HTML DOM node */
const helloWorld = document.createElement('div')
helloWorld.innerHTML = 'Hello World'
document.body.appendChild(helloWorld)

/* Clear the page. */
while (document.body.firstChild) {
  document.body.removeChild(document.body.firstChild)
}