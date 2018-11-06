'use strict';

angular.module('subcategory.services').
	factory('SubCategory',function($resource){
		var url = 'api/v1/cityapl/subcategories/'
		var subCategoryQuery = {
			method : "GET",
			params : {},
			isArray: true,
			cache: true,
		}
		return $resource(url,{},{
			query : subCategoryQuery
		});
	});