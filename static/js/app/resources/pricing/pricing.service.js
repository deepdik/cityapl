'use strict';

angular.module('pricing.services').
	factory('Pricing',function($resource){
		var url = 'api/v1/cityapl/pricing/'

		var pricingQuery = {
			url : url + ":slug/",
			method : "GET",
			params : {'slug' :'@slug'},
			isArray: true,
			cache: false,
		}
		return $resource(url, {}, {
   		 query : pricingQuery
  		});
	});