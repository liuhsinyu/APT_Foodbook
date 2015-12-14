// This is called with the results from from FB.getLoginStatus().
  function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    console.log(response);
    // The response object is returned with a status field that lets the
    // app know the current login status of the person.
    // Full docs on the response object can be found in the documentation
    // for FB.getLoginStatus().
    if (response.status === 'connected') {
      // Logged into your app and Facebook.
      testAPI();
      var msg = document.getElementById("welcome-msg");
      msg.style.display="none";
    } else if (response.status === 'not_authorized') {
      // The person is logged into Facebook, but not your app.
      document.getElementById('status').innerHTML = 'Please log ' +
        'into this app.';
      var msg = document.getElementById("welcome-msg");
      msg.style.display="block";
    } else {
      // The person is not logged into Facebook, so we're not sure if
      // they are logged into this app or not.
      document.getElementById('status').innerHTML = 'Please log ' +
        'into Facebook.';
      var msg = document.getElementById("welcome-msg");
      msg.style.display="block";
    }
  }
  // This function is called when someone finishes with the Login
  // Button.  See the onlogin handler attached to it in the sample
// code below.
  function checkLoginState() {
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
  }
  function facebookLogout()
	{
		FB.logout();
		var loginButtonDiv=document.getElementById("fb-login-button-div");
		loginButtonDiv.style.display="block";
		var logoutButtonDiv=document.getElementById("fb-logout-button-div");
		logoutButtonDiv.style.display="none";
		var contentDiv=document.getElementById("user-is-authenticated-div");
		contentDiv.style.display="none";
	}
  window.fbAsyncInit = function() {
  FB.init({
    appId      : '890575511032481',
    cookie     : true,  // enable cookies to allow the server to access
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.4' // use version 2.2
  });
  // Now that we've initialized the JavaScript SDK, we call
  // FB.getLoginStatus().  This function gets the state of the
  // person visiting this page and can return one of three states to
  // the callback you provide.  They can be:
  //
  // 1. Logged into your app ('connected')
  // 2. Logged into Facebook, but not your app ('not_authorized')
  // 3. Not logged into Facebook and can't tell if they are logged into
  //    your app or not.
  //
  // These three cases are handled in the callback function.
  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });
  };
  // Load the SDK asynchronously
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));
  // Here we run a very simple test of the Graph API after login is
  // successful.  See statusChangeCallback() for when this call is made.
function testAPI() {
    console.log('Welcome!  Fetching your information.... ');
    var form = document.createElement("form");
    form.setAttribute("method","post");
    form.setAttribute("action","/login");

    FB.api('/me', function(response) {
      console.log(response);
      document.getElementById('status').innerHTML = 'Successfully logging in, ' + response.name + '!'+'<br> Start exploring Foodbook!<br></h3>';
      var idField = document.createElement("input");
      idField.setAttribute("type","hidden");
      idField.setAttribute("name","user_id");
      idField.setAttribute("value",response.id);
      form.appendChild(idField);
      var nameField = document.createElement("input");
      nameField.setAttribute("type","hidden");
      nameField.setAttribute("name","user_name");
      nameField.setAttribute("value",response.name);
      form.appendChild(nameField);
      document.body.appendChild(form);
    });

    FB.api('/me/picture',
        function (response) {
        if (response && !response.error) {
            /* handle the result */
            console.log(response);
            var photoField = document.createElement("input");
            photoField.setAttribute("type","hidden");
            photoField.setAttribute("name","photo");
            photoField.setAttribute("value",response.data.url);
            form.appendChild(photoField);
            document.body.appendChild(form);
        }
        }
    );

    FB.api('/me/friends', function(response) {
      console.log(response);
//      document.getElementById('status').innerHTML = 'Successfully friends, ' + response.data + '!'+'<br> Start exploring Foodbook!<br></h3>';
      var nameField = document.createElement("input");
      nameField.setAttribute("type","hidden");
      nameField.setAttribute("name","user_friends");
      nameField.setAttribute("value",JSON.stringify(response.data));
      form.appendChild(nameField);
      document.body.appendChild(form);
      form.submit();
    });

  }
