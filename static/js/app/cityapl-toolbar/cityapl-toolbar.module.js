'use strict';

angular.module('cityaplToolbar',['category.services','city.services'])
.controller('MdAutocompleteBugController', function($scope, $cookies,$q,$http, $timeout) {
           var subcat =0
           var cityId=0
          
          var token = $cookies.get('token')
            if($cookies.get('city')){
                cityId = $cookies.get('city');
            }


            console.log(cityId)

  

        this.getMatches = function(searchText) {

         var  url= 'api/v1/cityapl/'+cityId+'/'+subcat+'/shops/?ordering=-likes&search='+searchText+''
          console.log(url)

          function getState(searchText){
          console.log(searchText)
         return $http({
            method: 'GET',
            url : url
              
            
        });
        }
           var a=getState().then(function successCallback(response){
            $scope.products = response.data;
            console.log($scope.products)

        }, function errorCallback(response){
            alert('Sorry!! Search box is not working due to some problem')
            
        });
 
            console.log(searchText)
            $scope.name=$scope.products
            console.log($scope.name)

            return $scope.products 

    
        }
    


     
     

    




    })

