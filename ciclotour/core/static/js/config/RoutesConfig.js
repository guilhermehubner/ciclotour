angular.module("ciclotourApp").config(function ($routeProvider) {
    $routeProvider.when("/login", {
        templateUrl: "static/js/views/login.html"
    });
    $routeProvider.when("/home", {
        templateUrl: "static/js/views/home.html"
    });
    $routeProvider.when("/routeCreate", {
        templateUrl: "static/js/views/routes_form.html"
    });
    $routeProvider.when("/routeDetail/:id", {
        templateUrl: "static/js/views/routes_detail.html"
    });
    $routeProvider.otherwise({redirectTo: "/home"});
});