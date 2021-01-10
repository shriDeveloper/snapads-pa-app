function addGoogleFont(FontName) {
    $("head").append("<link href='https://fonts.googleapis.com/css?family=" + FontName + "' rel='stylesheet' type='text/css'>");
}
function slugiFyFont(font){
	var font_name = font.split(":")[0];
    var font_slug =  font_name.split(' ').join('+');
    return font_slug;
}
function loadFontMan(store_token){
	const urlParams = new URLSearchParams(window.location.search);
	const myParam = urlParams.get('dev_mode');
	if(myParam != null && myParam === 'on'){
		console.log(myParam);
		//dev center here
		$('body').css({
          		"cursor":"pointer",
          	});
	console.log('AJX CALL Successfully');
	var array = []
	$(document).on('click',function(event){
		//classList
		if(array.includes(event.target)){
			$(event.target).css('border','none');
			if (array.indexOf(event.target) > -1) {
  				array.splice(array.indexOf(event.target), 1);
			}	
		}else{

			$(event.target).css('border','10px solid black');
			array.push(event.target);
			
			var arr   = event.target.classList['value'].split(/\s+/);
			var selector   = '.' + arr.join('.');
			
			if(selector === '.'){
				var selector = event.target; 
			}
			
			console.log(selector);
			console.log("Sending data to http://dev.project.com.");
			parent.postMessage(
				{
					user_age:    '12',
					user_height: '12',
				},
				"http://localhost:8000/");

		}
	});


	}
	
	$.ajax({
          type:'GET',
          url:'http://localhost:8000/api/fontman',
          data:{'store_token':store_token},
          success:function(response){
          	var tags = ['p','h1','h2','h3','h4','h5','h6','blockquote','li','a'];
          	if(response['body_tag']!=""){
          		//add google font to all tags dynamically
          		var slugifiedFont = slugiFyFont(response['body_tag'])  
          		addGoogleFont(slugifiedFont);
    //       		for (i = 0; i < tags.length; ++i) {
    // 				$(''+tags[i]).css({
    //       				"font-family":response['body_tag'],
    //       				"font-size":"10px",
    //       				"color":"red",
    //       			});
				// }

				$("p").css({
          				"font-family":response['body_tag'],
          				"font-size":"50px",
          				"color":"black",
          			});


            	console.log(response['body_tag']);
          	}
          	
          }
    });
}