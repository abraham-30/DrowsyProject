/* SCROLL */
window.onbeforeunload = function(){
    window.scrollTo(0, 0);
}

// left: 37, up: 38, right: 39, down: 40,
// spacebar: 32, pageup: 33, pagedown: 34, end: 35, home: 36
var keys = {37: 1, 38: 1, 39: 1, 40: 1};

function preventDefault(e) {
  e.preventDefault();
}

function preventDefaultForScrollKeys(e) {
  if (keys[e.keyCode]) {
    preventDefault(e);
    return false;
  }
}

// modern Chrome requires { passive: false } when adding event
var supportsPassive = false;
try {
  window.addEventListener("test", null, Object.defineProperty({}, 'passive', {
    get: function () { supportsPassive = true; } 
  }));
} catch(e) {}

var wheelOpt = supportsPassive ? { passive: false } : false;
var wheelEvent = 'onwheel' in document.createElement('div') ? 'wheel' : 'mousewheel';

window.onload = disableScroll();

// call this to Disable
function disableScroll() {
  window.addEventListener('DOMMouseScroll', preventDefault, false); // older FF
  window.addEventListener(wheelEvent, preventDefault, wheelOpt); // modern desktop
  window.addEventListener('touchmove', preventDefault, wheelOpt); // mobile
  window.addEventListener('keydown', preventDefaultForScrollKeys, false);
}

// call this to Enable
function enableScroll() {
  window.removeEventListener('DOMMouseScroll', preventDefault, false);
  window.removeEventListener(wheelEvent, preventDefault, wheelOpt); 
  window.removeEventListener('touchmove', preventDefault, wheelOpt);
  window.removeEventListener('keydown', preventDefaultForScrollKeys, false);
}

document.addEventListener('DOMContentLoaded',function(event){
    // array with texts to type in typewriter
    var dataText = [ "dRizz.ly"];
    var column_right =  document.getElementById('jumbo-col-right');
    var menu = document.getElementById('menu');
    var menu_content = document.getElementById('menu_content');
    var camera = document.getElementById('camera');
    
    // type one text in the typwriter
    // keeps calling itself until the text is finished
    function typeWriter(text, i, fnCallback) {
      // chekc if text isn't finished yet
      if (i < (text.length)) {
        // add next character to h1
       document.querySelector("h1").innerHTML = text.substring(0, i+1) +'<span aria-hidden="true"></span>';
  
        // wait for a while and call this function again for next character
        setTimeout(function() {
          typeWriter(text, i + 1, fnCallback)
        }, 100);
      }
      // text finished, call callback if there is a callback function
    //   else if (typeof fnCallback == 'function') {
    //     // call callback after timeout
    //     setTimeout(fnCallback, 700);
    //   }
        else{
            column_right.style.opacity = "1";
            column_right.style.transition = "opacity 1s ease-in";
            menu.style.opacity = "1";
            menu.style.transition = "opacity 1s ease-in";
            camera.style.opacity = "1";    
            camera.style.transition = "opacity 1s ease-in";
            setTimeout(enableScroll(), 1000);
        }
    }
    // start a typewriter animation for a text in the dataText array
     function StartTextAnimation(i) {
       if (typeof dataText[i] == 'undefined'){
          setTimeout(function() {
            StartTextAnimation(0);
          }, 20000);
       }
       // check if dataText[i] exists
      if (i < dataText[i].length) {
        // text exists! start typewriter animation
       typeWriter(dataText[i], 0, function(){
         // after callback (and whole text has been animated), start next text
         StartTextAnimation(i + 1);
       });
      }
    }
    // start the text animation
    StartTextAnimation(0);
  });

/* Clock */
const time_hour = document.querySelector(".time_hour");
const time_minute = document.querySelector(".time_minute");
const time_seconds = document.querySelector(".time_seconds");

/**
 * @param {Date} date
 */

function format_hour(date){
    const hour = date.getHours();
    return `${(hour.toString().padStart(2, "0"))}`;
}

function format_minute(date){
    const minute = date.getMinutes();
    return `${(minute.toString().padStart(2, "0"))}`;
}

function format_second(date){
    const seconds = date.getSeconds();
    return `${(seconds.toString().padStart(2, "0"))}`;
}

setInterval(function(){
    const now = new Date();
    time_hour.textContent = format_hour(now);
    time_minute.textContent = format_minute(now);
    time_seconds.textContent = format_second(now);
}, 200);
