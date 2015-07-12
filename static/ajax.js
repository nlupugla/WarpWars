// make AJAX GET request
function makeGetRequest(url, callback){
	var request = new XMLHttpRequest();
	request.open('GET', url, true);
	
	request.onload = function(){
		if(request.status >= 200 && request.status < 400) {
			// success
			var data = JSON.parse(request.responseText);
			callback(data);
		} else {
			// We reached our target server, but it returned an error
			// do something competent, maybe?
		}
	};

	request.onerror = function() {
		// There was a connection error of some sort
	};

	request.send();
}