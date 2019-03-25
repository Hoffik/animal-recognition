
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

// Define CRUD functions
app.factory("animalsUtils", function($http, $log) {
    
    var AnimalsUtils = {
        get: function(url, id) {
            $http.get(url + id + '/').then(function(response){response.data});
        },
    };
    return AnimalsUtils;
});

app.controller('animalsCtrl', function animalsCtrl($scope, $filter, $log, $http, animalsUtils) { 

    // Get logged user
    // $scope.getLoggedUser = function() {
    //     $http.get('/accounts/logged_user/').then(function (response) {
    //         $scope.loggedUser = response.data;
    //     }, function (reject) {
    //         $log.log("UserUtils get logged user error " + response.status);
    //     });
    // }

    // Project
    $scope.loadProjects = function() {
        $http.get('/rest_api/projects/').then(function(response) {
            $scope.projects = response.data;
        });
    };

    $scope.loadProjects();
});