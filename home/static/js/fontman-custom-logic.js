
    if(window.opener){
      window.opener.postMessage({ msg: "picker",mode:'init' }, '*'),
            window.addEventListener(
                "message",
                function (event) {
                  let pick_msg = event.data.msg;
                  let mode = event.data.mode;
                  if(mode === 'start' && pick_msg === 'picker'){
                      $('#fontman-btn-picker').css('display','block');
                  }
                  console.log('Event received');
                },
                !1
            );
    }
    var handlerPicker = function (element) {
      const classes = document.getElementById('customElements');
      const dom_path = finder(element).trim();
      window.opener.postMessage({ msg: "picker", data: dom_path , mode:'picked' }, '*')
      disableLinks('');
    }
    var myFontManPicker = DomOutline({ onClick: handlerPicker});
    const font_picker = document.getElementById('fontman-btn-picker');
    font_picker.addEventListener('click', function(){
      myFontManPicker.start();
      //disable all links on the page
      disableLinks('none');
    });
    const disableLinks = (val) => {
      const links = document.querySelectorAll('a');
      Array.from(links).forEach( function(link) {
        link.setAttribute('style',`pointer-events:${val}`);
      });
    }