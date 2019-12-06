
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


/**
 * @this vm
 * @ngdoc controller
 * @name animalsApp.controller:ProjectListCtrl
 *
 * @description
 * Takes care of Project list application page.
 * Serves list of Projects.
 */
app.controller('ProjectListCtrl', function($scope, $filter, $log, $http) { 

    /**
     * @ngdoc method
     * @name ProjectListCtrl#loadProjects
     *
     * @methodOf
     * animalsApp.controller:ProjectListCtrl
     *
     * @summary
     * Loads Project list.
     *
     * @description
     * Loads list of animal recognition Projects.
     * 
     * @scope   {array}     projects                        List of Projects.
     * @scope   {object}    project                         Animal recognition project.
     * @scope   {number}    project.id                      Project identification. Private key.
     * @scope   {string}    project.name                    Project name.
     * @scope   {string}    project.directory               Restricted Project name suitable for url address and filepath. Unique.
     * @scope   {string}    project.current_user_right      Logged-in user Right in Project (if any).
     * @scope   {string}    project.file_type               File format of animal Records (image, audio or video).
     * @scope   {number}    project.right_count             Sum of Users with Right in Project.
     * @scope   {number}    project.tag_count               Sum of Tags in Project.
     * @scope   {number}    project.record_count            Sum of Records in Project.
     * @scope   {number}    project.identification_count    Sum of Identifications in Project. 
     */
    $scope.loadProjects = function() {
        $http.get('/rest_api/projects/').then(function(response) {
            $scope.projects = response.data;
        });
    };

    $scope.loadProjects();
});

/**
 * @this vm
 * @ngdoc controller
 * @name animalsApp.controller:ProjectTagCtrl
 *
 * @description
 * Takes care of main application page.
 * Serves a random animal Record with available Tags.
 * Saves user defined Identification.
 */
app.controller('ProjectTagCtrl', function($scope, $sce, $filter, $log, $http) {

    /**
     * @ngdoc method
     * @name ProjectTagCtrl#getRandomRecord
     *
     * @methodOf
     * animalsApp.controller:ProjectTagCtrl
     * 
     * @summary
     * Loads random animal Record from the Project.
     *
     * @description
     * Loads random animal Record (image, audio or video) from the Project.
     * Probability of record selection is based on their importance value. 
     *
     * @param   {string}    project_dir             Project directory. Unique.
     * 
     * @scope   {object}    record                  Record of animal in image, audio or video format.
     * @scope   {number}    record.id               Record identification. Private key.
	 * @scope   {string}    record.filename         Filename of the Record file stored in media folder.
     * @scope   {string}    record.filepath         Filepath and name to the Record file stored in media folder.
	 * @scope   {string}    record.filetype         Filetype of the Record file stored in media folder.
     * @scope   {number}    record.project          Record project.
     * @scope   {number}    record.project_dir      Record project directory. Unique.
     * @scope   {array}     record.project_phase    Record project phase.
     */
    $scope.getRandomRecord = function(project_dir) {
        $http.get('/rest_api/records/' + project_dir + '/random/').catch(function(error) {
            console.log(error.data.detail, error);
            $scope.error_message = error.data.detail;
        }).then(function(response) {
            $scope.record = response.data;
            $scope.record.file = $sce.trustAsResourceUrl($scope.record.file);
            $scope.getRecordTags(project_dir);
        });
    };

    /**
     * @ngdoc method
     * @name ProjectTagCtrl#getRecordTags
     *
     * @methodOf
     * animalsApp.controller:ProjectTagCtrl
     * 
     * @summary
     * Loads Tags of the given Project.
     *
     * @description
     * Loads Tags available for the given Project.
     * Tags order is defined by their weight for given Record if available.
     * Remaining Tags without weight are ordered by their prior value.
     *
     * @param   {string}    project_dir         Project directory. Private key.
     * 
     * @scope   {array}     tags                List of Tag objects.
     * @scope   {object}    tag                 Possible choice (most often animal species name) for Record Identification.
     * @scope   {number}    tag.id              Tag identification. Private key.
     * @scope   {string}    tag.name            Tag name.
     * @scope   {string}    tag.imagepath       Filepath and name to Tag image stored in media folder.
     * @scope   {number}    tag.project         Tag project.
     * @scope   {number}    tag.prior           Tag prior defining order in Tags list. 
     * @scope   {array}     tag.identifications List of executed Identifications with given Tag.
     */
    $scope.getRecordTags = function(project_dir) {
        $http.get('/rest_api/tags/' + project_dir + '/' + $scope.record.id + '/').catch(function(error) {
            console.log(error.data.detail, error);
            $scope.error_message = error.data.detail;
        }).then(function(response) {
            $scope.tags = response.data;
        });
    };

    /**
     * @ngdoc method
     * @name ProjectTagCtrl#addIdentification
     *
     * @methodOf
     * animalsApp.controller:ProjectTagCtrl
     * 
     * @summary
     * Creates new Identification.
     *
     * @description
     * Creates new Identification.
     * I.e. connects input Tag to examined Record. 
     *
     * @param   {number}    tag_id      Tag identification. Private key.
     * 
     * @return  {Object}                Created Identification.
     */
    $scope.addIdentification = function(tag_id) {
        var data = $.param({
            record: $scope.record.id,
            tag: tag_id,
            phase: $scope.record.phase,
        });
        var config = {
            headers : {
                'Content-Type': 'application/x-www-form-urlencoded;'
            }
        }
        return $http.post('/rest_api/identifications/' + $scope.record.project_dir + '/', data, config).catch(function(error) {
            console.log(error.data.detail, error);
            $scope.error_message = error.data.detail;
        }).then(function() {
            $scope.getRandomRecord($scope.record.project_dir);
        });
    }
});

/**
 * @this vm
 * @ngdoc controller
 * @name animalsApp.controller:ProjectDetailCtrl
 *
 * @description
 * Takes care of Project detail application page.
 * Serves Project details.
 * Saves Project updates.
 */
app.controller('ProjectDetailCtrl', function($scope, $filter, $log, $http) { 

    /**
     * @ngdoc method
     * @name ProjectDetailCtrl#getProject
     *
     * @methodOf
     * animalsApp.controller:ProjectDetailCtrl
     * 
     * @summary
     * Loads Project.
     *
     * @description
     * Loads Project defined by input Project directory.
     *
     * @param   {string}    dir                             Project directory. Unique.
     * 
     * @scope   {object}    project                         Animal recognition project.
     * @scope   {number}    project.id                      Project identification. Private key.
     * @scope   {string}    project.name                    Project name.
     * @scope   {string}    project.directory               Restricted Project name suitable for url address and filepath. Unique.
     * @scope   {string}    project.current_user_right      Logged-in user Right in Project (if any).
     * @scope   {string}    project.file_type               File format of animal Records (image, audio or video).
     * @scope   {number}    project.right_count             Sum of Users with Right in Project.
     * @scope   {number}    project.tag_count               Sum of Tags in Project.
     * @scope   {number}    project.record_count            Sum of Records in Project.
     * @scope   {number}    project.identification_count    Sum of Identifications in Project.
     */
    $scope.getProject = function(dir) {
        $http.get('/rest_api/projects/' + dir + '/').catch(function(error) {
            console.log(error.data.detail, error);
            $scope.error_message = error.data.detail;
        }).then(function(response) {
            $scope.project = response.data;
            $scope.new_user_role = "layman";
        });
    };

    /**
     * @ngdoc method
     * @name ProjectDetailCtrl#updateProject
     *
     * @methodOf
     * animalsApp.controller:ProjectDetailCtrl
     * 
     * @summary
     * Updates Project.
     *
     * @description
     * Updates input Project. 
     *
     * @param   {Object}    project     Project to be updated.
     * 
     * @return  {Object}                Updated Project.
     */
    $scope.updateProject = function(project) {
        var data = $.param({
            name: project.name,
        });
        var config = {
            headers : {
                'Content-Type': 'application/x-www-form-urlencoded;'
            }
        }
        return $http.put('/rest_api/projects/' + project.directory + '/', data, config).catch(function(error) {
            console.log(error.data.detail, error);
            $scope.error_message = error.data.detail;
        });
    };

    /**
     * @ngdoc method
     * @name ProjectDetailCtrl#updateNewUser
     *
     * @methodOf
     * animalsApp.controller:ProjectDetailCtrl
     * 
     * @summary
     * Updates $scope new_user information.
     *
     * @description
     * Updates $scope new_user and new_user_role_name information.
     * new_user and new_user_role_name are auxiliary objects used for creating new User Right in Project.
     *
     * @param   {string}    [username]                      new_user username.
     * @param   {string}    [email]                         new_user email.
     * @param   {string}    [role_name]                     new_user role in Project.
     * 
     * @scope   {object}    [new_user]                      Updated new_user.
     * @scope   {string}    [new_user_role_name]            Updated new_user role.
     */
    $scope.updateNewUser = function(username, email, role_name) {
        if (username) {
            $scope.new_user = $scope.project.users_wo_rights.find(user_wo_rights => user_wo_rights.username === username);
        } else if (email) {
            $scope.new_user = $scope.project.users_wo_rights.find(user_wo_rights => user_wo_rights.email === email);
        } else {
            $scope.new_user_role_name = role_name
        }
    }

    /**
     * @ngdoc method
     * @name ProjectDetailCtrl#addRight
     *
     * @methodOf
     * animalsApp.controller:ProjectDetailCtrl
     * 
     * @summary
     * Creates new User Right for Project.
     *
     * @description
     * Creates new User Right for Project.
     * Gives User Right to Tag animal Records (i.e. create Identifications) in Project (and possibly edit Project).
     * Sets auxiliary objects new_user and new_user_role_name to undefined.
     *
     * @scope   {object}    [new_user]              new_user set to undefined.
     * @scope   {string}    [new_user_role_name]    new_user role set to undefined.
     * 
     * @return  {Object}                            Created User Right.
     */
    $scope.addRight = function() {
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
        return $http.post('/rest_api/rights/', data, config).catch(function(error) {
            console.log(error.data.detail, error);
            $scope.error_message = error.data.detail;
        }).then(function() {
            $scope.getProject($scope.project.directory);
            $scope.new_user = undefined;
            $scope.new_user_role_name = undefined;
        });
    };

    /**
     * @ngdoc method
     * @name ProjectDetailCtrl#updateRight
     *
     * @methodOf
     * animalsApp.controller:ProjectDetailCtrl
     * 
     * @summary
     * Updates User Right in Project.
     *
     * @description
     * Changes User role in Project.
     *
     * @param   {object}    right       User Right to be updated.
     * @param   {string}    role_name   New User role in Project.
     * 
     * @return  {Object}                Updated User Right.
     */
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
        return $http.put('/rest_api/rights/' + right.id + '/', data, config).catch(function(error) {
            console.log(error.data.detail, error);
            $scope.error_message = error.data.detail;
        }).then(function() {
            $scope.getProject(right.project_dir);
        });
    };

    /**
     * @ngdoc method
     * @name ProjectDetailCtrl#deleteRight
     *
     * @methodOf
     * animalsApp.controller:ProjectDetailCtrl
     * 
     * @summary
     * Removes User Right from Project.
     *
     * @description
     * Removes User Right from Project.
     *
     * @param   {object}    right   User Right to be removed.
     */
    $scope.deleteRight = function(right) {
        return $http.delete('/rest_api/rights/' + right.id + '/').catch(function(error) {
            console.log(error.data.detail, error);
            $scope.error_message = error.data.detail;
        }).then(function() {
            $scope.getProject(right.project_dir);
        });
    };
});

// Global scope variables
app.run(function($rootScope) {
    $rootScope.icon_add_user = "data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAARZSURBVGhD7ZlZqFZVFMdvVpalGNlEhZkWNhA0EiFFYUT0EKQ5RKQgJT00QBFEJRFRBFI0UJYZhaL0UgSBikQTPRSFWRENVNAgNNhENNhkvx/cBYuPc+53zvnynO/h/uH3su/e+6x9915rr7W/kXGNa/g0GS6FJ+AV+ADegufhVjgRhlqT4Bb4EXb14UU4HYZOs+B9KDK6jH/gZtgDhkInwfeQjfwOVsNSuBAuAY1+DXI/eQQ618HwCYRRf8NdoJ+U6Wzo3b3roVPp0GHMTrgYqmgKvAQx9g+YCZ3oBHAHwpjroI4OgM8gxq+HTrQSwoitMAHqaj7EHO7oVGhdH0MYcaUNDWTE2g4xz2XQqvaF+LgcCU2V/exuG9qUjhkf/wuaHKvQ7RBzPWVDmzoe4uOe7UF0G8RcT9vQpg6C+LgcBk31KMQ8D9rQtrKTXm5DQ+UL9Sob2lZ2UrPcJjofYo5/YZCg0VhnQRghC6GO9oN3IMZvhs60CcKQX+FMqKK9QceOsWbCVcfuFh0NP0EY9Dssh72gTMfAyxBj5D7oXHPBBWTDPoQVcB4cB6eBt7a7YLjOfd3VsoWbXB4B7mAr0uBvIRtYhXUwEUIa7b1iZvwbRD8DwdfwLCyB3ZaTGX3ehmxkP8wITEkOBOuaJ+FPKOrbyw9wI5gq/S/yItwIRR+rys/QW2FWxag3AwbSudB7nIw+r4Nl7Rw4CvYBK0br+gWwBvyP5nEZ/cvXFh8nDgWPnkdOX3wALKNz/29AH2ykiyCfYdFpT4Yq2h9y+BWj3zIYK+IpCzJrIf0mxn4JLraWzoAcebw/6l6GHskdEHNYKVpx1pFFmSVyzPEqVH6RmQZfQAz2aJ0KdaVjxxzuRNGj3Wz4dJRtNhToCoh5xKNbSY9DDHJXTFPqajoYsWIej1ORfGaKPi62TBsg+ulffeV/XmeOQVdDE+nIMYfPqXtCkaouxOwi/2P6npC1EJ3fg6ZVYU5PvP3LVHUhyifY6HuHDWXyJs1Rqur7VZEMDjFPfv/VcMNosAii3y+jbRl3InQTRN9nbCjTPIiOPlI3zX28T2IeOQRCn0P+Wz/yO5hRM9rfsKFM90LRBHV1OMQ8kvOsQRZyAUT7RzaUaQtExxtsaCh3Ml9kuSJ8F7zxA1OX6OeY/DfxkTyUw/CY1ao/1ETHxTYMILPYmMu0o0x1nP1OiL5jvsToTPeMcqwNA8hUPD5q7lSmOgtxN6PvtTa0IX8ziY+appTVFlUXcg5EP4+gF24r0vCctpsAFqnKQrxM34Topy+3Koui+Lj/RcN7r8xmHxvlfhsK9BDkebxfWpWVXT7X1vxGnqoy1c+LkIehE1l09RZmJoD5xi6SBZ2XXh5nyM13Uus6Bb6CbJQJoLmTkdI0xcvO3fK3ybyLgXWI5UXn8rbXmF4D+6FPrIJOd6JXVnYWRaYXRUZnXMAL4G4Otawn/PHnOfAhw8W5Y/rPNdDaPTGucZVqZOQ/FRoQ53gVmukAAAAASUVORK5CYII=";
    $rootScope.icon_edit = "data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHfSURBVGhD7Zk7Sx1RFEavWIiPQOxNwEa7EKtoRP+H6UQSLYyNpBTBXlDsJWWwzy+I2mhlLBNIMJVWmoCKoq6PuGFzObmoA5kt7AULZs7cM+yP8xg4t5EkSZI8kOe4gJ9xCzfwLXbio+EDnuF1wV84hqFpwzUsBfCeY9gwpRA/cRLHcRH9KB1guGlWCrGNT9HzCn2YKQxDKcQVvsQSGhn73Sc1RKDVmtC06sdmXqP95osa6qYU4htqNOy+FEZrxp5ra66VUogd1JrQvP9XmF78gfZM35naaBXCKIUZQn0Yre0Un2Et3CWE0RzGX8t5rIX7hDCaw5irWAsPCSH0/Dv6fnqP3vffqRJiF32/DFGFDIG+X4aoQoZA3y9DVCFDoO+XIaqQIdD3qy2EWEFfzAW+wFaEC9GNl+gLkn/wHZYIF0L4E4ySS+gJGULMoRWko5hpPHRt0kYmbAjxEa2oZTWADgD20dp/o9ZM2BBiD62wN2q4pQ+P0J5pA7BrGSpEF/qFPoieGfTFm6FCiGG04k6wHQdwAjXNNtEHkOFCiPdoBepw7NjdlwwZQqxjqeBmNf107hQyhPA7k6lF/RW1m2nERlEfzbD0oP7uUtEamVkcQW0Aj4oOfPL3MkmSJAyNxg1x2mXbXV7r+QAAAABJRU5ErkJggg==";
    $rootScope.icon_save = "data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAEwSURBVGhD7ZkxjsIwEEUjigXKvQAFPRWn4AA0dFxy9wC0e5ItViDokID5kkcaWUk2TiYDEv9JTwI7xn4FLqAihBDyiszFdaAf4iisxHugX+JUdCc6BH6LM9EVG3IT/zIvos5f01id+gw8pjGINXZOdY+xIThAzk7U+QMGGtBn4AIDCazR8V/zGrrGRIbsRRzePusWExmCz8IXfZQYr5BP4wQDiTwENMUMupq9QpqoCwF1MThLb54VAhBjb8WwkLP4UyjW6Po8BGBPnQ8LGSpDuvBfCK7SrZP2WlbCQsaGITkMcSIkxG7iZdseDAFvF7IRlz3F2i57hIQM2SRiD4aUwJASGFIAQ0pgSAEMKcFukv+Ijfc6d0pjfcTaLnu4hTxbhoDov97axFkIIYS8ElX1ALJPbVp9kizNAAAAAElFTkSuQmCC";
    $rootScope.icon_trash = "data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFwSURBVGhD7ZmtSgVRFIVHBDEIahMUX0AFg8EgWHwEQRCsPoAWq8Fg1SCCVYuCJvEHk8VkEGwWX8AsFl0L9oaDHPHOZZ87w2V98JXFMPssmDn3cqYSQggBpuEBvIH3Ge/gMZyFrWUSfsDvDvyE87CV7MHcov/yDLaSS+iLPIWbGQ+hX/MMe8oAHO/AW+iL3Lbst2vQr3m17D8HYQij0Ic34RwMQUWCDCvi78gu9JufWxZtbkbYO+LsQB/CXakEvZihInVotMgYXDGXGCR4TocZGAvQ8wkGRqNFuHjP3xkkeE75h9J5hJ6vMzBUpA4qYqpINCpiqkg0KmKqSDQqYqpINCpitr7IIuSZL31hkOA5nWJgXEPPVxkYjRaJREXq0DdFeDDtQx4YFOAE+gye3BdhGfoQegRznw66dR9+Qb//BiwCj06fYFqmlG8wPT4Kh1sot9jc8Cj5WzQDizME+ShcwNwHz269gltwBAohRF9SVT/YcCJDemJ9EwAAAABJRU5ErkJggg==";
});
