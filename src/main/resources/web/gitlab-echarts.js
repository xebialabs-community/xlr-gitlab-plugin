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
/*
Copyright 2020 XEBIALABS

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
function commitsTimelineSummary(response, id) {
    var dates = response.data.data.dates;
    var commitsEachDay = response.data.data.commitsEachDay;
    var dom = document.getElementById(id);
    var chart = echarts.init(dom);
    var option = {
        tooltip: {
            trigger: 'axis',
            position: function(pt) {
                return [pt[0], '10%'];
            }
        },
        toolbox: {
            right: '10%',
            feature: {
                dataZoom: {
                    yAxisIndex: 'none',
                    title: {
                        zoom: 'Zoom',
                        back: 'Back'
                    }
                },
                restore: {
                    title: "Restore"
                }
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: dates
        },
        yAxis: {
            type: 'value',
            boundaryGap: [0, '100%']
        },
        dataZoom: [{
            type: 'inside',
            start: 0,
            end: 100
        }, {
            start: 0,
            end: 10,
            handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
            handleSize: '80%',
            handleStyle: {
                color: '#fff',
                shadowBlur: 3,
                shadowColor: 'rgba(0, 0, 0, 0.6)',
                shadowOffsetX: 2,
                shadowOffsetY: 2
            }
        }],
        series: [{
            name: 'Commits',
            type: 'line',
            smooth: true,
            symbol: 'none',
            sampling: 'average',
            itemStyle: {
                color: 'rgb(255, 70, 131)'
            },
            areaStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgb(255, 158, 68)'
                }, {
                    offset: 1,
                    color: 'rgb(255, 70, 131)'
                }])
            },
            data: commitsEachDay
        }]
    };
    if (option && typeof option === "object") {
        chart.setOption(option, true);
    }
}

function contributionsSummary(response, id) {
    var authors = response.data.data.authors;
    var committers = response.data.data.committers;
    var people = response.data.data.people;
    var dom = document.getElementById(id);
    var chart = echarts.init(dom);
    var option = {
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} Commit(s) ({d}%)"
        },
        legend: {
            orient: 'vertical',
            type: 'scroll',
            x: 'left',
            data: people
        },
        series: [{
                name: 'Authors',
                type: 'pie',
                selectedMode: 'single',
                radius: [0, '45%'],
                label: {
                    normal: {
                        show: false
                    }
                },
                data: authors
            },
            {
                name: 'Committers',
                type: 'pie',
                radius: ['60%', '82.5%'],
                label: {
                    normal: {
                        show: false
                    }
                },
                data: committers
            }
        ]
    };
    if (option && typeof option === "object") {
        chart.setOption(option, true);
    }
}

function tagsTimelineSummary(response, id) {
    var dates = response.data.data.dates;
    var tagsEachDay = response.data.data.tagsEachDay;
    var tagNamesEachDay = response.data.data.tagNamesEachDay;
    var dom = document.getElementById(id);
    var chart = echarts.init(dom);
    var option = {
        tooltip: {
            trigger: 'axis',
            position: function(pt) {
                return [pt[0], '10%'];
            },
            formatter: '{b}<br/>{a0}: {c0}<br/>{a1}: {c1}',
            confine: true
        },
        toolbox: {
            right: '10%',
            feature: {
                dataZoom: {
                    yAxisIndex: 'none',
                    title: {
                        zoom: 'Zoom',
                        back: 'Back'
                    }
                },
                restore: {
                    title: "Restore"
                }
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: dates
        },
        yAxis: {
            type: 'value',
            boundaryGap: [0, '100%']
        },
        dataZoom: [{
            type: 'inside',
            start: 0,
            end: 100
        }, {
            start: 0,
            end: 10,
            handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
            handleSize: '80%',
            handleStyle: {
                color: '#fff',
                shadowBlur: 3,
                shadowColor: 'rgba(0, 0, 0, 0.6)',
                shadowOffsetX: 2,
                shadowOffsetY: 2
            }
        }],
        series: [{
                name: 'Tags Count',
                type: 'line',
                smooth: true,
                symbol: 'none',
                sampling: 'average',
                itemStyle: {
                    color: 'rgb(224, 61, 0)'
                },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                        offset: 0,
                        color: 'rgb(255, 123, 0)'
                    }, {
                        offset: 1,
                        color: 'rgb(255, 186, 0)'
                    }])
                },
                data: tagsEachDay
            },
            {
                name: 'Tags List',
                type: 'line',
                symbol: 'none',
                itemStyle: {
                    opacity: 0
                },
                data: tagNamesEachDay
            }
        ]
    };
    if (option && typeof option === "object") {
        chart.setOption(option, true);
    }
}
