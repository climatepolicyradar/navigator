// type one text in the typwriter
// keeps calling itself until the text is finished
export function typeWriter(text, i, fnCallback, el) {
  // chekc if text isn't finished yet
  if (i < text.length) {
    // add next character to placeholder
    el.placeholder = text.substring(0, i + 1);

    // wait for a while and call this function again for next character
    setTimeout(function () {
      typeWriter(text, i + 1, fnCallback, el);
    }, 30);
  }
  // text finished, call callback if there is a callback function
  else if (typeof fnCallback == 'function') {
    // call callback after timeout
    setTimeout(fnCallback, 700);
  }
}
// start a typewriter animation for a text in the dataText array
export function StartTextAnimation(i, text, el) {
  //el.focus();
  if (typeof text[i] === 'undefined') {
    return;
    setTimeout(function () {
      StartTextAnimation(0, text, el);
    }, 20000);
  }
  // check if text[i] exists
  if (i < text[i]?.length) {
    // text exists! start typewriter animation
    typeWriter(
      text[i],
      0,
      function () {
        // after callback (and whole text has been animated), start next text
        StartTextAnimation(i + 1, text, el);
      },
      el
    );
  }
}
