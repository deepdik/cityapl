'use strict';

angular.module('categoryList').
	component('categoryList',{
//		templateUrl: 'api/templates/cityaplhome.html',
		template :"<ng-include src='getTemplateUrl()'/>",
		controller: function($scope,$http,Category){
			$scope.loading = true
			$scope.categories = null
			$scope.pageError = false
			$scope.pageNotFound = false

			$scope.getTemplateUrl = function(){
				if ($scope.loading && $scope.shop == null) {
                    return '/api/templates/loader/listloader.html'
                } else if ($scope.notFound) {
                     return '/api/templates/error/404.html'
                } else if ($scope.pageError) {
                    return '/api/templates/error/500.html'
                }else {
                    return '/api/templates/cityaplhome.html'
                }
			}
			Category.query({},
				function(data){
					$scope.categories = data;
					$scope.loading = false
			},
			function(error){
				$scope.loading = false
				if(responseError.status == 500){
					$scope.pageError = true;
				}else if(responseError.status == 404){
					$scope.notFound = true
				}
			});
		}
	});