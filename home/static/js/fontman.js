function InitFontMan(){!function(e){var t="https://www.fontman.in",n=document.head||document.getElementsByTagName("head")[0],a=document.createElement("style");a.type="text/css",a.id="fontman-picker";var o=!1,i=[];function r(){o=!0,e("body").on("click","*:not(.btn-add-picker-element)",function(n){n.stopPropagation(),n.preventDefault();var a=e(this);console.log();var r=[];if(""!=n.currentTarget.id)r.push("#"+n.currentTarget.id);else if(a.get(0).className.length>0){let e=a.parent();if(r="",e){let t=e.parent().get(0);t&&(console.log(t.classList.value.trim()),r=(t.id?"#"+t.id:t.classList.length?"."+t.classList.value.trim().replace(/\s+/g,"."):t.localName)+" ",console.log(r)),r+=(e=e.get(0)).id?"#"+e.id:e.classList.length?"."+e.classList.value.trim().replace(/\s+/g,"."):e.localName,console.log(r)}r+=" ."+a.get(0).className.trim().replace(/\s/g,"."),console.log(r)}else{var s=""!=n.currentTarget.parentElement.id?"#"+n.currentTarget.parentElement.id:n.currentTarget.parentElement&&n.currentTarget.parentElement.classList.length?"."+n.currentTarget.parentElement.className.trim().replace(/\s+/g,"."):n.currentTarget.parentElement.localName;r.push(s+" "+n.currentTarget.localName)}i=jQuery.unique(i.concat(r)),window.opener.postMessage({message:"pull",data:i},t),e("body *:not(.btn-add-picker-element)").unbind(n),e(this).css("box-shadow","inherit"),e(".btn-add-picker-element").removeClass("active"),o=!1})}n.appendChild(a),window.opener.postMessage({message:"init",data:[]},t),window.addEventListener("message",function(n){n.origin===t&&"string"==typeof n.data.message&&"pick"==n.data.message&&(i=n.data.data,e("#fontman-picker").text("*{cursor: pointer;}.btn-add-picker-element:not(.active){z-index:99999;font-weight:bold;font-size:20px; position:fixed;top:50%;right:20px;width:50px;height:50px;text-align:center;opacity:1;border-radius:50%;border-color:purple!important;border-width:.5px ;border-radius:50%;-webkit-animation:bounce 0.5s infinite alternate;-moz-animation:bounce 0.5s infinite alternate;animation:bounce 0.5s infinite alternate;pointer-events:auto;cursor:pointer}.btn-add-picker-element.active{position:absolute;top:50%;right:20px;width:50px;height:50px;text-align:center;opacity:1;border-color:purple!important;border-width:.5px border-radius:50%;cursor:not-allowed;pointer-events:none;-webkit-animation:bounce 995s infinite alternate;-moz-animation:bounce 95s infinite alternate;animation:bounce 95s infinite alternate}@-webkit-keyframes bounce{to{-webkit-transform:scale(1.2);border-width:3px}}@-moz-keyframes bounce{to{-moz-transform:scale(1.2);border-width:3px}}@keyframes bounce{to{transform:scale(1.2);border-width:3px}}p"),e("body").on("mouseenter","*:not(.btn-add-picker-element)",function(t){t.stopPropagation(),t.preventDefault(),o&&(console.log("Set shadow"),e(this).css("box-shadow","0px 0px 1px 1px purple"))}),e("body").on("mouseleave mouseout","*:not(.btn-add-picker-element)",function(t){t.stopPropagation(),t.preventDefault(),o&&e(this).css("box-shadow","inherit")}),e("body").append('<button class="btn-add-picker-element icon-addition secondary tip active" data-hover="Pick element" title="Pick element">+</button>'),e("body").on("click",".btn-add-picker-element",function(t){t.preventDefault(),e(this).addClass("active"),r()}),r())},!1)}(jQuery)}if(window.opener){var fontman_count=0,fontman_inteval=function(){setTimeout(function(){if(window.jQuery)InitFontMan();else if(fontman_count<=30){if(fontman_inteval(),fontman_count>20&&!document.getElementById("fontman-embed-jquery")){let e=document.createElement("script");e.src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js",e.async="async",e.id="fontman-embed-jquery",document.head.appendChild(e)}fontman_count+=1}else console.log("Your site missing JQuery. Please contact: support@fontman.in")},500)};fontman_inteval()}