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
                      + "<%=value%> "
                      + "<%if(datasetLabel == '%')\u007B%>"
                      + "<%=datasetLabel%>"
                      + "<%} else if(value != 1)\u007B%>"
                      + "<%=datasetLabel%>s"
                      + "<%}else\u007B%>"
                      + "<%=datasetLabel%>"
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
};


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
    let ctx   = canvas[0].getContext("2d"),
        chart = new Chart(ctx).Bar(data);
    chart.draw();
    return chart;
}


/** Draw and return a line chart in the default style. */
function drawLineChart(canvas, container, data) {
    let ctx   = canvas[0].getContext("2d"),
        opts  = {populateSparseData:true},
        chart = new Chart(ctx).Line(data, opts);
    chart.draw();
    return chart;
}


/** Draw and return a donut chart in the default style. */
function drawDonutChart(canvas, container, data, legendContainer) {
    let legendTemplate = `<ul class=\"legend\">
                          <% for (var i=0; i<segments.length; i++){%>
                          <li><span style=\"background-color:
                          <%=segments[i].fillColor%>\"></span>
                          <%if(segments[i].label){%><%=segments[i].label%>
                          <%}%></li><%}%></ul>`;
    let ctx    = canvas[0].getContext("2d"),
        opts   = {tooltipTemplate: "<%=label%>", legendTemplate: legendTemplate},
        chart  = new Chart(ctx).Doughnut(data, opts),
        legend = chart.generateLegend();
    legendContainer.html(legend);
}


/** Draw and return a radar chart in the default style. */
function drawRadarChart(canvas, container, data) {
    let tooltipTemplate = "<%if(label)\u007B%><%=label%>: <%}%><%=value%>%";
    let ctx   = canvas[0].getContext("2d"),
        opts  = {populateSparseData:true, tooltipTemplate: tooltipTemplate},
        chart = new Chart(ctx).Radar(data, opts);
    chart.draw();
    return chart;
}


/** Return n followed by noun, pluralised with suffix, if necessary. */
function pluralise(n, noun, suffix){
    suffix = (typeof suffix === 'undefined') ? 's' : suffix;
    if (suffix == 'ies') {
        return `${n} ` + noun.substring(0, noun.length - 1) + suffix;
    }
    if (n == 1) {
        return `${n} ${noun}`;
    }
    return `${n} ${noun}${suffix}`;
}


/** Sets all chart containers in a stats-row to the same height. */
function resizeStatsRow() {
    if ($(window).width() > 991) {
        let m2 = 0;
        $(".stats-row").children().children().height("");
        $(".stats-row").children().children().each(function(i, el) {
	    m2 = Math.max(m2, $(el).height());
	});
	$(".stats-row").children().children().height(m2);
    }
}


/** Populate the statistics summary. */
function populateSummary(stats, id) {
    let n_volunteers  = stats.n_auth + stats.n_anon,
        volunteers    = pluralise(n_volunteers, 'volunteer'),
        projects      = pluralise(stats.n_published_projects, 'project'),
        contributions = pluralise(stats.n_task_runs, 'contribution'),
        tasks         = pluralise(stats.n_tasks_completed, 'task'),
        have          = (n_volunteers === 1) ? ' has' : ' have',
        summary       = `${volunteers}${have} participated in ${projects},
                        made ${contributions} and complete ${tasks}.`;
    $(`#${id}`).find(".text-stats").html(summary);
}


/** Populate the locations summary. */
function populateLocationsSummary(stats, id) {
    let continents = pluralise(stats.n_continents, 'continent'),
        countries  = pluralise(stats.n_countries, 'country', 'ies'),
        cities     = pluralise(stats.n_cities, 'city', 'ies'),
        summary    = `Contributions have been made from ${continents},
                     ${countries} and ${cities}.`;
    $(`#${id}`).find(".text-stats").html(summary);
}


/** Populate the locations chart. */
function populateLocationsChart(locs, id) {
    if(!locs.length) {
	$(`#${id}`).hide();
	return;
    }

    let map   = L.map('map', {scrollWheelZoom: false, minZoom:1}),
	token = 'pk.eyJ1IjoibGliY3Jvd2RzIiwiYSI6ImNpdmlxaHFzNTAwN3YydHBncHV3dHc3aXgifQ.V4WUx9SDcU_XLFJo2M3RxQ',
	url   = `https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=${token}`;
    map.fitWorld();
    map.setZoom(2);
    L.tileLayer(url, {
	attribution: `Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,
		     <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy;
		     <a href="http://mapbox.com">Mapbox</a>`,
	maxZoom: 18,
	id: 'mapbox.streets',
	accessToken: token
    }).addTo(map);

    let i = 0;
    let locations = locs;
    let l = locations.length;
    let markers = new L.MarkerClusterGroup();
    for (i; i < l; i++) {
	if (locations[i].loc !== null) {
	    let lat = parseFloat(locations[i].loc.latitude),
		lng = parseFloat(locations[i].loc.longitude);
	    markers.addLayer(L.marker([lat, lng]));
	}
    }
    map.addLayer(markers);
}


/** Populate the leaderboard chart. */
function populateLeaderboardChart(leaderboard, id){
    let users  = [],
	scores = [];
    for (i = 0; i < leaderboard.length; i++) {
	users.push(leaderboard[i].name);
	scores.push(parseInt(leaderboard[i].score));
    }

    let con    = $(`#${id}`).find(".canvas-container"),
	canvas = $(`#${id}`).find("canvas"),
	data   = {
	    labels: users,
	    datasets: getBarDataset("contribution", scores)
	};
    let chart = drawBarChart(canvas, con, data);
    let highScore = scores.indexOf(Math.max.apply(Math, scores));
    highlightBar(chart.datasets[0].bars[highScore]);
    chart.update();
}


/** Populate the most active countries chart. */
function populateMostActiveCountriesChart(topCountries, id){
    let countries = topCountries.countries,
	taskRuns  = topCountries.n_task_runs;
    let con    = $(`#${id}`).find(".canvas-container"),
	canvas = $(`#${id}`).find("canvas"),
	data = {
	    labels: countries.slice(0,5),
	    datasets: getBarDataset("contribution", taskRuns.slice(0,5))
	};
    let chart = drawBarChart(canvas, con, data);
    highlightBar(chart.datasets[0].bars[0]);
    chart.update();

    // Populate the table
    $.each(countries, function(i){
	$(`#${id}`).find("tbody").append(
	    `<tr>
	    <td class="text-center">${countries[i]}</td>
	    <td class="text-center">${taskRuns[i]}</td>
	    </tr>`
	);
    });
}


/** Populate the contributions per day chart. */
function populateDailyContributionsChart(taskRunsDaily, id) {
    let days     = taskRunsDaily.days,
	taskRuns = taskRunsDaily.task_runs,
	labels   = [];
    $.each(days, function(i, date) {
	let dateObj = new Date(date);
	labels.push($.datepicker.formatDate('dd M', dateObj));
    });

    let con    = $(`#${id}`).find(".canvas-container"),
	canvas = $(`#${id}`).find("canvas"),
	data   = {
	    labels: labels,
	    datasets: getLineDataset("contribution", taskRuns)
	};
    drawLineChart(canvas, con, data);
}

/** Populate the users per day chart. */
function populateUsersPerDayChart(usersDaily, id) {
    let days   = usersDaily.days,
        users  = usersDaily.users;
        labels = [];
    $.each(days, function(i, date) {
        let dateObj = new Date(date);
        labels.push($.datepicker.formatDate('dd M', dateObj));
    });

    let con    = $(`#${id}`).find(".canvas-container"),
        canvas = $(`#${id}`).find("canvas"),
	data   = {
	    labels: labels,
	    datasets: getLineDataset("volunteer", users)
	};
    drawLineChart(canvas, con, data);
}


/** Populate the top users this week chart. */
function populateTopUsersThisWeekChart(top5Users1Week, id) {
    if(top5Users1Week.length < 2) {
	$(`#${id}`).hide();
	return;
    }

    let users    = [],
	taskRuns = [];
    for (i = 0; i < top5Users1Week.length; i++) {
	users.push(top5Users1Week[i]['name']);
	taskRuns.push(parseInt(top5Users1Week[i]['task_runs']));
    }

    let con    = $(`#${id}`).find(".canvas-container"),
	canvas = $(`#${id}`).find("canvas"),
	data   = {
	    labels: users,
	    datasets: getBarDataset("contribution", taskRuns)
	};
    let chart = drawBarChart(canvas, con, data);
    let highScore = taskRuns.indexOf(Math.max.apply(Math, taskRuns));
    highlightBar(chart.datasets[0].bars[highScore]);
    chart.update();
}


/** Populate the proportion authenticated chart. */
function populateProportionAuthChart(stats, id) {
    let total       = stats.n_auth + stats.n_anon,
	authPercent = Math.round(stats.n_auth/total*100),
	anonPercent = Math.round(stats.n_anon/total*100),
	authUsers   = pluralise(stats.n_auth, " user"),
	anonUsers   = pluralise(stats.n_anon, " user"),
        authLabel   = `Authenticated: ${authPercent}% (${authUsers})`,
	anonLabel   = `Authenticated: ${anonPercent}% (${anonUsers})`;

    let con       = $(`#${id}`).find(".canvas-container"),
        canvas    = $(`#${id}`).find("canvas"),
        legendCon = $(`#${id}`).find(".legend-container"),
	data      = getDonutDataset(authLabel, stats.n_auth, anonLabel, stats.n_anon);
    drawDonutChart(canvas, con, data, legendCon);
}


/** Populate the contributions per day chart. */
function populateDowChart(dow, id) {
    let labels      = dow.days,
        percentages = dow.percentages;

    let con    = $(`#${id}`).find(".canvas-container"),
        canvas = $(`#${id}`).find("canvas"),
	data   = {
	    labels: labels,
	    datasets: getRadarDataset("day", percentages)
        };
    drawRadarChart(canvas, con, data);
}


/** Populate the top 10 percent chart. */
function populateTop10PercentChart(stats, id) {
    let top10 = stats.n_tr_top_10_percent,
        bottom90 = stats.n_task_runs - top10,
        top10Label = "Most Active 10%: " + pluralise(top10, "contribution"),
        bottom90Label = "Remaining 90%: " + pluralise(bottom90, "contribution");

    let con       = $(`#${id}`).find(".canvas-container"),
        canvas    = $(`#${id}`).find("canvas"),
        legendCon = $(`#${id}`).find(".legend-container"),
	data = getDonutDataset(top10Label, top10, bottom90Label, bottom90);
    drawDonutChart(canvas, con, data, legendCon);
}


/** Populate the hourly activity chart. */
function populateHourlyActivityChart(hourlyActivity, id) {
    var labels      = [],
        percentages = [];
    for(var i = 0; i < hourlyActivity.length; i++) {
        hour = hourlyActivity[i][0] + ':00'
        if (hour.length < 5) {
            hour = '0' + hour;
        }
        labels.push(hour);
        percentages.push(hourlyActivity[i][1]);
    }

    let con    = $(`#${id}`).find(".canvas-container"),
        canvas = $(`#${id}`).find("canvas");
	data   = {
	    labels: labels,
	    datasets: getLineDataset("%", percentages)
	};
    drawLineChart(canvas, con, data);
}