/*
 *
 * Copyright 2021 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
window.addEventListener("xlrelease.load", function() {
    window.xlrelease.queryTileData(function(response) {
		const chart = echarts.init(document.getElementById('main'), 'theme1');
		let rawData = response.data.data.pipelines;

		// Only report on pipelines that are running or have ran
		// Separate data representation from data presentation
		class STATUSES {
			// static created = 'Created';
			// static waiting_for_resource = 'Waiting for Resource';
			// static preparing = 'Preparing';
			// static pending = 'Pending';
			static running = 'Running';
			static success = 'Success';
			static failed = 'Failed';
			static canceled = 'Canceled';
			static skipped = 'Skipped';
			static manual = 'Manual';
			// static scheduled = 'Scheduled';
		}
		const selectedCategories = Object.values(STATUSES).map(s => s.toLowerCase().replace(/ /g,"_"));

		function getMappedData() {
			const data = _.orderBy(rawData, 'created_at')
			return data
				.filter(pipeline => 'status' in pipeline)
				.filter(pipeline => selectedCategories.includes(pipeline.status))
				.map(pipeline => {
					const {id, status, web_url, duration} = pipeline;
					return {
						name: id,
						value: duration,
						itemStyle: {
							color: getBarColor(status)
						},
						url: web_url,
						result: status,
						pipelineNumber: id
					}
				});
		}

		function drawLegend() {
			const legendEl = document.querySelector('.legend');
			Object.values(STATUSES).forEach(status => {
				const legendItem = document.createElement('div');
				const legendIcon = document.createElement('div');
				const legendText = document.createElement('div');
				legendItem.classList.add('legend-item');
				legendIcon.classList.add('icon');
				legendText.classList.add('text');
				legendText.innerHTML = `<span>${status}</span>`;
				legendIcon.style.backgroundColor = getBarColor(status);
				legendItem.appendChild(legendIcon);
				legendItem.appendChild(legendText);
				addLegendItemEventListener(legendItem, status.toLowerCase());
				legendEl.appendChild(legendItem);
			});
		}

		function addLegendItemEventListener(item, status) {
			item.addEventListener('click', () => {
				filterDataByStatus(status);
				const icon = item.querySelector('.icon');
				const text = item.querySelector('.text');
				if (selectedCategories.includes(status)) {
					icon.style.backgroundColor = getBarColor(status);
					text.style.color = 'black';
				} else {
					icon.style.backgroundColor = 'grey';
					text.style.color = 'grey';
				}
			})
		}

		function filterDataByStatus(status) {
			if (selectedCategories.includes(status)) {
				selectedCategories.splice(selectedCategories.indexOf(status), 1);
			} else {
				selectedCategories.push(status);
			}
			chart.setOption(getChartOptions());
		}

		function getChartOptions() {
			return {
				tooltip: {
					trigger: 'item',
					padding: 15,
					formatter: function (params) {
						const {value, pipelineNumber, result} = params.data;
						const duration = moment.duration(value, 'seconds');
						return `Pipeline Number: ${pipelineNumber} <br>
						Result: ${STATUSES[result]} <br>
						Execution took ${duration.humanize()}
						`;
					},
					backgroundColor: 'rgba(50,50,50,0.85)'
				},
				xAxis: {
					type: 'category',
					axisLabel: {
						show: false,
					}
				},
				yAxis: {
					type: 'value',
					axisLabel: {
						formatter: (function (value) {
							const seconds = (value % 60).toString();
							const minutes = (Math.floor(value / 60) % 60).toString();
							const hours = (Math.floor(value / 60 / 60) % 24).toString();
							return `${hours.padStart(2, '0')}:${minutes.padStart(2, '0')}:${seconds.padStart(2, '0')}`;
						}),
					},
					name: 'Duration',
					nameTextStyle: {
						fontWeight: 'bold',
					}
				},
				series: [
					{
						type: 'bar',
						barMinHeight: 10,
						data: getMappedData(),
						label: {
							show: false,
						},
					}
				]
			}
		};

		chart.setOption(getChartOptions());
		drawLegend();

		function getBarColor(result) {
			const resultLowerCase = result.toLowerCase();
			switch (resultLowerCase) {
				case 'failed':
					return '#db4545';
				case 'success':
					return '#39aa56'
				case 'running':
					return '#205AB7'
				default:
					return '#636363';
			}
		}

		chart.on('click', function (params) {
			const url = _.get(params, 'data.url');
			if (url) {
				window.open(url, '_blank');
			}
		});

		window.addEventListener('resize', () => {
			chart.resize();
		});

	});
});