$(document).ready(function () {
    $("#search").click(function () {
        var indus = $("#industry").val();

        $.getJSON("/indus", {indus: indus}, function (inputData) {
            tree = inputData;
            heat_map(tree);
        });
    });
});