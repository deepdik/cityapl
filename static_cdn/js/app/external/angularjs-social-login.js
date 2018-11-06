"use strict";

var socialLogin = angular.module('socialLogin', []);

socialLogin.provider("social", function(){
	var fbKey, fbApiV, googleKey;
	return {
		setFbKey: function(obj){
			fbKey = obj.appId;
			fbApiV = obj.apiVersion;
			var d = document, fbJs, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
			fbJs = d.createElement('script'); 
			fbJs.id = id; 
			fbJs.async = true;
			fbJs.src = "//connect.facebook.net/en_US/sdk.js";

			fbJs.onload = function() {
				FB.init({ 
					appId: fbKey,
					status: true, 
					cookie: true, 
					xfbml: true,
					version: fbApiV
				});
	        };

			ref.parentNode.insertBefore(fbJs, ref);
		},
		setGoogleKey: function(value){
			googleKey = value;
			var d = document, gJs, ref = d.getElementsByTagName('script')[0];
			gJs = d.createElement('script');
			gJs.async = true;
			gJs.src = "//apis.google.com/js/platform.js"

			gJs.onload = function() {
				var params ={
					client_id: value,
					scope: 'email'
				}
				gapi.load('auth2', function() {
        			gapi.auth2.init(params);
      			});
		    };

		    ref.parentNode.insertBefore(gJs, ref);
		},

		$get: function(){
			return{
				fbKey: fbKey,
				googleKey: googleKey,
						
			}
		}
	}
});




socialLogin.directive("gLogin", ['$rootScope', 'social',
	function($rootScope, social){
	return {
		restrict: 'EA',
		scope: {},
		replace: true,
		link: function(scope, ele, attr){
			ele.on('click', function(){
				var fetchUserDetails = function(){
					var currentUser = scope.gauth.currentUser.get();
					var profile = currentUser.getBasicProfile();
					var idToken = currentUser.getAuthResponse().id_token;
					var accessToken = currentUser.getAuthResponse().access_token;
					return {
						token: accessToken,
						idToken: idToken, 
						name: profile.getName(), 
						email: profile.getEmail(), 
						uid: profile.getId(), 
						provider: "google", 
						imageUrl: profile.getImageUrl()
					}
				}
		    	if(typeof(scope.gauth) == "undefined")
		    		scope.gauth = gapi.auth2.getAuthInstance();
			
					scope.gauth.signIn({ prompt: 'select_account' }).then(function(googleUser){

						
						$rootScope.$broadcast('event:google-sign-in-success', fetchUserDetails());
					}, function(err){
						alert("Error to fetch data from google.try after some time")
					});
				
	        	
	        });
		}
	}
}]);

socialLogin.directive("fbLogin", ['$rootScope', 'social',  '$q',
 function($rootScope, social,  $q){
	return {
		restrict: 'EA',
		scope: {},
		replace: true,
		link: function(scope, ele, attr){
			ele.on('click', function(){
				var fetchUserDetails = function(){
					var deferred = $q.defer();
					FB.api('/me?fields=name,email,picture', function(res){
						if(!res || res.error){
							deferred.reject('Error occured while fetching user details.');
						}else{
							deferred.resolve({
								name: res.name, 
								email: res.email, 
								uid: res.id, 
								provider: "facebook", 
								imageUrl: res.picture.data.url
							});
						}
					});
					return deferred.promise;
				}
				FB.getLoginStatus(function(response) {
					if(response.status === "connected"){
						fetchUserDetails().then(function(userDetails){
							userDetails["token"] = response.authResponse.accessToken;
							$rootScope.userdata=userDetails
							
							$rootScope.$broadcast('event:fb-sign-in-success', userDetails);
						});
					}else{
						FB.login(function(response) {
							if(response.status === "connected"){
								fetchUserDetails().then(function(userDetails){
									userDetails["token"] = response.authResponse.accessToken;
									
									$rootScope.$broadcast('event:fb-sign-in-success', userDetails);
								});
							}
						}, {scope: 'email', auth_type: 'rerequest'});
					}
				});
			});
		}
	}
}]);