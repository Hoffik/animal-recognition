
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

// Global scope variables
app.run(function($rootScope) {
    $rootScope.icon_edit = "data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHfSURBVGhD7Zk7Sx1RFEavWIiPQOxNwEa7EKtoRP+H6UQSLYyNpBTBXlDsJWWwzy+I2mhlLBNIMJVWmoCKoq6PuGFzObmoA5kt7AULZs7cM+yP8xg4t5EkSZI8kOe4gJ9xCzfwLXbio+EDnuF1wV84hqFpwzUsBfCeY9gwpRA/cRLHcRH9KB1guGlWCrGNT9HzCn2YKQxDKcQVvsQSGhn73Sc1RKDVmtC06sdmXqP95osa6qYU4htqNOy+FEZrxp5ra66VUogd1JrQvP9XmF78gfZM35naaBXCKIUZQn0Yre0Un2Et3CWE0RzGX8t5rIX7hDCaw5irWAsPCSH0/Dv6fnqP3vffqRJiF32/DFGFDIG+X4aoQoZA3y9DVCFDoO+XIaqQIdD3qy2EWEFfzAW+wFaEC9GNl+gLkn/wHZYIF0L4E4ySS+gJGULMoRWko5hpPHRt0kYmbAjxEa2oZTWADgD20dp/o9ZM2BBiD62wN2q4pQ+P0J5pA7BrGSpEF/qFPoieGfTFm6FCiGG04k6wHQdwAjXNNtEHkOFCiPdoBepw7NjdlwwZQqxjqeBmNf107hQyhPA7k6lF/RW1m2nERlEfzbD0oP7uUtEamVkcQW0Aj4oOfPL3MkmSJAyNxg1x2mXbXV7r+QAAAABJRU5ErkJggg==";
});

app.controller('ProjectListCtrl', function($scope, $filter, $log, $http) { 

    $scope.loadProjects = function() {
        $http.get('/rest_api/projects/').then(function(response) {
            $scope.projects = response.data;
        });
    };

    $scope.loadProjects();

    // $scope.isProjectOwner = function(user, project) {
    //     return project.owners.includes(user);
    // }
});

app.controller('ProjectDetailCtrl', function($scope, $filter, $log, $http) { 

    $scope.updateNewUser = function(username, email, role_name) {
        if (username) {
            $scope.new_user = $scope.project.users_wo_rights.find(user_wo_rights => user_wo_rights.username === username);
        } else if (email) {
            $scope.new_user = $scope.project.users_wo_rights.find(user_wo_rights => user_wo_rights.email === email);
        } else {
            $scope.new_user_role_name = role_name
        }
    }

    $scope.getProject = function(dir) {
        $http.get('/rest_api/projects/' + dir + '/').then(function(response) {
            $scope.project = response.data;
            $scope.new_user_role = "layman";
        }).catch(function(error) {
            console.log(error.data.detail, error);
            $scope.error_message = error.data.detail;
        });
    };

    $scope.addRight = function() {
        // console.log($scope.new_user + " " + $scope.new_user_role_name);
        if (!$scope.new_user || !$scope.new_user_role_name) {
            throw "Input user name and role.";
        }
        var data = $.param({
            project: $scope.project.id,
            user: $scope.new_user.id,
            role: $scope.project.role_names.indexOf($scope.new_user_role_name),
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
            $scope.new_user = undefined;
            $scope.new_user_role_name = undefined;
        });
    };

    $scope.updateRight = function(right, role_name) {
        var data = $.param({
            project: $scope.project.id,
            user: right.user,
            role: $scope.project.role_names.indexOf(role_name),
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
});

