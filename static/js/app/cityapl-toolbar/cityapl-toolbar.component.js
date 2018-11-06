'use strict';

angular.module('cityaplToolbar').
	component('cityaplToolbar',{
		templateUrl : 'api/templates/cityapltoolbar.html',
		controller : function($cookies,
            $http,
            $location,
            $scope,
            $rootScope,
            $mdSidenav,
            $mdMedia,
            $mdDialog,
            $mdMenu,
            $route,
            $window,
            Category,
                      
            ){
			$scope.title = "assadasd"
			$scope.city = "SELECT CITY"
			$scope.userLoggedIn = false
            var token = $cookies.get('token')
                if(token){
                    var req = {
                    method : 'POST',
                    url : 'api/token/verify/',
                    data : {"token":token},
                    headers : {}
                    }
                    $http(req).then(function success(response){
                        $scope.userLoggedIn = true    
                    },
                    function error(response){
                        $scope.userLoggedIn = false
                        if(response.status=401){
                            $cookies.remove('token')
                            $route.reload();
                        }
                    })
                }else{
                    $scope.userLoggedIn = false
                }
			$scope.$watch(function(){
				var token = $cookies.get('token')
				if(token){
					$scope.userLoggedIn = true
                    $scope.username = $cookies.get('username')
				}else{
					$scope.userLoggedIn = false
				}
			})
            $scope.doSearch = function(selectedItem){
                var search=selectedItem
                $location.path('/search/'+search)
            }
	        $scope.toogleSideNav = function () {36
	            $mdSidenav('catNav').toggle();
	        };
            $scope.closeSidenav =function () {
                $mdSidenav('catNav').close(100);
            };
	        $scope.searchBox = false
	        	$scope.setSearchBox = function () {
	            $scope.searchBox = true;
	        };
	        $scope.resetSearchBox = function () {
	            $scope.searchBox = false;
	        };
	        
	        Category.query({},
				function(data){
					$scope.dataSet = data;
			},
			function(error){
				console.log(error)
			});

			$scope.showCityDialog = function (ev) {
	       //     var fullscreenb = ($mdMedia('sm') || $mdMedia('xs')) &&  ($mdMedia('xs') || $mdMedia('sm'));
	            var dialogConf = {
	                controller:DialogCityController,
	                templateUrl:'api/templates/dialogs/dialogCityTemplate.html',
	                parent:document.getElementsByTagName("body"),
	                targetEventtr: ev,
	                fullscreen:true,
	                clickOutsideToClose:true
	            };
	            $mdDialog.show(dialogConf).then(function(city,citySlug){
	                $scope.city = city;
	                $scope.citySlug = citySlug;
	            });
        	};

        	$scope.showAccountsDialog = function(ev,flag){
	            $rootScope.flagLogin = flag;


	     //       var fullscreenb = ($mdMedia('sm') || $mdMedia('xs')) &&  ($mdMedia('xs') || $mdMedia('sm'));
	            var dialogConf ={
	                controller:DialogAccountsController,
	                templateUrl:'api/templates/dialogs/dialogAccountsTemplate.html',
	                parent:document.getElementsByTagName("body"),
	                targetEvent: ev,
	                fullscreen:true,
	                clickOutsideToClose:true
	            }
	            $mdDialog.show(dialogConf).then(function(){
                    
            	})
        	}


            $scope.showFreeListingDialog = function (ev) {
                var dialogConf = {
                    controller:dialogFreeListingController,
                    templateUrl:'api/templates/dialogs/dialogFreeListing.html',
                    parent:document.getElementsByTagName("body"),
                    targetEventtr: ev,
                    fullscreen:true,
                    clickOutsideToClose:true
                };
                $mdDialog.show(dialogConf).then(function(){
                    console.log('dialog success')
                });
            };

            var cityID = $cookies.get('city')
            if(cityID){
                $scope.city = $cookies.get('cityName')
            }else{
                var fullscreenb = ($mdMedia('sm') || $mdMedia('xs')) &&  ($mdMedia('xs') || $mdMedia('sm'));
                var dialogConf = {
                    controller:DialogCityController,
                    templateUrl:'api/templates/dialogs/dialogCityTemplate.html',
                    parent:document.getElementsByTagName("body"),
                    fullscreen:fullscreenb,
                    clickOutsideToClose:false
                };
                    $mdDialog.show(dialogConf).then(function(city,citySlug){
                    $scope.city = city;
                    $scope.citySlug = citySlug;
                });
            }
            
		}
	});

function DialogCityController($scope, $mdDialog,$http,$cookies,$route,City) {
    City.query({},function(data){
        $scope.cityList = data
    })

    $scope.hide = function() {
        $mdDialog.hide();
    };
    $scope.cancel = function() {
        $mdDialog.cancel();
    };
    $scope.city = function(city,cityId){
        $cookies.put('city',cityId)
        $cookies.put('cityName',city)
        $route.reload();
        $mdDialog.hide(city,cityId);
    };
    
}

function dialogFreeListingController($mdDialog,$scope,$http){
    $scope.loading = false
    $scope.hide = function() {
        $mdDialog.hide();
    };
    $scope.listShopQuerry = function(data){
        console.log(data)
        $scope.loading = true
        var config = {
            method :"POST",
            url : 'api/v1/cityapl/freelist/',
            data:data,
            headers:{}
        }
        $http(config).then(function successCallBack(response){
            $scope.loading = false
            // console.log(response)
            $mdDialog.hide();
        },function errorCallback(response){
            $scope.loading = false
            // console.log(response)
            $mdDialog.hide();
        })

    }
    
}
function DialogAccountsController(social,$cookies,$http,$mdToast,$scope,$rootScope,$route,$mdDialog) {
        $scope.loading = false
        $scope.flag = $rootScope.flagLogin
        $scope.hide = function() {
            $mdDialog.hide();
        }
       
        $scope.cancel = function() {
            $mdDialog.cancel();
        }
        // $scope.city = function(city,citySlug) {
        //     $mdDialog.hide(city,citySlug);
        // };
        $scope.resetFlag = function () {
            $scope.flag = false;
        }
       
        $scope.setFlag = function () {
            $scope.flag = true;
        }
         

        //login stuff

        var loginUrl = 'api/v1/users/login/'
        $scope.user = {

        }

        var token = $cookies.get('token')
        if (token){
        	$cookies.remove('token')
            $route.reload();
        }

        $scope.doLogin = function(user){
            $scope.loading = true
        	$scope.loginPasswordError = ""
            $scope.loginNonFieldError = ""
            $scope.loginUsernameError = ""
        	var req = {
        		method : 'POST',
        		url : loginUrl,
        		data : {
        			username : user.username,
        			password : user.password
        		},
        		headers: {}
        	}
        	var reqResp = $http(req)

        	reqResp.success(function(r_data,r_status,r_headers,r_config){
        	//	console.log(r_data.token)
        		$cookies.put('token',r_data.token)
        		$cookies.put('username',r_data.username)
        		var msz = 'Successfully logged in as '+r_data.username
                
                $mdToast.show(
                    $mdToast.simple()
                    .textContent(msz)
                    .hideDelay(3000)
                );
                $route.reload()
                $scope.loading = false
        		$mdDialog.hide()
        	})
        	reqResp.error(function(e_data,e_status,e_headers,e_config){
                $scope.loading = false
                if (e_data.password){
                    $scope.loginPasswordError = e_data.password[0]
                }
                if (e_data.username){
                    $scope.loginUsernameError = e_data.username[0]
                }
                if(e_data.non_field_errors){
                    $scope.loginNonFieldError = e_data.non_field_errors[0]

                    $mdToast.show(
                        $mdToast.simple()
                        .textContent(e_data.non_field_errors[0])
                        .position('top')
                        .hideDelay(4000)
                    );
                }                
        	})
        }




// fb login 

$rootScope.$on('event:fb-sign-in-success', function(event, userDetails){
         $scope.loading=true     
        $scope.userDetails=userDetails.token
       
    if (!event.defaultPrevented) {
        event.defaultPrevented = true;
        $scope.Error=""
        $cookies.remove('token')
        $cookies.remove('username')
        var url='api/v1/users/rest-auth/facebook/'
        var reqConfig={
        method:"POST",
        url:url,
        data:{
            access_token:$scope.userDetails,                       

            },
             headers:{}
            }

            var reqResp=$http(reqConfig)
            reqResp.success(function(r_data){                                        
                
                $cookies.put('token',r_data.token)
                $cookies.put('username',r_data.user.first_name)
                var msz = 'Successfully logged in as '+r_data.user.first_name  
               
                $mdToast.show(
                    $mdToast.simple()
                    .textContent(msz)
                    .hideDelay(4000)
                );
                $route.reload()
               $scope.loading=false
                $mdDialog.hide()
                  
 
            })

            reqResp.error(function(e_data){
              $scope.loading=false
               
                 if(e_data.non_field_errors){
                    $scope.Error =e_data.non_field_errors[0]
                    $scope.loading=false
                    alert($scope.Error)

                  }
                 if(!e_data.non_field_errors){
                    $scope.loading=false
                    alert("Something went wrong. Pls try after sometime")           
                 }
                       // $mdDialog.hide();

                  })            
    }
            

    });
    
      
//goole login

$rootScope.$on('event:google-sign-in-success', function(event, userDetails){
   $scope.loading=true
    if (!event.defaultPrevented) {
        event.defaultPrevented = true;
         $scope.Error=""
    $scope.loading=true
    $cookies.remove('token')
    $cookies.remove('username')   
    var url='api/v1/users/rest-auth/google/'
    var reqConfig={
        method:"POST",
        url:url,
        data:{
            access_token:userDetails.token,                       

            },
             headers:{}
            }

            var reqResp=$http(reqConfig)
            reqResp.success(function(r_data){                               
               $cookies.put('token',r_data.token)
                $cookies.put('username',r_data.user.first_name)
                var msz = 'Successfully logged in as '+r_data.user.first_name  
                
                $mdToast.show(
                    $mdToast.simple()
                    .textContent(msz)
                    .hideDelay(4000)
                );
                $route.reload()
                $scope.loading=false
                $mdDialog.hide()
                   
            })

            reqResp.error(function(e_data){                    
                 $scope.loading=false
                 if(e_data.non_field_errors){
                    $scope.Error = e_data.non_field_errors[0]
                      $scope.loading=false
                    alert($scope.Error)
                  }
                 if(!e_data.non_field_errors){
                      $scope.loading=false
                    alert("Something went wrong. Pls try after sometime")           
                 }
                        // $mdDialog.hide();


                  })
        }
      
  } )
 
    // Forget password

            $scope.forgetPassword=function(data){
                   $scope.data={}             
                  $scope.loading=true
                  $scope.resetPassError=""
                  $scope.errorMsg=false
                   $scope.successMsg=false
                  var forgetPassUrl ='/api/v1/users/password/reset/'
                  $scope.data={}
                
                  var reqConfig={
                  method:"POST",
                  url:forgetPassUrl ,
                  data:{
                       email: data.email,            
                  },
                  headers:{}
            }

              var reqResp=$http(reqConfig)
            reqResp.success(function(r_data,r_status,r_headers,r_config){              
                      $scope.loading=false                    
                     $scope.successMsg=true                                     

            })

            reqResp.error(function(e_data,e_status,e_headers,e_config){
                  $scope.loading=false 
                   console.log(e_data)               
                  if(e_data.email){
                    $scope.resetPassError = e_data.email[0]
                  }
                 if(!e_data.email){
                    $scope.errorMsg=true            
                 }

                  })                             
            }

//signup-----------------

        var signUpUrl = '/api/v1/users/register/'
        $scope.doSignUp = function(user){
            $scope.loading = true
            $scope.signUpPasswordError = ""
            $scope.signUpUsernameError = ""
            $scope.signUpEmailError = ""
            $scope.signUpNonFieldError = ""
            var req = {
                method : 'POST',
                url : signUpUrl,
                data : {
                    username : user.userName,
                    email : user.email,
                    password : user.password
                },
                headers : {}
            }
            var reqResp = $http(req)
            reqResp.success(function(r_data,r_status,r_headers,r_config){
            //  console.log(r_data.token)
            //    $cookies.put('token',r_data.token)
                $cookies.put('username',r_data.username)
                var msz = r_data.username + ' registered Successfully. Please verify your email now'
                $mdToast.show(
                    $mdToast.simple()
                    .textContent(msz)
                    .hideDelay(4000)
                );
                $scope.loading = false
                $route.reload()
                $mdDialog.hide()
            })
            reqResp.error(function(e_data,e_status,e_headers,e_config){
                $scope.loading = false
                if (e_data.password){
                    $scope.signUpPasswordError = e_data.password[0]
                }
                if(e_data.username){
                    $scope.signUpUsernameError = e_data.username[0]
                }
                if(e_data.email){
                    $scope.signUpEmailError = e_data.email[0]
                }
                if(e_data.non_field_errors){
                    $scope.signUpNonFieldError = e_data.non_field_errors[0]

                $mdToast.show(
                    $mdToast.simple()
                    .textContent(e_data.non_field_errors[0])
                    .position('top')
                    .theme('error-toast')
                    .hideDelay(4000)
                );
                }
                // $scope.loginPasswordError = e_data.password
                // $scope.loginUsernameError = e_data.username
                // $scope.loginUsernameError = e_data.email
                // $scope.loginNonFieldError = e_data.non_field_errors
            }



        )}


  }


