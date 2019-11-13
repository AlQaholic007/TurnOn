function start_scroll_down() { 
    scroll = setInterval(function(){ window.scrollBy(0, 1000); console.log('start');}, 1500);
 }
 
 function stop_scroll_down() {
    clearInterval(scroll);
    console.log('stop');
 }