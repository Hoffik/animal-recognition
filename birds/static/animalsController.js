
var app = angular.module('animalsApp', []); //'ngResource'

// https://www.consolelog.io/django-csrf-token-with-angularjs
app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);
// Allow django templates and angular to co-exist
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

// // Global scope variables
// app.run(function($rootScope, $http, ){
//     $rootScope.getLoggedUser = function() {
//         $http.get('/auth/logged_user/').then(function (response) {
//             $rootScope.loggedUser = response.data;
//         });
//     }
//     $rootScope.getLoggedUser();
// })

// // Common Ctrl functions
// app.factory("AnimalsUtils", function($http, $log) {
    
//     var AnimalsUtils = {
//         get: function(url, id) {
//             $http.get(url + id + '/').then(function(response){response.data});
//         },
//     };
//     return AnimalsUtils;
// });


app.controller('ProjectListCtrl', function($scope, $filter, $log, $http) { 

    $scope.loadProjects = function() {
        $http.get('/rest_api/projects/').then(function(response) {
            $scope.projects = response.data;
        });
    };

    $scope.loadProjects();
});

app.controller('ProjectDetailCtrl', function($scope, $filter, $log, $http) { 

    $scope.getProject = function() {
        $http.get('/rest_api/projects/' + id + '/').then(function(response) {
            $scope.project = response.data;
        });
    };

    $scope.getProject();

    // get: function(url, id) {
    //     $http.get(url + id + '/').then(function(response){response.data});
    // },
    // update: function(url, obj, errors) {
    //     //$log.log(obj.text + " " + obj.date_time + " " + obj.calories + " " + obj.user);
    //     var data = $.param({
    //         text: obj.text,
    //         date: obj.date,
    //         time: obj.time,
    //         calories: obj.calories,
    //         user: obj.user
    //     });
    //     var config = {
    //         headers : {
    //             'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
    //         }
    //     }
    //     return $http.put(url + obj.id + '/', data, config).
    //     then(function(response, status, headers, config) {
    //         angular.extend(obj, response);
    //     }, function(response, status, headers, config) {
    //         $log.log("MealUtils update error " + response.status);
    //         //handleErrors(response, status, errors);
    //     });
    // },
    // del: function(url, obj) {
    //     return $http.delete(url + obj.id + '/');
    // }

    // $scope.updateMeal = function(meal) {
    //     MealUtils.update('/meals/', meal, $scope.errors).then(function() {
    //         $scope.loadMeals();
    //     });
    // };

    // $scope.deleteMeal = function(meal) {
    //     MealUtils.del('/meals/', meal).then(function() {
    //         $scope.loadMeals();
    //     });
    // };
});