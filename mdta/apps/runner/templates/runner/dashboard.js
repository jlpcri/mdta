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

function runAll(){
    var suite_id = s_id;
    console.log(s_id);
    var button = $(this);
    $("#testcase").html("Generating tests. Please wait.");
    $("#result").html("");
    $.ajax('{% url "runner:run_all_modal" %}?suite=' + suite_id, {
        success: function(data, textStatus, jqXHR){
            var div = $("#testcase");
            var table_draw = '<table class="table table-bordered"><tr><th>Title</th><th>Script</th><th>Status</th><th>Call ID</th><th>Failure reason</th></tr>'
            console.log(data)
            console.log(data.scripts)
            $.each(data.scripts, function(index, value){
                table_draw += "<tr><td class='title'></td>" +
                    "<td class='script'>" + value + "</td>" +
                    "<td class='status'><i class='fa fa-spin fa-spinner'></i> <span> Running...</span></td>" +
                    "<td class='call-id'></td>" +
                    "<td class='reason'></td></tr>"
            });
            table_draw += "</table>";
            div.html(table_draw);
            var counter = 0;
            var poll = setInterval(function() {
                checkScript(data.scripts[counter])
                counter++;
                if (counter >= data.scripts.length){
                    if (checkCompletion()) {
                        console.log('Run complete')
                        clearInterval(poll)
                    }
                    counter = 0
                }

            }, 750)
        }
    })
}

function checkCompletion(script){
    var done = true
    $(".status span").each(function(i, element){
        if (element.innerHTML === " Running...") {
            done = false
        }
    })
    return done
}

function checkScript(script){
    $.ajax('{% url "runner:check_result" %}' + "?filename=" + script, {
        success: function(data, textStatus, jqXHR){
            console.log(data)
            if (!data.running) {
                if (data.success) {
                    markSuccess(script, data.call_id)
                }
                else {
                    markFailure(script, data.call_id, data.reason)
                }
            }
        }
    })

}

function markSuccess(script, callId){
    updateStatusClassAndText(script, "fa fa-check-square text-success", "Pass")
    updateCallID(script, callId)
}

function markFailure(script, callId, failureReason){
    updateStatusClassAndText(script, "fa fa-minus-square text-danger", "Fail")
    updateCallID(script, callId)
    updateFailureReason(script, failureReason)
}

function updateStatusClassAndText(script, cls, text){
    var status_td = $("#testcase table").find('td.script:contains("' + script + '")').siblings(".status")
    status_td.find("i").attr("class", cls)
    status_td.find("span").html(text)
}

function updateCallID(script, callId){
    var id_td = $("#testcase table").find('td.script:contains("' + script + '")').siblings(".call-id")
    id_td.html(callId)
}

function updateFailureReason(script, failureReason){
    var reason_td = $("#testcase table").find('td.script:contains("' + script + '")').siblings(".reason")
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
            var table_draw = '<table class="table table-bordered"><thead><tr><th class="col-md-4">Content</th><th class="col-md-8">Expected Result</th></tr></thead>'
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
            var result_table = "<table class='table table-bordered'><tr><th>Result</th><td>" + data.result + "</td></tr>"
            result_table += "<tr><th>Call ID</th><td>" + data.call_id + "</td></tr>"
            result_table += "<tr><th>Fail Reason</th><td>" + data.reason + "</td></tr></table>"
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
            var result_table = "<table class='table table-bordered'><tr><th>Result</th><td>ERROR</td></tr>"
            result_table += "<tr><th>Call ID</th><td>N/A</td></tr>"
            result_table += "<tr><th>Fail Reason</th><td>" + textStatus + ": " + errorThrown +  "</td></tr></table>"
            $("#result").html(result_table);
        }
    });
    
}
