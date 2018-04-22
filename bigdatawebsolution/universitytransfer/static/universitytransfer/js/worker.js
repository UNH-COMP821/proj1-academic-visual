importScripts("./viz.js");


onmessage = function(e) {        
    result = e.data;        
    updateOutput(result);
  }

// onmessage = function(e) {
// //   var result = new Viz(e.data.src, e.data.options);
// //   postMessage(result);
// var dataz = e.data;

// }
