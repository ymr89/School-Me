(function() {
var app = angular.module('myApp', []);
    app.config(['$httpProvider', function($httpProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }])
    app.controller('TabController', ['$scope', '$http', function($scope, $http){
        this.tab = 1;
        this.setTab = function(newValue){
            console.log('tab: ' + newValue);
            this.tab = newValue;
        };
        
        this.isSet = function(tabName){
            return this.tab === tabName;
        };
        $http.get('/checklogin/').success(function(data) {
            console.log('Current User: ' + data.user_id);
            $scope.user = data;
            $scope.userid = data.user_id;
        }).error(function(data) {
            console.log('error: ' + data);
        });

        /*$scope.checkUpvote = function(enable, id) {
            document.getElementById('upvote-' + id).disabled = enable;
        }
        $scope.checkDownvote = function(enable, id) {
            document.getElementById('downvote-' + id).disabled = enable;
        }*/


    }]);
}) ();