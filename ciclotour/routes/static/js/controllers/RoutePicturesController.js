angular.module("ciclotourApp").controller('RoutePicturesController', function($scope, $stateParams, RoutesAPI) {
    $scope.pictures = [];
    $scope.routeId = 0;

    $scope.showPicture = function(url, description){
        $('#imagepreview').attr('src', url);
        $('#imagedescription').text(description);
        $('#imagemodal').modal('show');
    };

    $scope.init = function() {
        $scope.routeId = $stateParams.id;
        get_pictures();
    };

    $scope.getNext = get_pictures;

    function get_pictures (){
        if($scope.next == null && $scope.pictures.length == 0)
            RoutesAPI.get_route_pictures($scope.routeId).success(getPicturesSuccess).error(getPicturesFail);
        else if($scope.next && $scope.pictures.length > 0)
            RoutesAPI.get_next_pictures($scope.routeId, $scope.next).success(getPicturesSuccess).error(getPicturesFail);
    }

    function getPicturesSuccess(data){
        $scope.next = data.next;
        $scope.pictures = $scope.pictures.concat(data.results);
    }

    function getPicturesFail(data){
        Message.showWarning('Não foi possível obter imagens.', 'Ocorreu uma falha ao tentar ' +
            'obter imagens. Tente novamente.');

        console.log(data);
    }
});