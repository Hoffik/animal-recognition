
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

// Common Ctrl functions
app.factory("AnimalsUtils", function($http, $log) {
    
    var AnimalsUtils = {
        get: function(url, id) {
            $http.get(url + id + '/').then(function(response){response.data});
        },
    };
    return AnimalsUtils;
});


app.controller('ProjectsCtrl', function($scope, $filter, $log, $http, AnimalsUtils) { 

    $scope.loadProjects = function() {
        $http.get('/rest_api/projects/').then(function(response) {
            $scope.projects = response.data;
        });
    };

    $scope.loadProjects();
});