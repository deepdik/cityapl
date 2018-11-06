'use strict';

angular.module('cityapl').
	config(
		function(socialProvider,$locationProvider,$routeProvider,$mdThemingProvider,$resourceProvider){
		$resourceProvider.defaults.stripTrailingSlashes = false;
		$locationProvider.html5Mode({enabled:true})
		$routeProvider.
			when("/",{
				template:"<category-list></category-list>"
			}).
			when("/category/:id",{
				template:"<subcategory-list></subcategory-list>"
			}).
			when("/:subcatid/shops",{
				template:"<shop-list></shops-list>"
			}).
			when("/shop/:slug",{
				template:"<shop-detail></shop-detail>"
			}). //implementingg searching and listing of shops from same component
			when("/search/:search",{
				template:"<shop-list></shops-list>"
			}).when("/changepassword",{
				template:"<change-password></change-password>"
			}).
			when("/chat/dashboard",{
				template:"<chat-dashboard></chat-dashboard>"
			}).
			when("/chat/dialog/:username",{
				template:"<chat-dialog></chat-dialog>"
			}).
			otherwise({
				template:"NOT FOUND"
			});

		$mdThemingProvider.
			theme('default').
			primaryPalette('teal').
			accentPalette('orange');

			socialProvider.setGoogleKey("239012674449-gqhifoaqkkd638dlso24gptjjtv8q0lt.apps.googleusercontent.com");            
            socialProvider.setFbKey({appId: "550373872014486", apiVersion: "v2.11"});
    


		});