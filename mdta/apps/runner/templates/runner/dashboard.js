$(function(){
    $(".run-btn").click(populateSteps)
    $(".run-all-btn").click(runAll)
});

function runAll(){
    var suite_id = this.getAttribute('data-suite')
    var button = $(this);
    $("#testcase").html("");
    $("#result").html("");
    $.ajax('{% url "runner:runall" %}?suite=' + suite_id, {
        success: function(data, textStatus, jqXHR){
            var div = $("#testcase");
            console.log(data)
        }
    })
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
