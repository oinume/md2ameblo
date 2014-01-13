'use strict';
var app = angular.module('md2ameblo', [ ]);

app.controller('Controller', function ($scope, $http, $location, $anchorScroll) {
  $scope.kind = null;

  $scope.initialize = function () {
    $scope.blogs = [
      { kind: 'ameblo', label: 'Ameblo', url: 'http://blog.ameba.jp/ucs/entry/srventryinsertinput.do' },
      { kind: 'blogger', label: 'Blogger', url: 'http://www.blogger.com/home' }
    ];
  }

  $scope.showTextarea = function (blog_kind) {
    $scope.blog_kind = blog_kind;
    console.log('blog_kind = ' + $scope.blog_kind);
  }

  $scope.send = function () {
    console.log('markdown = ' + $scope.markdown);
    $http.post('/' + $scope.blog_kind + '.json', {
      blog_kind: $scope.blog_kind,
      markdown: $scope.markdown
    }).success(function (data, status, headers, config) {
      $scope.html = data.html;
      var blogs = $scope.blogs;
      for (var i = 0; i < blogs.length; i++) {
        if (blogs[i]['kind'] == data.blog_kind) {
          $scope.blog_label = blogs[i]['label'];
          break;
        }
      }
      //alert($scope.html);
      $location.hash('copy');
      $anchorScroll();
    }).error(function (data, status, headers, config) {
      alert("Server error! (" + status + ")");
    });
  }

  var clip = new ZeroClipboard(document.getElementById("copy-to-clipboard"), {
    moviePath: "/static/bower_components/zeroclipboard/ZeroClipboard.swf"
  });
  clip.on("load", function (client) {
    //alert("movie is loaded");
    client.on("complete", function (client, args) {
      // `this` is the element that was clicked
      //this.style.display = "none";
      console.log("Copied text to clipboard: " + args.text);
      angular.element('#html').select();
      //alert("クリップボードにコピーされました");
    });
  });

  $scope.openBlog = function () {
    var blogs = $scope.blogs;
    var url = null;
    for (var i = 0; i < blogs.length; i++) {
      if (blogs[i]['kind'] == $scope.blog_kind) {
        url = blogs[i]['url'];
        break;
      }
    }
    window.open(url, $scope.blog_kind);
  }
});
