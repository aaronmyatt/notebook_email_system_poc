(function() {

    function send_emails_button() {
        var request = new XMLHttpRequest();
        request.open('GET', '/emailer/send', true);
        
        request.onload = function() {
          if (this.status >= 200 && this.status < 400) {
            // Success!
            console.log('EMAILER SEND SUCCESS')
            location.reload()
          } else {
            console.log('EMAILER SEND DID NOTHING')
            location.reload()
          }
        }
        
        request.onerror = function() {
            console.log('EMAILER SEND DID SOMETHING WRONG')
        }
        
        request.send()
    }


    function attach_handlers(){
        console.log('ATTACHING EVENT HANDLERS')
        el = document.getElementById('email_send_button')
        el.addEventListener('click', send_emails_button)
    }



    function ready(fn) {
        if (document.attachEvent ? document.readyState === "complete" : document.readyState !== "loading"){
            console.log('DOCUMENT READY')
            attach_handlers()
        } else {
          document.addEventListener('DOMContentLoaded', attach_handlers)
        }
      }

    ready()

})()