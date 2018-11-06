'use strict';

angular.module('chatDashboard').
	component('chatDashboard',{
		templateUrl :'api/templates/chat/chat_dashboard.html',
	// template:"<ng-include src='getTemplateUrl()'/>",
		controller : function($scope,$http,$cookies){
        

                 
        $scope.main_user=$cookies.get('username')
        var dashboardUrl = 'api/chat/dialogs/'
        
        	var req = {
        		method : 'GET',
        		url : dashboardUrl,       		
        		headers: {}
        	}
        	var reqResp = $http(req)

        	reqResp.success(function(r_data,r_status,r_headers,r_config){
        		console.log(r_data)
        		 var imagePath = 'media/svg/chat_user.svg'; 
        		$scope.opponent_username=r_data
                $scope.main_user=$cookies.get('username')
    })

        	reqResp.error(function(e_data,e_status,e_headers,e_config){
        		console.log(e_data)
                // $scope.loading = false
                // if (e_data.password){
                //     $scope.loginPasswordError = e_data.password[0]
                // }
                // if (e_data.username){
                //     $scope.loginUsernameError = e_data.username[0]
                // }
                // if(e_data.non_field_errors){
                //     $scope.loginNonFieldError = e_data.non_field_errors[0]

                //     $mdToast.show(
                //         $mdToast.simple()
                //         .textContent(e_data.non_field_errors[0])
                //         .position('top')
                //         .hideDelay(4000)
                //     );
                // }                
        	})
        

			 var dashboardUrl = 'api/chat/dialogs/notifications/'
        
            var req = {

                method : 'GET',
                url : dashboardUrl,             
                headers: {}
            }

            var reqResp = $http(req)
            reqResp.success(function(r_data,r_status,r_headers,r_config){
                console.log(r_data)
                 var imagePath = 'media/svg/chat_user.svg'; 
                $scope.unseen_msg = r_data
                console.log($scope.unseen_msg.dialog)
                if($scope.unseen_msg.dialo){

                }
    })

            reqResp.error(function(e_data,e_status,e_headers,e_config){
                console.log(e_data)
                              
            })
			



		}


	})


