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
}