angular.module("ciclotourApp").factory('RoutesAPI', function($http){
    return{
        get_route: function(id){
            return $http.get("/api/routes/"+id);
        },
        get_fields: function(){
            return $http.get("/api/fields/");
        },
        save_route: function(route){
            return $http.post("/api/routes/", route);
        }
    }
});