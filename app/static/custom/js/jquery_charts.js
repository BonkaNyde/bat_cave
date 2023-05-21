(function ($) {
	"use strict";

	$(function () {
		/*-------------------------------------
			Line Chart 
		-------------------------------------*/
		if ($("#earning-line-chart").length) {

			var lineChartData = {
				labels: ["", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", ""],
				datasets: [{
					data: [0, 5e4, 1e4, 5e4, 14e3, 7e4, 5e4, 75e3, 5e4],
					backgroundColor: '#ff0000',
					borderColor: '#ff0000',
					borderWidth: 1,
					pointRadius: 0,
					pointBackgroundColor: '#ff0000',
					pointBorderColor: '#ffffff',
					pointHoverRadius: 6,
					pointHoverBorderWidth: 3,
					fill: 'origin',
					label: "Total Collection"
				},
				{
					data: [0, 3e4, 2e4, 6e4, 7e4, 5e4, 5e4, 9e4, 8e4],
					backgroundColor: '#417dfc',
					borderColor: '#417dfc',
					borderWidth: 1,
					pointRadius: 0,
					pointBackgroundColor: '#304ffe',
					pointBorderColor: '#ffffff',
					pointHoverRadius: 6,
					pointHoverBorderWidth: 3,
					fill: 'origin',
					label: "Fees Collection"
				}
				]
			};
			var lineChartOptions = {
				responsive: true,
				maintainAspectRatio: false,
				animation: {
					duration: 2000
				},
				scales: {

					xAxes: [{
						display: true,
						ticks: {
							display: true,
							fontColor: "#222222",
							fontSize: 16,
							padding: 20
						},
						gridLines: {
							display: true,
							drawBorder: true,
							color: '#cccccc',
							borderDash: [5, 5]
						}
					}],
					yAxes: [{
						display: true,
						ticks: {
							display: true,
							autoSkip: true,
							maxRotation: 0,
							fontColor: "#646464",
							fontSize: 16,
							stepSize: 25000,
							padding: 20,
							callback: function (value) {
								var ranges = [{
									divider: 1e6,
									suffix: 'M'
								},
								{
									divider: 1e3,
									suffix: 'k'
								}
								];

								function formatNumber(n) {
									for (var i = 0; i < ranges.length; i++) {
										if (n >= ranges[i].divider) {
											return (n / ranges[i].divider).toString() + ranges[i].suffix;
										}
									}
									return n;
								}
								return formatNumber(value);
							}
						},
						gridLines: {
							display: true,
							drawBorder: false,
							color: '#cccccc',
							borderDash: [5, 5],
							zeroLineBorderDash: [5, 5],
						}
					}]
				},
				legend: {
					display: false
				},
				tooltips: {
					mode: 'index',
					intersect: false,
					enabled: true
				},
				elements: {
					line: {
						tension: .35
					},
					point: {
						pointStyle: 'circle'
					}
				}
			};
			var earningCanvas = $("#earning-line-chart").get(0).getContext("2d");
			var earningChart = new Chart(earningCanvas, {
				type: 'line',
				data: lineChartData,
				options: lineChartOptions
			});
		}

		/*-------------------------------------
			Bar Chart 
		-------------------------------------*/
		if ($("#expense-bar-chart").length) {

			var barChartData = {
				labels: ["Jan", "Feb", "Mar"],
				datasets: [{
					backgroundColor: ["#40dfcd", "#417dfc", "#ffaa01"],
					data: [125000, 100000, 75000, 50000, 150000],
					label: "Expenses (millions)"
				},]
			};
			var barChartOptions = {
				responsive: true,
				maintainAspectRatio: false,
				animation: {
					duration: 2000
				},
				scales: {

					xAxes: [{
						display: false,
						maxBarThickness: 100,
						ticks: {
							display: false,
							padding: 0,
							fontColor: "#646464",
							fontSize: 14,
						},
						gridLines: {
							display: true,
							color: '#e1e1e1',
						}
					}],
					yAxes: [{
						display: true,
						ticks: {
							display: true,
							autoSkip: false,
							fontColor: "#646464",
							fontSize: 14,
							stepSize: 25000,
							padding: 20,
							beginAtZero: true,
							callback: function (value) {
								var ranges = [{
									divider: 1e6,
									suffix: 'M'
								},
								{
									divider: 1e3,
									suffix: 'k'
								}
								];

								function formatNumber(n) {
									for (var i = 0; i < ranges.length; i++) {
										if (n >= ranges[i].divider) {
											return (n / ranges[i].divider).toString() + ranges[i].suffix;
										}
									}
									return n;
								}
								return formatNumber(value);
							}
						},
						gridLines: {
							display: true,
							drawBorder: true,
							color: '#e1e1e1',
							zeroLineColor: '#e1e1e1'

						}
					}]
				},
				legend: {
					display: false
				},
				tooltips: {
					enabled: true
				},
				elements: {}
			};
			var expenseCanvas = $("#expense-bar-chart").get(0).getContext("2d");
			var expenseChart = new Chart(expenseCanvas, {
				type: 'bar',
				data: barChartData,
				options: barChartOptions
			});
		}

		/*-------------------------------------
			Doughnut Chart 
		-------------------------------------*/
		if ($("#student-doughnut-chart").length) {

			var doughnutChartData = {
				labels: ["Female Students", "Male Students"],
				datasets: [{
					backgroundColor: ["#304ffe", "#ffa601"],
					data: [45000, 105000],
					label: "Total Students"
				},]
			};
			var doughnutChartOptions = {
				responsive: true,
				maintainAspectRatio: false,
				cutoutPercentage: 65,
				rotation: -9.4,
				animation: {
					duration: 2000
				},
				legend: {
					display: false
				},
				tooltips: {
					enabled: true
				},
			};
			var studentCanvas = $("#student-doughnut-chart").get(0).getContext("2d");
			var studentChart = new Chart(studentCanvas, {
				type: 'doughnut',
				data: doughnutChartData,
				options: doughnutChartOptions
			});
		}

		/*-------------------------------------
			Calender initiate 
		-------------------------------------*/
		if ($.fn.fullCalendar !== undefined) {
			$('#fc-calender').fullCalendar({
				header: {
					center: 'basicDay,basicWeek,month',
					left: 'title',
					right: 'prev,next',
				},
				fixedWeekCount: false,
				navLinks: true, // can click day/week names to navigate views
				editable: true,
				eventLimit: true, // allow "more" link when too many events
				aspectRatio: 1.8,
				events: [{
					title: 'All Day Event',
					start: '2019-04-01'
				},

				{
					title: 'Meeting',
					start: '2019-04-12T14:30:00'
				},
				{
					title: 'Happy Hour',
					start: '2019-04-15T17:30:00'
				},
				{
					title: 'Birthday Party',
					start: '2019-04-20T07:00:00'
				}
				]
			});
		}
	});

})(jQuery);
