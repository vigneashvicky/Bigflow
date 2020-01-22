var loginapp = angular.module('loginapp', ['ngMaterial']).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

loginapp.controller("Logincnt", ['$scope', '$window', 'loginService', '$http', function($scope, $window, loginService, $http) {

    $scope.maintable = [];
    document.getElementById('Username').focus();

    function loadcheck() {
        var jsonData = {
            "employee_gid": $scope.maintable.employee_gid
        };
        var schedule_check = loginService.ipset('check', jsonData)
        schedule_check.then(function(result) {
            if (result.data > 0) {
               alert("'Kindly Logout' Session Before You Logged In!");
                if (r == true) {
                    $scope.chckid = result.data;
                } else {
                    return false;
                }
            } else if (result.data == 0) {
                load()
            } else {
                alert("Not Login Successfully!.");
            }
        }, function(err) {
            alert("Not Login Successfully!");
        });
    };

    function load() {
        if ($scope.chckid > 0) {
            var jsonData = {
                "employee_gid": $scope.maintable.employee_gid,
                "logingid": $scope.chckid
            };
        } else {
            var jsonData = {
                "employee_gid": $scope.maintable.employee_gid,
                "logingid": ''
            };
        }
        var schedule_check = loginService.ipset('insert', jsonData)
        schedule_check.then(function(result) {
            if (result.data > 0) {
                alert("Logged In Successfully!.");
                $window.location.href = "../welcome";
            } else {
                alert("Not Login Successfully!.");
            }
        }, function(err) {
            alert("Not Login Successfully!");
        });
    };

    $scope.Loginchk = function() {
        var username = $scope.Username;
        var password = $scope.Password;
        var pswd = loginService.getlogin(username, password);
        pswd.then(function(result) {
                if (JSON.parse(result.data) != "FAIL") {
                    $scope.maintable = JSON.parse(result.data);
                    sessionStorage.setItem('today', result.data);
                    loadcheck()
                } else {
                    alert('User Name or Password Not Matched.');
                }
            }),
            function() {
                alert('no data');
            };
    };
}]);

loginapp.service("loginService", function($http) {
    this.getlogin = function(e, e1) {
        var response = $http.post("/loginpswd/", {
            parms: {
                "username": e,
                "password": e1
            }
        });
        return response;
    }
    this.ipset = function(action, jsonData) {
        var response = $http.post("/setip_sys/", {
            parms: {
                "action": action,
                "jsonData": jsonData
            }
        });
        return response;
    }
});