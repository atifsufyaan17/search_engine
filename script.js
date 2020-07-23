
$('li').click(function() {
    $(this).addClass('active').siblings().removeClass('active');
});
var app = angular.module("myApp", []);
app.controller("myCtrl", function ($scope, $http) {
    $scope.query = '';
    $scope.results = [];
    $scope.detailed_info = [];
    $scope.showMe = false;
    $scope.showMe1 = false;
    $scope.dict = new Object();
    $scope.page1 = 1; $scope.page2 = 2; $scope.page3 = 3;
    $scope.fromTime = ''; $scope.toTime = '';
    $scope.prevPage = function () {
        if ($scope.page3 > 3) {
            $scope.page1 = $scope.page1 - 3; $scope.page2 = $scope.page2 - 3; $scope.page3 = $scope.page3 - 3;
            $scope.search(3);
        }
    }
    $scope.nextPage = function () {
        if ($scope.page3 < 100) {
            $scope.page1 = $scope.page1 + 3; $scope.page2 = $scope.page2 + 3; $scope.page3 = $scope.page3 + 3;
            $scope.search(1);
        }
    }
    $scope.search = function (page) {
        if (page == 1) start_page = $scope.page1;
        else if (page == 2) start_page = $scope.page2;
        else start_page = $scope.page3;
        var parameters = {
            'data': $scope.query,
            'fromTime': $scope.fromTime,
            'toTime': $scope.toTime,
            'start_page': start_page,
        };
        $http.post("http://localhost:5000/", parameters).then(function (response) {
            $scope.results = response.data['hits']['hits'];
            $scope.showMe = true;
        });
    };
    $scope.details = function (result) {
        $scope.detailed_info = result;
        $scope.dict = {
            100: "影くっきり／はっきり Clear shadow",
            101: "影ぼんやり／うっすら Vague/slight shadow",
            200: "影見えない（くもり） No shadow (cloudy)",
            300: "ぽつぽつ Rain sometimes drops",
            301: "ぱらぱら Sprinkling/drizzling",
            302: "さー Raining",
            303: "ザー Pouring",
            304: "ゴーッ Terrible rain",
            400: "べちゃ（みぞれ） Sleet",
            410: "ちらちら Snow sometimes drops",
            411: "ふわふわ Snowing fluffily",
            412: "しんしん Snowing",
            420: "ドカドカ Snowing heavily",
            421: "あられ Hailstone",
            422: "吹雪 Snowstorm/blizzard",
        };
    };
    // $scope.$watch(function (scope) { return scope.query },
    //     function () {
    //         $scope.search();
    //     }
    // );
});