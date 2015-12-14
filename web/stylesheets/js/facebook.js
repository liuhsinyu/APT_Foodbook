  window.fbAsyncInit = initFacebook;

	function initFacebook()
	{
	    console.log('statusChangeCallback');
		FB.init({
		  appId      : '890575511032481',
          cookie     : true,  // enable cookies to allow the server to access
                        // the session
          xfbml      : true,  // parse social plugins on this page
          version    : 'v2.4' // use version 2.2
		});

		FB.getLoginStatus(onFacebookLoginStatus);
	};
	(function() {
		var e = document.createElement('script');
		e.src = document.location.protocol + '//connect.facebook.net/en_US/all.js';
		e.async = true;
		document.getElementById('fb-root').appendChild(e);
		}());


  function onFacebookLoginStatus(response)
	{
	    console.log(response);
		if (response.status=="connected" && response.authResponse)
		{
			console.log(response.authResponse.userID);
			document.getElementById("user_id").value = response.authResponse.userID;
		}
		else
		{
		}

	}
