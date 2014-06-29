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
/*
ghUser.fetch(function (err, resUser){


    if(err) {
        alert("outch ...");
    }

    userInfo = resUser;
    presentResultsWhenReady();
    console.log(userInfo);

});
*/

var ghRepos = new Gh3.Repositories(ghUser);
ghRepos.fetch({page:1, per_page:500, direction : "desc"}, null, function (err, result) {
    if (err) alert (err);
    else {
        //console.log(result);
        _.each(result.getRepositories(), function(r) {
            // console.log(r);
            var commits = [];
            Gh3.Helper.callHttpApi({
                //service : "repos/"+r.user.login+"/"+r.name+"/commits",
                service : "repos/"+ghRepos.user.login+"/"+r.name+"/commits",
                data : {},
                success : function(res) {
                    console.log('commits for '+r.name+': ', res);
                    _.each(res.data, function (commit) {
                        commits.push(new Gh3.Commit(commit));
                    });
                },
                error : function (res) {
                    console.log('error', res);
                }
            });
        });
    }
});

//all repositories, one page, 500 items per page, sort : descending

$('document').ready(function() {
    $main = $('#main');
    $main.text('yolo');
    presentResultsWhenReady();
});
