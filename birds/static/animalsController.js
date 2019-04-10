
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

    $scope.isProjectOwner = function(user, project) {
        return project.owners.includes(user);
    }
});

app.controller('ProjectDetailCtrl', function($scope, $filter, $log, $http) { 

    $scope.getProject = function(dir) {
        $http.get('/rest_api/projects/' + dir + '/').then(function(response) {
            $scope.project = response.data;
            $scope.new_user_role = "layman";
        }).catch(function(error) {
            console.log("Error in getProject processing", error);
            $scope.error_message = error.data.detail;
        });
    };

    // $http.get("url").
    // then(someProcessingOf).
    // catch(function(e){
    //    console.log("got an error in initial processing",e);
    //    throw e; // rethrow to not marked as handled, 
    //             // in $q it's better to `return $q.reject(e)` here
    // }).then(function(res){
    //     // do more stuff
    // }).catch(function(e){
    //     // handle errors in processing or in error.
    // });


    // updateProject(project)


    $scope.addRight = function() {
        $log.log("ADD - ID: " + $scope.new_user.id + " name: " + $scope.new_user.username + " " + $scope.new_user.email);
        var data = $.param({
            project: $scope.project.id,
            user: $scope.new_user.id,
            role: $scope.project.role_names.indexOf($scope.new_user_role),
        });
        var config = {
            headers : {
                'Content-Type': 'application/x-www-form-urlencoded;'
            }
        }
        return $http.post('/rest_api/rights/', data, config).then(function(response) {
            angular.extend( $scope.new_user, response);
        }, function(response) {
            $log.log("UserUtils create error " + response.status);
            //handleErrors(response, status, errors);
        }).then(function() {
            $scope.getProject($scope.project.directory);
        });
    };

    $scope.updateRight = function(right) {
        $log.log("ID: " + right.id + " role: " + right.role + " user: " + right.user);
        right.role = $scope.project.role_names.indexOf(right.role_name);
        $log.log("ID: " + right.id + " role: " + right.role + " " + right.role_name);
        var data = $.param({
            project: $scope.project.id,
            user: right.user,
            role: right.role,
            // "role_name": right.role_name
        });
        var config = {
            headers : {
                'Content-Type': 'application/x-www-form-urlencoded;'
            }
        }
        return $http.put('/rest_api/rights/' + right.id + '/', data, config).then(function(response) {
            angular.extend(right, response);
        }, function(response) {
            $log.log("Method updateRight error " + response.status);
            //handleErrors(response, status, errors);
        }).then(function() {
            $log.log("then function " + right.role + " " + right.project);
            $scope.getProject(right.project_dir);
        });
    };

    $scope.deleteRight = function(right) {
        $log.log("DELETE - ID: " + right.id + " role: " + right.role + " " + right.role_name);
        return $http.delete('/rest_api/rights/' + right.id + '/').then(function() {
            $log.log("then function " + right.role + " " + right.project);
            $scope.getProject(right.project_dir);
        });
    };
    
    // $scope.getProject($scope.project_id);

    // get: function(url, id) {
    //     $http.get(url + id + '/').then(function(response){response.data});
    // },

    
});