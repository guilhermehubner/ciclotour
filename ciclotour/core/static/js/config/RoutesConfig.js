angular.module("ciclotourApp").config(function ($stateProvider, $urlRouterProvider, $urlMatcherFactoryProvider) {

    var GUID_REGEXP = /^[a-f\d]{8}-([a-f\d]{4}-){3}[a-f\d]{12}$/i;
    $urlMatcherFactoryProvider.type('guid', {
        encode: angular.identity,
        decode: angular.identity,
        is: function(item) {
            return GUID_REGEXP.test(item);
        }
    });

    $stateProvider
        .state('login', {
            url: "/login",
            templateUrl: "static/js/views/login.html"
        })
        .state('confirmation', {
            url: "/confirmation/{token:guid}",
            templateUrl: "static/js/views/confirmation.html"
        })
        .state('pendingRequests', {
            url: "/pendingRequests",
            templateUrl: "static/js/views/pending_requests.html"
        })
        .state('friends', {
            url: "/friends",
            templateUrl: "static/js/views/friends.html"
        })
        .state('userProfile', {
            url: "/userProfile",
            templateUrl: "static/js/views/user_form.html"
        })
        .state('userSearch', {
            url: "/userSearch",
            templateUrl: "static/js/views/user_search.html"
        })
        .state('home', {
            url: "/home",
            templateUrl: "static/js/views/home.html"
        })
        .state('routeCreate',{
            url: "/routeCreate",
            templateUrl: "static/js/views/routes_form.html"
        })
        .state('routeDetail',{
            url: "/routeDetail/{id:[0-9]+}",
            templateUrl: "static/js/views/routes_detail.html"
        })
        .state('routePointCreate',{
            url: "/routePointCreate/{id:[0-9]+}",
            templateUrl: "static/js/views/routes_point_form.html"
        })
        .state('routePictures',{
            url: "/routePictures/{id:[0-9]+}",
            templateUrl: "static/js/views/route_pictures.html"
        })
        .state('pendingRoutes',{
            url: "/pendingRoutes",
            templateUrl: "static/js/views/pending_routes.html"
        })
        .state('performedRoutes',{
            url: "/performedRoutes",
            templateUrl: "static/js/views/performed_routes.html"
        })
        .state('routePointDetail',{
            url: "/routePoint/{id:[0-9]+}",
            templateUrl: "static/js/views/routes_point_detail.html"
        });

    $urlRouterProvider.otherwise("/home");
});
