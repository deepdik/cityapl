'use strict';

angular.module('feedback.services').
	factory('Feedbacks',function($resource,$cookies){
		var url = 'api/v1/cityapl/feedback/'
		var feedbackCreate = {
			url : 'api/v1/cityapl/feedback/add/',
			method : 'POST',
		}
		return {
			 foo: function(token){
				return $resource(url,{},{
					create:{
						url : 'api/v1/cityapl/feedback/add/',
						method : 'POST',
						headers:{
							'Authorization': 'JWT ' + token
						}
					}
				});
			} 
		}
	});



// 	'use strict';

// angular.module('feedback.services').
// 	factory('Feedbacks',function($resource,$cookies){
// 		var url = 'api/v1/cityapl/feedback/'

// 		var feedbackCreate = {
// 			url : 'api/v1/cityapl/feedback/add/',
// 			method : 'POST',
// 		}
 		
// 		// var subcategoryQuerry = {
// 		// 	url : url+':id/',
// 		// 	method : 'GET',
// 		// 	params : {'id' :'@id'}
// 		// }
// 		console.log(feedbackCreate)
// 		return $resource(url, {}, {
//    		 create : feedbackCreate
//   		});
// 	});