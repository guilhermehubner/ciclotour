angular.module("ciclotourApp").factory('RoutesAPI', function($http){
    return{
        get_route: function(id){
            return $http.get("/api/routes/"+id);
        },
        get_routes: function(){
            return $http.get("/api/routes/");
        },
        get_next_routes: function(next){
            return $http.get("/api/routes/?page="+next);
        },
        get_fields: function(){
            return $http.get("/api/fields/");
        },
        get_pointkinds: function(){
            return $http.get("/api/pointkinds/");
        },
        get_route_pictures: function(routeId){
            return $http.get("/api/route/pictures/?route="+routeId);
        },
        get_next_pictures: function(routeId, next){
            return $http.get("/api/route/pictures/?route="+routeId+"&page="+next);
        },
        save_route_point: function(point){
            return $http.post("/api/route/points/", point);
        },
        save_route_picture: function(picture){
            var fd = new FormData();

            for (var key in picture) {
                fd.append(key, picture[key]);
            }

            return $http.post("/api/route/pictures/", fd,{
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            });
        },
        save_route: function(route){
            return $http.post("/api/routes/", route);
        },
        search: function(originCoordinates, destinationCoordinates){
            return $http.get("/api/routes_search/?from_lat="+originCoordinates.lat+"&from_lng="+
                originCoordinates.lng+"&to_lat="+destinationCoordinates.lat+"&to_lng="+
                destinationCoordinates.lng);
        },
        search_next: function(originCoordinates, destinationCoordinates, next){
            return $http.get("/api/routes_search/?from_lat="+originCoordinates.lat+"&from_lng="+
                originCoordinates.lng+"&to_lat="+destinationCoordinates.lat+"&to_lng="+
                destinationCoordinates.lng+"&page="+next);
        },
        mark_as_performed: function(id){
            return $http.get("api/route/mark-as-performed/"+id);
        },
        mark_as_pending: function(id){
            return $http.get("api/route/mark-as-pending/"+id);
        },
        get_pending_routes: function(){
            return $http.get("/api/pending-routes/");
        },
        get_next_pending_routes: function(next){
            return $http.get("/api/pending-routes/?page="+next);
        },
        get_performed_routes: function(){
            return $http.get("/api/performed-routes/");
        },
        get_next_performed_routes: function(next){
            return $http.get("/api/performed-routes/?page="+next);
        },
        get_route_comments: function(routeId){
            return $http.get("/api/route-comments/?routeId="+routeId);
        },
        get_next_route_comments: function(routeId, next){
            return $http.get("/api/route-comments/?routeId="+routeId+"&page="+next);
        },
        post_comment: function(routeId, comment){
            data = {
                route: routeId,
                description: comment
            };

            return $http.post("/api/comment-route/", data);
        },
        get_point_comments: function(pointId){
            return $http.get("/api/point-comments/?pointId="+pointId);
        },
        get_next_point_comments: function(pointId, next){
            return $http.get("/api/point-comments/?pointId="+pointId+"&page="+next);
        },
        post_point_comment: function(pointId, comment){
            data = {
                point: pointId,
                description: comment
            };

            return $http.post("/api/comment-point/", data);
        },
        get_route_point: function(pointId){
            return $http.get("/api/route/points/"+pointId);
        }
    }
});