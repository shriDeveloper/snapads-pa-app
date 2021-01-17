function InitFontify() {
    (function ($) {
        var origin = "http://localhost:8000";
        var css = "h1 { background: red; }",
            head = document.head || document.getElementsByTagName("head")[0],
            style = document.createElement("style");
        style.type = "text/css";
        style.id = "fontify-picker";
        var isPicker = false;
        var doms = [];
        head.appendChild(style);
        function receiveMessage(evt) {
            if (evt.origin !== origin) return;
            if (typeof evt.data.message == "string" && evt.data.message == "pick") {
                doms = evt.data.data;
                $("#fontify-picker").text(
                    "*{cursor: pointer;}.btn-add-picker-element:not(.active){z-index:99999;font-weight:bold;font-size:20px; position:fixed;top:50%;right:20px;width:50px;height:50px;text-align:center;opacity:1;border-radius:50%;border-color:red!important;border-width:.5px ;border-radius:50%;-webkit-animation:bounce 0.5s infinite alternate;-moz-animation:bounce 0.5s infinite alternate;animation:bounce 0.5s infinite alternate;pointer-events:auto;cursor:pointer}.btn-add-picker-element.active{position:absolute;top:50%;right:20px;width:50px;height:50px;text-align:center;opacity:1;border-radius:50%;border-color:red!important;border-width:.5px border-radius:50%;cursor:not-allowed;pointer-events:none;-webkit-animation:bounce 995s infinite alternate;-moz-animation:bounce 95s infinite alternate;animation:bounce 95s infinite alternate}@-webkit-keyframes bounce{to{-webkit-transform:scale(1.2);border-width:3px}}@-moz-keyframes bounce{to{-moz-transform:scale(1.2);border-width:3px}}@keyframes bounce{to{transform:scale(1.2);border-width:3px}}p"
                );
                $("body").on("mouseenter", "*:not(.btn-add-picker-element)", function (evt) {
                    evt.stopPropagation();
                    evt.preventDefault();
                    if (isPicker) {
                        console.log("Set shadow");
                        $(this).css("box-shadow", "0px 0px 1px 1px red");
                    }
                });
                $("body").on("mouseleave mouseout", "*:not(.btn-add-picker-element)", function (evt) {
                    evt.stopPropagation();
                    evt.preventDefault();
                    if (isPicker) {
                        $(this).css("box-shadow", "inherit");
                    }
                });
                $("body").append('<button class="btn-add-picker-element icon-addition secondary tip active" data-hover="Pick element" title="Pick element">+</button>');
                $("body").on("click", ".btn-add-picker-element", function (evt) {
                    evt.preventDefault();
                    $(this).addClass("active");
                    doPicker();
                });
                doPicker();
            }
        }
        function doPicker() {
            isPicker = true;
            $("body").on("click", "*:not(.btn-add-picker-element)", function (event) {
                event.stopPropagation();
                event.preventDefault();
                var $this = $(this);
                console.log();
                var dom = [];
                if (event.currentTarget.id != "") {
                    dom.push("#" + event.currentTarget.id);
                } else if ($this.get(0).className.length > 0) {
                    let parent = $this.parent();
                    dom = "";
                    if (parent) {
                        let granfather = parent.parent().get(0);
                        if (granfather) {
                            console.log(granfather.classList.value.trim());
                            dom = (granfather.id ? "#" + granfather.id : granfather.classList.length ? "." + granfather.classList.value.trim().replace(/\s+/g, ".") : granfather.localName) + " ";
                            console.log(dom);
                        }
                        parent = parent.get(0);
                        dom += parent.id ? "#" + parent.id : parent.classList.length ? "." + parent.classList.value.trim().replace(/\s+/g, ".") : parent.localName;
                        console.log(dom);
                    }
                    dom += " ." + $this.get(0).className.trim().replace(/\s/g, ".");
                    console.log(dom);
                } else {
                    var parent =
                        event.currentTarget.parentElement.id != ""
                            ? "#" + event.currentTarget.parentElement.id
                            : event.currentTarget.parentElement && event.currentTarget.parentElement.classList.length
                            ? "." + event.currentTarget.parentElement.className.trim().replace(/\s+/g, ".")
                            : event.currentTarget.parentElement.localName;
                    dom.push(parent + " " + event.currentTarget.localName);
                }
                doms = jQuery.unique(doms.concat(dom));
                window.opener.postMessage({ message: "pull", data: doms }, origin);
                $("body *:not(.btn-add-picker-element)").unbind(event);
                $(this).css("box-shadow", "inherit");
                $(".btn-add-picker-element").removeClass("active");
                isPicker = false;
            });
        }
        window.opener.postMessage({ message: "init", data: [] }, origin);
        window.addEventListener("message", receiveMessage, false);
    })(jQuery);
}
if (window.opener) {
    var fontify_count = 0;
    var fontify_inteval = function () {
        setTimeout(function () {
            if (window.jQuery) {
                InitFontify();
            } else if (fontify_count <= 30) {
                fontify_inteval();
                if (fontify_count > 20 && !document.getElementById("fontify-embed-jquery")) {
                    let dom = document.createElement("script");
                    dom.src = "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js";
                    dom.async = "async";
                    dom.id = "fontify-embed-jquery";
                    document.head.appendChild(dom);
                }
                fontify_count += 1;
            } else {
                console.log("Your site missing JQuery. Please contact: truongthangit9x@gmail.com");
            }
        }, 500);
    };
    fontify_inteval();
}