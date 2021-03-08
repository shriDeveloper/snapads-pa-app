function loadFontMan(){
      //add the link to head element
    var fontman_link = document.createElement('link');
      fontman_link.setAttribute('rel', 'stylesheet');
      fontman_link.type = 'text/css';
      fontman_link.href = 'https://www.fontman.in/static/css/font-man-picker-css.css';
    var picker_button  = document.createElement('input');
      picker_button.setAttribute('id', 'fontman-btn-picker');
      picker_button.setAttribute('type', 'button');
      picker_button.setAttribute('value', '+');
    document.head.appendChild(fontman_link);
    document.body.appendChild(picker_button);
    const fontman_scripts = [{
        'id':'fontman-jquery-script',
        'src':'https://code.jquery.com/jquery-3.6.0.min.js'
    },{
        'id':'fontman-element-picker',
        'src':'https://www.fontman.in/static/js/fontman-element-picker.js'
    },{
        'id':'fontman-dom',
        'src':'https://www.fontman.in/static/js/fontman-dom.js'
    },{
        'id':'fontman-custom-logic',
        'src':'https://www.fontman.in/static/js/fontman-custom-logic.js'
    }];
    fontman_scripts.forEach((script)=>{
      var fontman_script = document.createElement('script');
      fontman_script.setAttribute('id', script.id);
      fontman_script.setAttribute('src', script.src);
      fontman_script.setAttribute('type','text/javascript');
      document.body.appendChild(fontman_script);
    });
  }

  loadFontMan();
