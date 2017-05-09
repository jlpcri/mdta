$(function(){
    $(".run-btn").click(populateSteps);
    $(".run-all-suite").click(getId);
    $(".run-all-btn").click(runAll);
});

var s_id;

function getId() {
    s_id = this.getAttribute('data-suite');
    $("#suiteid").val(s_id);
    return s_id;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
console.log(csrftoken);

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function runAll() {
    $('#run-all-modal-form').on('submit', function(event) {
        event.preventDefault();
        var button = $(this);
        $("#testcase").html("Generating tests. Please wait.");
        $("#result").html("");
        var data = $(this).serialize();
        $.ajax({
            type: 'POST',
            data: data,
            url: '{% url "runner:run_all_modal" %}',
            dataType: 'json',
            success: function (data, status) {
                $('#run-all-modal').modal('hide');
                $(location).attr('href', '#');
                var cases = data;
                var div = $("#testcase");
                var table_draw = '<table class="table table-bordered"><tr><th>Title</th><th>Status</th><th>Holly</th><th>Call ID & TestRail ID</th><th>Failure reason</th></tr>';
                $.each(cases.cases, function (index, value) {
                    table_draw += "<tr><td id='cinfo' class='title col-xs-2'>" + value.title+ "</td>" +
                    "<td class='status col-xs-1'><i class='fa fa-spin fa-spinner'></i><span> Running...</span></td>" +
                    "<td class='holly col-xs-1'>" + cases.holly + "</td>" +
                    "<td class='call-id col-xs-1'></td>" +
                    "<td class='reason col-xs-2'></td></tr>";
                });
                table_draw += "</table>";
                div.html(table_draw);
                $('#cinfo').append('<a href="javascript://" data-html="true" data-content="" title="Case Script" data-trigger="focus" data-toggle="popover">' + value.title + '</a>');
                $('#cinfo a').popover({ content:cases.cases.script });
                var counter = 0;
                var poll = setInterval(function () {
                    var run_id = parseInt(cases.run);
                    var hollytrace_url = cases.hollytrace_url;
                    var tr_host = cases.tr_host;
                    checkCase(cases.cases[counter], run_id, tr_host, hollytrace_url);
                    counter++;
                    if (counter >= cases.cases.length) {
                        if (checkCompletion()) {
                            console.log('Run complete');
                            clearInterval(poll)
                        }
                        counter = 0
                    }

                }, 750)
            }
        });
        return false;
    });
}

function checkCompletion(cases){
    var done = true;
    $(".status span").each(function(i, element){
        if (element.innerHTML === " Running...") {
            done = false
        }
    });
    return done
}

function checkCase(cases, run, tr_host, hollytrace_url) {
    $.ajax('{% url "runner:check_result" %}' + "?run_id=" + run, {
        success: function (data, textStatus, jqXHR) {
            console.log(data);
            if (!data.running) {
                $.each(data.data, function (index, value) {
                    if (value.hasOwnProperty('reason')) {
                        markFailure(value.title, value.call_id, value.reason, value.testrail_case_id, tr_host, hollytrace_url, value.tr_test_id);
                        console.log(value.title, value.call_id, value.reason, value.testrail_case_id, tr_host, hollytrace_url, value.tr_test_id);
                    }
                    else {
                        markSuccess(value.title, value.call_id, value.testrail_case_id, tr_host, hollytrace_url, value.tr_test_id);
                        console.log(value.title, value.call_id, value.testrail_case_id, tr_host, hollytrace_url, value.tr_test_id);

                    }
                })
            }
        }
    })
}

function markSuccess(title, callId, tc_id, tr_host, hollytrace_url, tr_test_id){
    updateStatusClassAndText(title, "fa fa-check-square text-success", "Pass");
    updateCallID(title, callId, tc_id, tr_host, hollytrace_url, tr_test_id)
}

function markFailure(title, callId, failureReason, tc_id, tr_host, hollytrace_url, tr_test_id){
    updateStatusClassAndText(title, "fa fa-minus-square text-danger", "Fail");
    updateCallID(title, callId, tc_id, tr_host, hollytrace_url, tr_test_id);
    updateFailureReason(title, failureReason)
}

function updateStatusClassAndText(title, cls, text){
    var status_td = $("#testcase table").find('td.title:contains("' + title + '")').siblings(".status");
    status_td.find("i").attr("class", cls);
    status_td.find("span").html(text)
}

function updateCallID(title, callId, tc_id, tr_host, hollytrace_url, tr_test_id) {
    var id_td = $("#testcase table").find('td.title:contains("' + title + '")').siblings(".call-id");
    var trurl = "<a href="  + tr_host + '/index.php?/tests/view/' + tr_test_id +" onclick='window.open(" + tr_host + '/index.php?/tests/view/' + tr_test_id +");'>" + tc_id + "</a>";
    var callurl = "<a href=" + 'http://' + hollytrace_url + '/call/' + callId +" onclick='window.open(" + hollytrace_url + '/call/' + callId +");'>" + callId + "</a>";
    id_td.html("<strong>Call ID:</strong> " + callurl + "<br>" + "<strong>TestRail:</strong> " + trurl);
}

function updateFailureReason(title, failureReason) {
    var reason_td = $("#testcase table").find('td.title:contains("' + title + '")').siblings(".reason");
    reason_td.html(failureReason)
}


function populateSteps(){
    var case_id = this.getAttribute('data-case');
    var button = $(this);
    $("#testcase").html("");
    $("#result").html("");
    button.siblings(".fa-spin").removeClass("hidden");
    $.ajax('{% url "runner:steps" project.id %}?case_id=' + case_id, {
        success: function(data, textStatus, jqXHR){
            var div = $("#testcase");
            var table_draw = '<table class="table table-bordered"><thead><tr><th class="col-md-4">Content</th><th class="col-md-8">Expected Result</th></tr></thead>';
            $.each(data.steps, function(index, value){
                table_draw += "<tr><td>" + value.content + "</td><td>" + value.expected + "</td></tr>";
                console.log(value);
            });
            table_draw += "</table>";
            div.html(table_draw)
        }
    });
    $.ajax('{% url "runner:run" project.id %}?case_id=' + case_id, {
        success: function(data, textStatus, jqXHR){
            console.log(data.result);
            button.siblings(".fa-spin").addClass("hidden");
            var result_table = "<table class='table table-bordered'><tr><th>Result</th><td>" + data.result + "</td></tr>";
            result_table += "<tr><th>Call ID</th><td>" + data.call_id + "</td></tr>";
            result_table += "<tr><th>Fail Reason</th><td>" + data.reason + "</td></tr></table>";
            $("#result").html(result_table);
            if(data.result === 'PASS') {
                button.siblings(".text-success").removeClass("hidden");
                button.siblings(".text-danger").addClass("hidden");
            }
            else if(data.result === 'FAIL') {
                console.log("Calling FAIL");
                window.needit = button;
                button.siblings(".text-danger").removeClass("hidden");
                button.siblings(".text-success").addClass("hidden");
            }

        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log("FAIL: " + textStatus);
            console.log(errorThrown);
            button.siblings(".fa-spin").addClass("hidden");
            button.siblings(".text-danger").removeClass("hidden");
            button.siblings(".text-success").addClass("hidden");
            var result_table = "<table class='table table-bordered'><tr><th>Result</th><td>ERROR</td></tr>";
            result_table += "<tr><th>Call ID</th><td>N/A</td></tr>";
            result_table += "<tr><th>Fail Reason</th><td>" + textStatus + ": " + errorThrown +  "</td></tr></table>";
            $("#result").html(result_table);
        }
    });

}
