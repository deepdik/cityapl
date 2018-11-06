'use strict';

angular.module('subcategoryList').
	component('subcategoryList',{
	//	templateUrl :'api/templates/cityaplsubcategories.html',
	template:"<ng-include src='getTemplateUrl()'/>",
		controller : function($scope,$http,$routeParams,SubCategory){
			$scope.loading = true
			$scope.category = null
			$scope.pageError = false
			$scope.pageNotFound = false
			
			$scope.getTemplateUrl = function(){
				if($scope.loading && $scope.category==null){
					return '/api/templates/loader/listloader.html'
				}else if($scope.pageNotFound){
					return 'api/templates/error/404.html'
				}else if($scope.pageError){
					return 'api/templates/error/500.html'
				}else{
					return 'api/templates/cityaplsubcategories.html'
				}
			}

			SubCategory.query({'category':$routeParams.id},function(data){
			 	$scope.subcategories = data
			 	$scope.category = data[0].category.name
		//	 	$scope.loading = false
			},
			function(responseError){
				$scope.loading = false
				if(responseError.status == 500){
					$scope.pageError = true;
				}else if(responseError.status == 404){
		//			$scope.notFound = true
				}
			})
		}
	});