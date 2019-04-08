
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

    $scope.getProject = function(id) {
        $http.get('/rest_api/projects/' + id + '/').then(function(response) {
            $scope.project = response.data;
        });
    };

    // updateProject(project)


    // addRight(right)


    // updateRight(right)
    $scope.updateRight = function(right) {
        // $log.log("ID: " + right.id + " role: " + right.role + " " + right.role_name);
        right.role = $scope.project.role_names.indexOf(right.role_name);
        // $log.log("ID: " + right.id + " role: " + right.role + " " + right.role_name);
        var data = $.param({
            // "id": 1,
            // "user": "bert",
            // "email": "bert@sesamestreet.com",
            // "project": 1,
            // "identification_count": 2,
            "role": right.role,
            // "role_name": right.role_name
        });
        var config = {
            headers : {
                'Content-Type': 'application/x-www-form-urlencoded;'
            }
        }
        return $http.put('/rest_api/rights/' + right.id + '/', data, config).then(function(response, status, headers, config) {
            angular.extend(right, response);
        }, function(response, status, headers, config) {
            $log.log("Method updateRight error " + response.status);
            //handleErrors(response, status, errors);
        }).then(function() {
            $log.log("then function " + right.role + " " + right.project);
            $scope.getProject(right.project);
        });
    };

    // deleteRight(right)

    

    // $scope.getProject($scope.project_id);

    // get: function(url, id) {
    //     $http.get(url + id + '/').then(function(response){response.data});
    // },
    
    // del: function(url, obj) {
    //     return $http.delete(url + obj.id + '/');
    // }

    

    // $scope.deleteMeal = function(meal) {
    //     MealUtils.del('/meals/', meal).then(function() {
    //         $scope.loadMeals();
    //     });
    // };
});