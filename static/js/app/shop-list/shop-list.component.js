'use strict';

angular.module('shopList').
	component('shopList',{
//		templateUrl:'api/templates/cityapllistshops.html',
		template: "<ng-include src='getTemplateUrl()'/>",
		controller:function($cookies,$scope,$http,$mdToast,$route,$routeParams,Shops){
			$scope.loading = true;
			$scope.listLoader = false
			$scope.pageError = false
			$scope.pageNotFound = false
            $scope.shops = null;
            $scope.getTemplateUrl = function(){
                if ($scope.loading && $scope.shops == null) {
                    return '/api/templates/loader/listloader.html'
                }else if($scope.pageError){
                	return '/api/templates/error/500.html'
                }else if($scope.pageNotFound){
                	return '/api/templates/error/404.html'
                }
                else {
                    return 'api/templates/cityapllistshops.html'
                }
            }

			var subcat = 0
			var cityId = 0
			var search = ""
			var isSearchPage = false
			$scope.isSearchPage = false
			if($routeParams.subcatid){
				subcat  = $routeParams.subcatid
			}else{
				search = $routeParams.search
				isSearchPage = true
				$scope.isSearchPage = true
			}

			var token = $cookies.get('token')
			if($cookies.get('city')){
				cityId = $cookies.get('city');
			}
			if(token){
					var config = {'ordering':'-likes'}
                	getShopsAuthenticatedUser(token,config)
                }else{
                	var config = {'cityId':cityId,'subCategory':subcat,'ordering':'-likes'}
                	getShops(config)
            }
			$scope.vote = function(shopId,index,up){
				var token = $cookies.get('token')
				if(token){
					$scope.listLoader = true
					var config = {
						method : 'POST',
						url : 'api/v1/cityapl/vote/',
						data : {
							liked:up,
							shop :shopId
						},
						headers : {
							'Authorization': 'JWT  ' + token
						}
					}
					$http(config).then(function successCallback(response) {
						$scope.listLoader = false
						var r_data = response.data;
		                var likeCnt = r_data['likeCnt']
		                var dislikeCnt = r_data['dislikeCnt']
		                if(likeCnt == 1){
		             		$scope.shops[index]['isLiked'] = 1
		                }else if(dislikeCnt==1){
		                	$scope.shops[index]['isLiked'] = -1
		                }else{
		                	$scope.shops[index]['isLiked'] = 0
		                }
						$scope.shops[index]['likes'] += r_data['likeCnt']
						$scope.shops[index]['dislikes'] += r_data['dislikeCnt']
	        	}, function errorCallback(response) {
				    $scope.listloader = false
				    $scope.loading = false
				    if(response.status == 500){
						$scope.pageError = true;
					}else if(response.status == 404){
						$scope.notFound = true
					}else if(response.status == 401){
						$cookies.remove('token')
						$route.reload();
					}
				  });
		        	
				}else{
					$mdToast.show(
		                    $mdToast.simple()
		                    .textContent("Please Login to vote")
		                    .hideDelay(3000)
		                );
				}
			}

			//order by distance name will be chande later
			$scope.sortByDistance = function(){
				if (navigator.geolocation) {
					navigator.geolocation.getCurrentPosition(distance,function(error){
						var msz = ""
					    switch(error.code) {
					        case error.PERMISSION_DENIED:
					            msz = "Please allow Cityapl to access your location"
					            break;
					        case error.POSITION_UNAVAILABLE:
					            msz = "Sorry we can't find your location."
					            break;
					        case error.TIMEOUT:
					            msz = "It's taking too longer to fetch your location. Please try again"
					            break;
					        case error.UNKNOWN_ERROR:
					            msz = "An unknown error occurred."
					            break;
					    	}
					    	$mdToast.show(
		                    $mdToast.simple()
		                    .textContent(msz)
		                    .hideDelay(3000)
		                );
						});
				}else{
					$mdToast.show(
		                    $mdToast.simple()
		                    .textContent("Sorry Location is not supported by your browser")
		                    .hideDelay(3000)
		                );
				}
			}

			$scope.orderByName = function(){
				var token = $cookies.get('token')
				if(token){
					var config={'ordering':'shopName'}
					getShopsAuthenticatedUser(token,config)
				}else{
					var config={'cityId':cityId,'subCategory':subcat,'ordering':'shopName'}
					getShops(config)
				}
			}

			$scope.orderByLikes = function(){
				var token = $cookies.get('token')
				if(token){
					var config={'ordering':'-likes'}
					getShopsAuthenticatedUser(token,config)
				}else{
					var config={'cityId':cityId,'subCategory':subcat,'ordering':'-likes'}
					getShops(config)
				}
			}

			function distance(position){
				$scope.listLoader = true
				var token = $cookies.get('token')
				var header = {}
				var point = position.coords.longitude + ',' + position.coords.latitude;
                var dist = 40000
                if(token){
                	var config = {'dist':500000,'point':point}
                	getShopsAuthenticatedUser(token,config)
                }else{
                	var config = {'cityId':cityId,'subCategory':subcat,'dist':500000,'point':point}
                	getShops(config)
                }
			}

			function getShops(config){
				$scope.listLoader = true
				if(isSearchPage){
					config.search = search
				}
				Shops.query(config,function(data){
					$scope.listLoader = false
					$scope.shops = data;
				},function(errorData){
					$scope.listLoader = false
					console.log(errorData);
				})
			}

			function getShopsAuthenticatedUser(token,queryParams){
				if(isSearchPage){
					queryParams.search = search
				}
				var config = {
					method : 'GET',
					url : 'api/v1/cityapl/'+cityId+'/'+subcat+'/shops/',
					params : queryParams,
					headers : {
						'Authorization': 'JWT  ' + token
					}
				}
				$scope.listLoader = true
				$http(config).then(function successCallback(response) {
					$scope.shops = response.data
	        		$scope.listLoader = false
	        	},function errorCallback(response) {
				    $scope.listloader = false
				    $scope.loading = false
				    if(response.status == 500){
						$scope.pageError = true;
					}else if(response.status == 404){
						$scope.notFound = true
					}else if(response.status == 401){
						$cookies.remove('token')
						$route.reload();
					}
				});
			}



			$scope.share  = function(site,slug){
				if(site == "facebook"){
					var url = "https://www.facebook.com/sharer/sharer.php?u=cityapl.com/shop/" + slug
					window.location = url
				}else if(site=="twitter"){
					var url = "https://twitter.com/home?status=cityapl.com/shop/" + slug
					window.location = url
				}
		
			}
		}
	});