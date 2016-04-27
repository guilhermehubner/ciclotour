angular.module("ciclotourApp").factory('authInterceptor', function ($rootScope, $q, $cookies, $location) {
    return {
        request: function (config) {
            config.headers = config.headers || {};
            if ($cookies.get("token")) {
                config.headers.Authorization = 'Token ' + $cookies.get("token");
            }
            return config;
        },
        response: function (response) {
            return response || $q.when(response);
        },
        responseError: function (response) {
            if (response.status === 401) {
                $cookies.remove("token");
                $location.path("/login");
            }

            return $q.reject(response);
        }
    };
});