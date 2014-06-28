var ghUser = new Gh3.User("ksikka");

// ui state
var domready = false;
var $main;
var presented = false;

// model state
var userInfo;

var presentResultsWhenReady = function() {
    if (!userInfo) {
        // not yet ready
        return;
    }
    if (presented) {
        // already presented
        return;
    }
    presented = true;

    _.each(_.keys(userInfo), function (prop) {
        var $li = $main.append($('<li>').text(
        prop + " : " + userInfo[prop]
        ));
    });
};

// get data immediately
ghUser.fetch(function (err, resUser){


    if(err) {
        alert("outch ...");
    }

    userInfo = resUser;
    presentResultsWhenReady();
    console.log(userInfo);

});

$('document').ready(function() {
    $main = $('#main');
    $main.text('yolo');
    presentResultsWhenReady();
});
