var EASYINSTA;
if (!EASYINSTA) EASYINSTA = {}; 

(function(){
	var func = EASYINSTA;

	/** Create CORS:Cross-origin Resource Sharing **/
	  /*****************************************/
	func.createCORSRequest = function(method, url) {
	  if (window.XMLHttpRequest) {
	  	  var xhr = new XMLHttpRequest();
		  xhr.open(method,url);
		  return xhr;
	  };
	}

	/** Authenticate **/
	  /*************/
	func.authenticate2 = function(){
		var CLIENT_ID = '98f5f45159f042168e51b6c21aeb40e1';
    	var REDIRECT_URI = 'http://easyinsta.com/';
    	var AUTHENTICATE_URL = 'https://api.instagram.com/oauth/authorize/?client_id=98f5f45159f042168e51b6c21aeb40e1&redirect_uri=http://easyinsta.com/&response_type=code&scope=scope=basic+public_content+follower_list+relationships+likes+comments';
    	var xhr = EASYINSTA.createCORSRequest("GET",AUTHENTICATE_URL);
    	xhr.setRequestHeader('Access-Control-Allow-Origin','*');

    	xhr.onload = function(){
    		var data = xhr.responseText;
    		console.log("TITLE : " + getTitle(data));
    		console.log(data);
    	}

    	xhr.onerror = function(){
    		console.log("error authenticate!");
    	}

    	xhr.send();
	}

	func.authenticate = function(){
		var CLIENT_ID = '98f5f45159f042168e51b6c21aeb40e1';
    	var REDIRECT_URI = 'http://easyinsta.com/';
    	var AUTHENTICATE_URL = 'https://api.instagram.com/oauth/authorize/?client_id='+CLIENT_ID+'&redirect_uri='+REDIRECT_URI+'&response_type=code';
    	
		$.ajax({
		    type: "GET",
		    dataType: 'application/json',
		    url: AUTHENTICATE_URL,
		    crossDomain : true,
		    beforeSend : function(xhr){
		    	xhr.setRequestHeader('Access-Control-Allow-Origin','*');
		    	xhr.setRequestHeader("Content-Type", "application/json; charset=utf-8");
		    },
		    success: function(data){
		    	console.log(JSON.Stringify(data));
		    },
		    error: function(req, status, error){
		    	console.log(req.responseText);
	        	console.log(status);
	        	console.log(error);
		    }
		});
	}
	

})();
