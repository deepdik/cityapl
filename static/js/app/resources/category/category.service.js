'use strict';

angular.module('category.services').
	factory('Category',function($resource){
		var url = 'api/v1/cityapl/categories/'

		var categoryQuery = {
			method : "GET",
			params : {},
			isArray: true,
			cache: true,
		}
		var subcategoryQuerry = {
			url : url+':id/',
			method : 'GET',
			params : {'id' :'@id'}
		}
		return $resource(url, {}, {
   		 query : categoryQuery
  		});
	});