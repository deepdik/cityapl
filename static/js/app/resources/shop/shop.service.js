'use strict';

angular.module('shop.services').
	factory('Shops',function($resource){
		var url = 'api/v1/cityapl/shops/'
		var shopQuery = {
			url:'api/v1/cityapl/:cityId/:subCategory/shops/',
			method : 'GET',
			params : {'cityId':'@cityId'},
			isArray:true,
			cache:true
		}
		var shopGet = {
			url : url + ':slug/',
			method : 'GET',
			params : {'slug':'@slug'},
			isArray:false,
			cache:true
		}
		return $resource(url,{},{
				query:shopQuery,
				get:shopGet,
			});
	});