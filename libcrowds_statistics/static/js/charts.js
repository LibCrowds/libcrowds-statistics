Chart.defaults.global= {
    animation: true,
    animationSteps: 60,
    animationEasing: "easeOutQuart",
    showScale: true,
    scaleOverride: false,
    scaleSteps: null,
    scaleStepWidth: null,
    scaleStartValue: null,
    scaleLineColor: "rgba(0,0,0,.1)",
    scaleLineWidth: 1,
    scaleShowLabels: true,
    scaleLabel: "<%=value%>",
    scaleIntegersOnly: true,
    scaleBeginAtZero: false,
    scaleFontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
    scaleFontSize: 12,
    scaleFontStyle: "normal",
    scaleFontColor: "#666",
    responsive: true,
    maintainAspectRatio: false,
    showTooltips: true,
    customTooltips: false,
    tooltipEvents: ["mousemove", "touchstart", "touchmove"],
    tooltipFillColor: "rgba(0,0,0,0.8)",
    tooltipFontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
    tooltipFontSize: 14,
    tooltipFontStyle: "normal",
    tooltipFontColor: "#fff",
    tooltipTitleFontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
    tooltipTitleFontSize: 14,
    tooltipTitleFontStyle: "bold",
    tooltipTitleFontColor: "#fff",
    tooltipYPadding: 6,
    tooltipXPadding: 6,
    tooltipCaretSize: 8,
    tooltipCornerRadius: 6,
    tooltipXOffset: 10,
    tooltipTemplate:  "<%if(label)\u007B%><%=label%>: <%}%>"
                    + "<%=value%>"
                    + "<%if(datasetLabel == '%')\u007B%>"
                    + "<%=datasetLabel%>"
                    + "<%} else if(value != 1)\u007B%>"
                    + " <%=datasetLabel%>s"
                    + "<%}else\u007B%>"
                    + " <%=datasetLabel%>"
                    + "<%}%>",
    onAnimationProgress: function() {},
    onAnimationComplete: function() {},
    segmentShowStroke:  true,
    segmentStrokeColor:  "#fff",
    segmentStrokeWidth:  2,
    percentageInnerCutout:  50,
    animateRotate:  true,
    animateScale:  false,
    labelLength: 10
}


/** Highlights the bar in red. */
function highlightBar(bar) {
    bar.fillColor = "rgba(186,0,0,0.1)";
    bar.strokeColor = "rgba(186,0,0,0.5)";
    bar.highlightStroke = "rgba(208,0,0,0.5)";
    bar.highlightFill = "rgba(186,0,0,0.05)";
}


/** Returns a line chart dataset in the default style. */
function getLineDataset(label, data) {
    return [{
        label: label,
        fillColor: "rgba(151,187,205,0.2)",
        strokeColor: "rgba(151,187,205,1)",
        pointColor: "rgba(151,187,205,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(151,187,205,1)",
        data: data
    }];
}


/** Returns a bar chart dataset in the default style. */
function getBarDataset(label, data){
    return [{
        label: label,
        fillColor: "rgba(151,187,205,0.2)",
        strokeColor: "rgba(151,187,205,1)",
        highlightFill: "rgba(151,187,205,0.1)",
        highlightStroke: "rgba(151,187,205,1)",
        data: data
    }];
}


/** Returns a donut chart dataset in the default style. */
function getDonutDataset(label1, data1, label2, data2){
return [{
    label: label1,
    color:"rgba(186, 0, 0, 1)",
    highlight: "rgba(208, 0, 0, 1)",
    value : data1
    }, {
    label: label2,
    color: "rgba(151, 187, 205, 1)",
    highlight: "rgba(151, 187, 205, 0.8)",
    value: data2
    }];
}


/** Returns a radar chart dataset in the default style. */
function getRadarDataset(label, data) {
    return [{
        label: label,
        fillColor: "rgba(151,187,205,0.2)",
        strokeColor: "rgba(151,187,205,1)",
        pointColor: "rgba(151,187,205,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(151,187,205,1)",
        data: data
        }];
 }

/** Draw and return a bar chart in the default style. */
function drawBarChart(canvas, container, data) {
    var ctx = canvas[0].getContext("2d");
    var chart = new Chart(ctx).Bar(data);
    chart.draw();
    return chart;
}


/** Draw and return a line chart in the default style. */
function drawLineChart(canvas, container, data) {
    var ctx = canvas[0].getContext("2d");
    var opts = {populateSparseData:true};
    var chart = new Chart(ctx).Line(data, opts);
    chart.draw();
    return chart;
}


/** Draw and return a donut chart in the default style. */
function drawDonutChart(canvas, container, data, legendContainer) {
    var ctx = canvas[0].getContext("2d");
    var legendTemplate =  "<ul class=\"legend\">"
                        + "<% for (var i=0; i<segments.length; i++){%>"
                        + "<li><span style=\"background-color:"
                        + "<%=segments[i].fillColor%>\"></span>"
                        + "<%if(segments[i].label){%><%=segments[i].label%>"
                        + "<%}%></li><%}%></ul>";
    var opts = {tooltipTemplate: "<%=label%>", legendTemplate: legendTemplate};
    var chart = new Chart(ctx).Doughnut(data, opts);
    legend = chart.generateLegend();
    legendContainer.html(legend);
}


/** Draw and return a radar chart in the default style. */
function drawRadarChart(canvas, container, data) {
    var ctx = canvas[0].getContext("2d");
    tooltipTemplate = "<%if(label)\u007B%><%=label%>: <%}%><%=value%>%";
    var opts = {populateSparseData:true, tooltipTemplate: tooltipTemplate};
    var chart = new Chart(ctx).Radar(data, opts);
    chart.draw();
    return chart;
}


/** Return n followed by noun, pluralised with suffix, if necessary. */
function pluralise(n, noun, suffix){
    suffix = (typeof suffix === 'undefined') ? 's' : suffix;
    var str = n + ' ';
    if (suffix == 'ies') {
        return str + noun.substring(0, noun.length - 1) + suffix;
    }
    str = str + noun;
    if (n == 1) {
        return str;
    }
    return str + suffix;
}


/** Sets all chart containers in a stats-row to the same height. */
function resizeStatsRow() {
    if($(window).width() > 991) {
        var m2 = 0;
        $(".stats-row").children().children().height("");
        $(".stats-row").children().children().each(function(i, el) {
	m2 = Math.max(m2, $(el).height());
    });
    $(".stats-row").children().children().height(m2);
    }
}


/** Populate the statistics summary. */
function populateSummary(stats, id) {
    $('#' + id).slideDown();
    var n_volunteers = stats.n_auth + stats.n_anon
    var volunteers = pluralise(n_volunteers, 'volunteer');
    var projects = pluralise(stats.n_published_projects, 'project');
    var contributions = pluralise(stats.n_task_runs, 'contribution');
    var tasks = pluralise(stats.n_tasks_completed, 'task');
    have = (n_volunteers === 1) ? ' has' : ' have';
    var summary = ''.concat(volunteers, have, ' participated in ',
                            projects, ', made ',
                            contributions, ' and completed ',
                            tasks,
                            '.');
    $('#' + id).find(".text-stats").html(summary);
}


/** Populate the locations summary. */
function populateLocationsSummary(stats, id) {
    $('#' + id).slideDown();
    var continents = pluralise(stats.n_continents, 'continent');
    var countries = pluralise(stats.n_countries, 'country', 'ies');
    var cities = pluralise(stats.n_cities, 'city', 'ies');
    var summary = ''.concat('Contributions have been made from ', continents,
                            ', ', countries, ' and ', cities, '.');
    $('#' + id).find(".text-stats").html(summary);
}


/** Populate the locations chart. */
function populateLocationsChart(locs, id) {
    if(locs.length > 0) {
        $('#' + id).slideDown();
        var map = L.map('map', {scrollWheelZoom: false, minZoom:1});
        map.fitWorld();
        map.setZoom(2);
        var url = 'http://{s}.tile.osm.org/{z}/{x}/{y}.png'
        L.tileLayer(url,
            {
            attribution: '&copy; <a href="http://osm.org/copyright"> \
                                   OpenStreetMap \
                                 </a> &mdash; \
                                 <a href="http://www.maxmind.com"> \
                                   MaxMind \
                                 </a>',
            maxZoom: 18
            }).addTo(map);
        var i = 0;
        var locations = locs;
        var l = locations.length;
        var markers = new L.MarkerClusterGroup();
        for (i;i<l;i++) {
            if (locations[i].loc != null) {
                var lat = parseFloat(locations[i].loc.latitude);
                var lng = parseFloat(locations[i].loc.longitude);
                markers.addLayer(L.marker([lat,lng]));
            }
        }
        map.addLayer(markers);
    } else {
        $("#locations").hide();
    }
}


/** Populate the leaderboard chart. */
function populateLeaderboardChart(leaderboard, id){
    con = $('#' + id).find(".canvas-container");
    canvas = $('#' + id).find("canvas");

    if(leaderboard.length > 0) {
        $('#' + id).slideDown();
        var users = [];
        var scores = [];
        for (i = 0; i < leaderboard.length; i++) {
            users.push(leaderboard[i].name);
            scores.push(parseInt(leaderboard[i].score));
        }
        var data = {
            labels: users,
            datasets: getBarDataset("contribution", scores)
        };
        chart = drawBarChart(canvas, con, data);
        var highScore = scores.indexOf(Math.max.apply(Math, scores));
        highlightBar(chart.datasets[0].bars[highScore]);
        chart.update();
    } else {
        $('#' + id).hide();
    }
}


/** Populate the most active countries chart. */
function populateMostActiveCountriesChart(topCountries, id){
    con = $("#" + id).find(".canvas-container");
    canvas = $("#" + id).find("canvas");
    tbody = $("#" + id).find("tbody");

    if(topCountries['countries'].length > 0) {
        $('#' + id).slideDown();
        var countries = topCountries['countries'];
        var taskRuns = topCountries['n_task_runs'];

        var data = {
            labels: countries.slice(0,5),
            datasets: getBarDataset("contribution", taskRuns.slice(0,5))
        };
        chart = drawBarChart(canvas, con, data)
        highlightBar(chart.datasets[0].bars[0]);
        chart.update();

        // Populate the table
        var rows = '';
        $.each(countries, function(i){
            rows = rows + '<tr><td class="text-center">' + countries[i] +
            '</td><td class="text-center">' + taskRuns[i] +
            '</td></tr>';
        });
        tbody.html(rows);
    } else {
        $("#most-active-countries").hide();
    }
}


/** Populate the contributions per day chart. */
function populateDailyContributionsChart(taskRunsDaily, id) {
    con = $("#" + id).find(".canvas-container");
    canvas = $("#" + id).find("canvas");

    if(taskRunsDaily['days'].length > 0) {
        $('#' + id).slideDown();
        days = taskRunsDaily['days'];
        taskRuns = taskRunsDaily['task_runs'];
        var labels = [];
        $.each(days, function(i, date){
            var dateObj = new Date(date);
            labels.push($.datepicker.formatDate('dd M', dateObj));
        });
        var data = {
            labels: labels,
            datasets: getLineDataset("contribution", taskRuns)
        };
        drawLineChart(canvas, con, data);
    } else {
        $("#" + id).hide();
    }
}

/** Populate the users per day chart. */
function populateUsersPerDayChart(usersDaily, id) {
    $('#' + id).slideDown();
    con = $("#" + id).find(".canvas-container");
    canvas = $("#" + id).find("canvas");
    days = usersDaily['days'];
    users = usersDaily['users'];
    var labels = [];
    $.each(days, function(i, date){
        var dateObj = new Date(date);
        labels.push($.datepicker.formatDate('dd M', dateObj));
    });
    var data = {
        labels: labels,
        datasets: getLineDataset("volunteer", users)
    };
    drawLineChart(canvas, con, data);
}


/** Populate the top users this week chart. */
function populateTopUsersThisWeekChart(top5Users1Week, id) {
    con = $("#" + id).find(".canvas-container");
    canvas = $("#" + id).find("canvas");

    if(top5Users1Week.length > 0) {
        $('#' + id).slideDown();
        var users = [];
        var taskRuns = [];
        for (i = 0; i < top5Users1Week.length; i++) {
            users.push(top5Users1Week[i]['name']);
            taskRuns.push(parseInt(top5Users1Week[i]['task_runs']));
        }
        var data = {
            labels: users,
            datasets: getBarDataset("contribution", taskRuns)
        };
        chart = drawBarChart(canvas, con, data);
        var highScore = taskRuns.indexOf(Math.max.apply(Math, taskRuns));
        highlightBar(chart.datasets[0].bars[highScore]);
        chart.update();
    } else {
        $("#" + id).hide();
    }
}


/** Populate the proportion authenticated chart. */
function populateProportionAuthChart(stats, id) {
    $('#' + id).slideDown();
    con = $("#" + id).find(".canvas-container");
    canvas = $("#" + id).find("canvas");
    lCon = $("#" + id).find(".legend-container");

    var total = stats.n_auth + stats.n_anon;
    var authLabel = ''.concat("Authenticated: ",
                              Math.round(stats.n_auth/total*100),
                              "% (" + pluralise(stats.n_auth, " user"), ')');
    var anonLabel = ''.concat("Anonymous: ",
                              Math.round(stats.n_anon/total*100),
                              "% (" + pluralise(stats.n_anon, " user"), ')');
    var data = getDonutDataset(authLabel, stats.n_auth, anonLabel, stats.n_anon);
    drawDonutChart(canvas, con, data, lCon);
}


/** Populate the contributions per day chart. */
function populateDowChart(dow, id) {
    $('#' + id).slideDown();
    con = $("#" + id).find(".canvas-container");
    canvas = $("#" + id).find("canvas");

    var labels = dow['days'];
    var percentages = dow['percentages'];
    var data = {
        labels: labels,
        datasets: getRadarDataset("day", percentages)
        };
    drawRadarChart(canvas, con, data)
}


/** Populate the top 10 percent chart. */
function populateTop10PercentChart(stats, id) {
    $('#' + id).slideDown();
    con = $('#' + id).find(".canvas-container");
    canvas = $('#' + id).find("canvas");
    lCon = $('#' + id).find(".legend-container");

    var top10 = stats.n_tr_top_10_percent
    var bottom90 = stats.n_task_runs - top10
    var top10Label = "Most Active 10%: " + pluralise(top10, "contribution")
    var bottom90Label = "Remaining 90%: " + pluralise(bottom90, "contribution")
    var data = getDonutDataset(top10Label, top10, bottom90Label, bottom90);
    drawDonutChart(canvas, con, data, lCon);
}


/** Populate the hourly activity chart. */
function populateHourlyActivityChart(hourlyActivity, id) {
    $('#' + id).slideDown();
    con = $('#' + id).find(".canvas-container");
    canvas = $('#' + id).find("canvas");

    var labels = [];
    var percentages = [];
    for(var i = 0; i < hourlyActivity.length; i++) {
        hour = hourlyActivity[i][0] + ':00'
        if (hour.length < 5) {
            hour = '0' + hour;
        }
        labels.push(hour);
        percentages.push(hourlyActivity[i][1]);
    }
    var data = {
        labels: labels,
        datasets: getLineDataset("%", percentages)
    };
    drawLineChart(canvas, con, data);
}