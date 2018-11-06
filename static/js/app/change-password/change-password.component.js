'use strict';

angular.module('changePassword').
component('changePassword', {
    templateUrl: 'api/templates/cityaplchangepassword.html',
    controller: function($cookies,$http, $location,$mdToast,$route, $scope) {
      $scope.loading = false
      var token = $cookies.get('token')
      if(!token){
            $location.path('/')
      }
        $scope.changePassword = function(pass) {
            var token = $cookies.get('token')
            $scope.passwordError = ""
            if (token) {
                // console.log(pass)
                $scope.loading = true
                var req = {
                  method: 'PUT',
                  url: '/api/v1/users/changepassword/',
                  data: pass,
                  headers: {
                            'Authorization': 'JWT  ' + token
                        }
                  }
                  var reqResp = $http(req)
                  reqResp.success(function(r_data, r_status, r_headers, r_config) {
                        // $scope.pass.oldPassword = ""
                        // $scope.pass.newPassword = ""
                         $scope.loading = false
                        $mdToast.show(
                              $mdToast.simple()
                              .textContent("password changed successfully")
                              .hideDelay(3000)
                        );
                  })
                  reqResp.error(function(e_data,e_status,e_headers,e_config){
                     $scope.loading = false
                        if (e_data.oldPassword){
                              $scope.passwordError = e_data.oldPassword[0]
                        }
                  })
            }else {
            $location.path('/')
            }
      }
}
});