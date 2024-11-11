(function ($) {

  'use strict';
  $(function () {

    ////////////////////////////////////////////////

    // Assuming you have the API response stored in a variable called apiResponse
    const apiResponse = {
      "last_week": [
        { "mon": 400.0 }, { "tue": 200.0 }, { "wed": 300.0 },
        { "thu": 450.0 }, { "fri": 515.0 }, { "sat": 460.0 },
        { "sun": 570.0 }
      ],
      "current_week": [
        { "mon": 440.0 }, { "tue": 1000.0 }, { "wed": 394.0 },
        { "thu": 360.0 }, { "fri": 550.0 }, { "sat": 880.0 },
        { "sun": 440.0 }
      ]
    };

    // Extract data for last week
    const lastWeekData = apiResponse.last_week.map(day => Object.values(day)[0]);

    // Extract data for current week
    const currentWeekData = apiResponse.current_week.map(day => Object.values(day)[0]);

    if ($("#performanceLine").length) {
      const ctx = document.getElementById('performanceLine');
      const chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ["MON", "TUE", "WED", "THU", "FRI", "SAT","SUN"],
          datasets: [{
            label: 'This week',
            data: currentWeekData,
            backgroundColor: 'rgba(26, 115, 232, 0.18)',
            borderColor: '#1F3BB3',
            borderWidth: 1.5,
            fill: true,
            pointRadius: 4,
            pointBackgroundColor: '#1F3BB3',
            pointBorderColor: '#fff',
            pointHoverRadius: 6,
          }, {
            label: 'Last week',
            data: lastWeekData,
            backgroundColor: 'rgba(0, 208, 255, 0.19)',
            borderColor: '#52CDFF',
            borderWidth: 1.5,
            fill: true,
            pointRadius: 6, // Slightly larger point for last week
            pointBackgroundColor: '#52CDFF',
            pointBorderColor: '#fff',
            pointHoverRadius: 8,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          elements: {
            line: {
              tension: 0.4,
            }
          },
          scales: {
            y: {
              border: {
                display: false
              },
              grid: {
                display: true,
                color: "#F0F0F0",
                drawBorder: false,
              },
              ticks: {
                beginAtZero: false,
                autoSkip: true,
                maxTicksLimit: 4,
                color: "#6B778C",
                font: {
                  size: 10,
                }
              }
            },
            x: {
              border: {
                display: false
              },
              grid: {
                display: false,
                drawBorder: false,
              },
              ticks: {
                beginAtZero: false,
                autoSkip: true,
                maxTicksLimit: 7,
                color: "#6B778C",
                font: {
                  size: 10,
                }
              }
            }
          },
          plugins: {
            legend: {
              display: false,
            }
          }
        }
      });

      // Add click event listener to the chart
      ctx.onclick = function (evt) {
        const activePoints = chart.getElementsAtEventForMode(evt, 'nearest', { intersect: true }, false);
        if (activePoints.length) {
          const { index } = activePoints[0];
          const dayLabel = chart.data.labels[index];
          const currentWeekAmount = currentWeekData[index];
          const lastWeekAmount = lastWeekData[index];

          showMsg(`Day: ${dayLabel}\nCurrent Week Amount: ${currentWeekAmount}\nLast Week Amount: ${lastWeekAmount}`);
        }
      };
    }



    //////////////////////////////////////////////////


    if ($("#status-summary").length) {
      const statusSummaryChartCanvas = document.getElementById('status-summary');
      new Chart(statusSummaryChartCanvas, {
        type: 'line',
        data: {
          labels: ["SUN", "MON", "TUE", "WED", "THU", "FRI"],
          datasets: [{
            label: '# of Votes',
            data: [50, 68, 70, 10, 12, 80],
            backgroundColor: "#ffcc00",
            borderColor: [
              '#01B6A0',
            ],
            borderWidth: 2,
            fill: false, // 3: no fill
            pointBorderWidth: 0,
            pointRadius: [0, 0, 0, 0, 0, 0],
            pointHoverRadius: [0, 0, 0, 0, 0, 0],
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          elements: {
            line: {
              tension: 0.4,
            }
          },
          scales: {
            y: {
              border: {
                display: false
              },
              display: false,
              grid: {
                display: false,
              },
            },
            x: {
              border: {
                display: false
              },
              display: false,
              grid: {
                display: false,
              }
            }
          },
          plugins: {
            legend: {
              display: false,
            }
          }
        }
      });
    }

    if ($("#marketingOverview").length) {
      const marketingOverviewCanvas = document.getElementById('marketingOverview');
      new Chart(marketingOverviewCanvas, {
        type: 'bar',
        data: {
          labels: ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
          datasets: [{
            label: 'Last week',
            data: [110, 220, 200, 190, 220, 110, 210, 110, 205, 202, 201, 150],
            backgroundColor: "#52CDFF",
            borderColor: [
              '#52CDFF',
            ],
            borderWidth: 0,
            barPercentage: 0.35,
            fill: true, // 3: no fill

          }, {
            label: 'This week',
            data: [215, 290, 210, 250, 290, 230, 290, 210, 280, 220, 190, 300],
            backgroundColor: "#1F3BB3",
            borderColor: [
              '#1F3BB3',
            ],
            borderWidth: 0,
            barPercentage: 0.35,
            fill: true, // 3: no fill
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          elements: {
            line: {
              tension: 0.4,
            }
          },

          scales: {
            y: {
              border: {
                display: false
              },
              grid: {
                display: true,
                drawTicks: false,
                color: "#F0F0F0",
                zeroLineColor: '#F0F0F0',
              },
              ticks: {
                beginAtZero: false,
                autoSkip: true,
                maxTicksLimit: 4,
                color: "#6B778C",
                font: {
                  size: 10,
                }
              }
            },
            x: {
              border: {
                display: false
              },
              stacked: true,
              grid: {
                display: false,
                drawTicks: false,
              },
              ticks: {
                beginAtZero: false,
                autoSkip: true,
                maxTicksLimit: 7,
                color: "#6B778C",
                font: {
                  size: 10,
                }
              }
            }
          },
          plugins: {
            legend: {
              display: false,
            }
          }
        },
        plugins: [{
          afterDatasetUpdate: function (chart, args, options) {
            const chartId = chart.canvas.id;
            var i;
            const legendId = `${chartId}-legend`;
            const ul = document.createElement('ul');
            for (i = 0; i < chart.data.datasets.length; i++) {
              ul.innerHTML += `
                  <li>
                    <span style="background-color: ${chart.data.datasets[i].borderColor}"></span>
                    ${chart.data.datasets[i].label}
                  </li>
                `;
            }
            return document.getElementById(legendId).appendChild(ul);
          }
        }]
      });
    }

    if ($('#totalVisitors').length) {
      var bar = new ProgressBar.Circle(totalVisitors, {
        color: '#fff',
        // This has to be the same size as the maximum width to
        // prevent clipping
        strokeWidth: 15,
        trailWidth: 15,
        easing: 'easeInOut',
        duration: 1400,
        text: {
          autoStyleContainer: false
        },
        from: {
          color: '#52CDFF',
          width: 15
        },
        to: {
          color: '#677ae4',
          width: 15
        },
        // Set default step function for all animate calls
        step: function (state, circle) {
          circle.path.setAttribute('stroke', state.color);
          circle.path.setAttribute('stroke-width', state.width);

          var value = Math.round(circle.value() * 100);
          if (value === 0) {
            circle.setText('');
          } else {
            circle.setText(value);
          }

        }
      });

      bar.text.style.fontSize = '0rem';
      bar.animate(.64); // Number from 0.0 to 1.0
    }

    if ($('#visitperday').length) {
      var bar = new ProgressBar.Circle(visitperday, {
        color: '#fff',
        // This has to be the same size as the maximum width to
        // prevent clipping
        strokeWidth: 15,
        trailWidth: 15,
        easing: 'easeInOut',
        duration: 1400,
        text: {
          autoStyleContainer: false
        },
        from: {
          color: '#34B1AA',
          width: 15
        },
        to: {
          color: '#677ae4',
          width: 15
        },
        // Set default step function for all animate calls
        step: function (state, circle) {
          circle.path.setAttribute('stroke', state.color);
          circle.path.setAttribute('stroke-width', state.width);

          var value = Math.round(circle.value() * 100);
          if (value === 0) {
            circle.setText('');
          } else {
            circle.setText(value);
          }

        }
      });

      bar.text.style.fontSize = '0rem';
      bar.animate(.34); // Number from 0.0 to 1.0
    }

    if ($("#doughnutChart").length) {
      const doughnutChartCanvas = document.getElementById('doughnutChart');
      new Chart(doughnutChartCanvas, {
        type: 'doughnut',
        data: {
          labels: ['Total', 'Net', 'Gross', 'AVG'],
          datasets: [{
            data: [40, 20, 30, 10],
            backgroundColor: [
              "#1F3BB3",
              "#FDD0C7",
              "#52CDFF",
              "#81DADA"
            ],
            borderColor: [
              "#1F3BB3",
              "#FDD0C7",
              "#52CDFF",
              "#81DADA"
            ],
          }]
        },
        options: {
          cutout: 90,
          animationEasing: "easeOutBounce",
          animateRotate: true,
          animateScale: false,
          responsive: true,
          maintainAspectRatio: true,
          showScale: true,
          legend: false,
          plugins: {
            legend: {
              display: false,
            }
          }
        },
        plugins: [{
          afterDatasetUpdate: function (chart, args, options) {
            const chartId = chart.canvas.id;
            var i;
            const legendId = `${chartId}-legend`;
            const ul = document.createElement('ul');
            for (i = 0; i < chart.data.datasets[0].data.length; i++) {
              ul.innerHTML += `
                  <li>
                    <span style="background-color: ${chart.data.datasets[0].backgroundColor[i]}"></span>
                    ${chart.data.labels[i]}
                  </li>
                `;
            }
            return document.getElementById(legendId).appendChild(ul);
          }
        }]
      });
    }

    if ($("#leaveReport").length) {
      const leaveReportCanvas = document.getElementById('leaveReport');
      new Chart(leaveReportCanvas, {
        type: 'bar',
        data: {
          labels: ["Jan", "Feb", "Mar", "Apr", "May"],
          datasets: [{
            label: 'Last week',
            data: [18, 25, 39, 11, 24],
            backgroundColor: "#52CDFF",
            borderColor: [
              '#52CDFF',
            ],
            borderWidth: 0,
            fill: true, // 3: no fill
            barPercentage: 0.5,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          elements: {
            line: {
              tension: 0.4,
            }
          },
          scales: {
            y: {
              border: {
                display: false
              },
              display: true,
              grid: {
                display: false,
                drawBorder: false,
                color: "rgba(255,255,255,.05)",
                zeroLineColor: "rgba(255,255,255,.05)",
              },
              ticks: {
                beginAtZero: true,
                autoSkip: true,
                maxTicksLimit: 5,
                fontSize: 10,
                color: "#6B778C",
                font: {
                  size: 10,
                }
              }
            },
            x: {
              border: {
                display: false
              },
              display: true,
              grid: {
                display: false,
              },
              ticks: {
                beginAtZero: false,
                autoSkip: true,
                maxTicksLimit: 7,
                fontSize: 10,
                color: "#6B778C",
                font: {
                  size: 10,
                }
              }
            }
          },
          plugins: {
            legend: {
              display: false,
            }
          }
        }
      });
    }

  });
  // iconify.load('icons.svg').then(function() {
  //   iconify(document.querySelector('.my-cool.icon'));
  // });


})(jQuery);