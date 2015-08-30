//首页情感仪表盘
function fillIndexOpinionGauge(ec,path){
    var myChart = ec.init(document.getElementById('indexopiniongauge'));
    myChart.showLoading({
         text:"图表正在努力加载中……"
        });

    var percentage = 100,negativePercentage= 0,positivePercentage=0;
    var value = positivePercentage-negativePercentage; // 0:100, 50:50 40:20 60:-20 100:0; -100~100
    // 基于准备好的dom，初始化echarts图表

    var option = {
        title: {
            text: '情感倾向',
            textStyle: {
                fontSize: 14,
                fontWeight: 'bolder',
                color: '#333'
            }
        },
        tooltip: {
            trigger: 'item', formatter: "负面声量占比 : " + negativePercentage
            + "%</br>正面声量占比 : " + positivePercentage
            + "%</br>中性声量占比 : " + percentage + "%</br>"
        },
        toolbox: {
            show : true,
            feature : {
                dataView : {show: true, readOnly: false},
            }
        },
        series: [
            {
                "name": "正负声量情感倾向",
                "type": "gauge",
                "startAngle": 180,
                "endAngle": 0,
                "center": ['50%', '75%'],
                "radius": ['75%', '120%'],
                "axisLine": {
                    "show": true,
                    "lineStyle": {
                        "color": [[50 / 100, '#ff3e7d'], [1, '#00a5ff']]
                    }
                },
                "pointer": {
                    length: '80%',
                    width: 8,
                    color: '#2E4893'
                },
                min: -100,
                max: 100,
                axisLabel: {
                    formatter: function (v) {
                        /*return (v-50)*2;*/
                        if (v == 100) return '(正面)100';
                        if (v == -100) return '-100(负面)';
                        if (v == 0) return '(中性)';
                        return v;
                    }
                },
                data: [{value: value, name: '情感倾向'}],
                detail: {show: true}
            }
        ]
    };
    //通过Ajax获取数据
    $.ajax({
        type: "post",
        async:true, //同步执行
        url:path,
        dataType: "json", //返回数据形式为json
        success: function (result) {
            if (result) {
                todayMention = result.todaymention;
                todayPositive = result.positivenum;
                todayNegative = result.negativenum;
                if(todayMention != 0){
                    positivePercentage = (todayPositive / todayMention).toFixed(2) * 100;
                    negativePercentage = (todayNegative / todayMention).toFixed(2) * 100;
                    percentage = ((todayMention-todayPositive-todayNegative) / todayMention).toFixed(2) * 100;
                }
                value = positivePercentage-negativePercentage;
                option.tooltip = {
                    trigger: 'item', formatter: "负面声量占比 : " + negativePercentage
                    + "%</br>正面声量占比 : " + positivePercentage
                    + "%</br>中性声量占比 : " + percentage + "%</br>"
                }
                option.series[0].data[0].value=value;
                myChart.hideLoading();
                myChart.setOption(option);
            }
        },
        error: function (errorMsg) {
            alert("图表请求数据加载失败，请刷新重试!");
        }
    });
}
//首页情感倾向走势
function fillIndexOpinionLine(ec,path){
        var myChart = ec.init(document.getElementById('indexopinionline'));
        myChart.showLoading({
             text:"图表正在努力加载中……"
            });
        var option = {
        title : {
        text: '一周舆情走势',
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            data:['正面声量','中性声量','负面声量']
        },
        toolbox: {
            show : true,
            feature : {
                dataView : {show: true, readOnly: false},
                magicType : {show: true, type: ['line', 'bar','stack','tiled']},
            }
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : ['周一','周二','周三','周四','周五','周六','周日']
            }
        ],
        yAxis : [
            {
                type : 'value',
                axisLabel : {
                    formatter: '{value} 条'
                }
            }
        ],
        series : [
            {
                name:'正面声量',
                type:'line',
                data:[120, 132, 101, 134, 90, 230, 210],
                markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                    ]
                },
                markLine : {
                    data : [
                        {type : 'average', name: '平均值'}
                    ]
                }
            },
            {
                name:'中性声量',
                type:'line',
                data:[220, 182, 191, 234, 290, 330, 310]
            },
            {
                name:'负面声量',
                type:'line',
                data:[150, 232, 201, 154, 190, 330, 410],
                markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                    ]
                },
                markLine : {
                    data : [
                        {type : 'average', name: '平均值'}
                    ]
                }
            }
        ]
    };
    //通过Ajax获取数据
    $.ajax({
        type: "post",
        async:true, //异步执行
        url: path,
        dataType: "json", //返回数据形式为json
        success: function (result) {
            if (result) {
                option.xAxis[0].data = result.week;
                option.series[0].data = result.positivenum;
                option.series[1].data = result.todaymention;
                option.series[2].data = result.negativenum;
                myChart.hideLoading();
                myChart.setOption(option);
            }
        },
        error: function (errorMsg) {
            alert("图表请求数据加载失败，请刷新重试!");
        }
    });

}

// 新闻页面分析

function createRandomItemStyle() {
    return {
        normal: {
            color: 'rgb(' + [
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160)
            ].join(',') + ')'
        }
    };
}
// 分析页面填充柱状图
function fillAnalysisBar(ec,path){
    var myChart = ec.init(document.getElementById('analysisbar'));
    myChart.showLoading({
         text:"图表正在努力加载中……"
        });
    var option = {
        title : {
        text: '今日热点',
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            data:['热点词']
        },
        toolbox: {
            show : true,
            feature : {
                dataView : {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar']},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        xAxis : [
            {
                type : 'value',
                boundaryGap : [0, 0.01]
            }
        ],
        yAxis : [
            {
                type : 'category',
                data : ['巴西','印尼','美国','印度','中国','世界人口(万)']
            }
        ],
        series : [
            {
                name:'热点词',
                type:'bar',
                data:[18203, 23489, 29034, 104970, 131744, 630230],
                itemStyle: {
                normal: {
                    color: function(params) {
                        // build a color map as your need.
                        var colorList = [
                          '#C1232B','#B5C334','#FCCE10','#E87C25','#27727B',
                           '#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD',
                           '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'
                        ];
                        return colorList[params.dataIndex]
                        }
                    }
                }
            }

        ]
    };
    //通过Ajax获取数据
    $.ajax({
        type: "post",
        async:true, //异步执行
        url: path,
        dataType: "json", //返回数据形式为json
        success: function (result) {
            if (result) {
                option.yAxis[0].data = result.words;
                option.series[0].data = result.values;
                myChart.hideLoading();
                myChart.setOption(option);
            }
        },
        error: function (errorMsg) {
            alert("图表请求数据加载失败，请刷新重试!");
        }
    });
}

// 分析页面填充字符云
function fillAnalysisWordsCloud(ec,path) {
    var myChart = ec.init(document.getElementById('analysiswordscloud'));
    myChart.showLoading({
        text: "图表正在努力加载中……"
    });

    var option = {
        title: {
            text: '今日热点词'
        },
        tooltip: {
            show: true
        },
        series: [{
            name: '今日热点词',
            type: 'wordCloud',
            size: ['100%', '100%'],
            textRotation : [0, 30, -30, 15,-15,45,-45],
            textPadding: 0,
            autoSize: {
                enable: true,
                minSize: 14
            },
            itemStyle: {
                normal: {
                    color: function(params) {
                        // build a color map as your need.
                        var colorList = [
                          '#C1232B','#B5C334','#FCCE10','#E87C25','#27727B',
                           '#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD',
                           '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'
                        ];
                        return colorList[params.dataIndex]
                    }
                }
            }
        }]
    };
    //通过Ajax获取数据
    $.ajax({
        type: "post",
        async:true, //异步执行
        url: path,
        dataType: "json", //返回数据形式为json
        success: function (result) {
            if (result) {
                option.series[0].data = result.data;
                myChart.hideLoading();
                myChart.setOption(option);
            }
        },
        error: function (errorMsg) {
            alert("图表请求数据加载失败，请刷新重试!");
        }
    });
}

// 分析页面填充关键词柱状图
function fillAnalysisKeyword(ec,path){
    var myChart = ec.init(document.getElementById('analysiskeyword'));
    myChart.showLoading({
         text:"图表正在努力加载中……"
        });
    var option = {
        title : {
        text: '今日关键词',
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            data:['关键词']
        },
        toolbox: {
            show : true,
            feature : {
                dataView : {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar']},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                data:['1','2']
            }
        ],
        yAxis : [
            {
                type : 'value'
            }
        ],
        series : [
            {
                name:'热点词',
                type:'bar',
                data:[18203, 23489, 29034, 104970, 131744, 630230],
                itemStyle: {
                normal: {
                    color: function(params) {
                        // build a color map as your need.
                        var colorList = [
                          '#C1232B','#B5C334','#FCCE10','#E87C25','#27727B',
                           '#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD',
                           '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'
                        ];
                        return colorList[params.dataIndex]
                        }
                    }
                }
            }

        ]
    };
    //通过Ajax获取数据
    $.ajax({
        type: "post",
        async:true, //异步执行
        url: path,
        dataType: "json", //返回数据形式为json
        success: function (result) {
            if (result) {
                option.xAxis[0].data = result.countword;
                option.series[0].data = result.countvalue;
                myChart.hideLoading();
                myChart.setOption(option);
            }
        },
        error: function (errorMsg) {
            alert("图表请求数据加载失败，请刷新重试!");
        }
    });
}

// 分析页面填充情感词图
function fillAnalysisEmotion(ec,path){
    var myChart = ec.init(document.getElementById('analysisemotion'));
    myChart.showLoading({
         text:"图表正在努力加载中……"
        });
    var option = {
        title : {
            text: '今日情感词'
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            x : 'right',
            y : 'bottom',
            data:['情感词']
        },
        toolbox: {
            show : true,
            feature : {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        polar : [
            {
                indicator : [
                    {text : '进攻', max  : 100},
                    {text : '防守', max  : 100},
                    {text : '体能', max  : 100},
                    {text : '速度', max  : 100},
                    {text : '力量', max  : 100},
                    {text : '技巧', max  : 100}
                ],
            }
        ],
        series : [
            {
                name: '实时情感情况',
                type: 'radar',
                size: ['80%', '80%'],
                itemStyle: {
                    normal: {
                        areaStyle: {
                            type: 'default'
                        }
                    }
                },
                data : [
                    {
                        value : [97, 42, 88, 94, 90, 86],
                        name : '情感词'
                    },
                ]
            }
        ]
    };
    //通过Ajax获取数据
    $.ajax({
        type: "post",
        async:true, //异步执行
        url: path,
        dataType: "json", //返回数据形式为json
        success: function (result) {
            if (result) {
                option.polar[0].indicator = result.countword;
                option.series[0].data[0].value = result.countvalue;
                myChart.hideLoading();
                myChart.setOption(option);
            }
        },
        error: function (errorMsg) {
            alert("图表请求数据加载失败，请刷新重试!");
        }
    });
}

//------------search-------------
// 搜索页面填充河流事件图
function fillSearchDetailLine(ec){
    var myChart = ec.init(document.getElementById('searchcountline'));
    myChart.showLoading({
         text:"图表正在努力加载中……"
        });
    var option = {
    title : {
        text: '搜索词声量变化统计',
    },
    tooltip : {
        trigger: 'item',
        enterable: true
    },
    legend: {
        data:['新闻声量', '微信声量','微博声量']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    xAxis : [
        {
            type : 'time',
            boundaryGap: [0.05,0.1]
        }
    ],
    series : [
        {
            "name": "财经事件",
            "type": "eventRiver",
            "weight": 123,
            "data": [
                {
                    "name": "阿里巴巴上市",
                    "weight": 123,
                    "evolution": [
                        {
                            "time": "2014-05-01",
                            "value": 14,
                        },
                        {
                            "time": "2014-05-02",
                            "value": 34,
                        },
                        {
                            "time": "2014-05-03",
                            "value": 60,
                        },
                        {
                            "time": "2014-05-04",
                            "value": 40,
                        },
                        {
                            "time": "2014-05-05",
                            "value": 10,
                        }
                    ]
                },
                {
                    "name": "阿里巴巴上市2",
                    "weight": 123,
                    "evolution": [
                        {
                            "time": "2014-05-02",
                            "value": 10,
                        },
                        {
                            "time": "2014-05-03",
                            "value": 34,
                        },
                        {
                            "time": "2014-05-04",
                            "value": 40,
                        },
                        {
                            "time": "2014-05-05",
                            "value": 10,
                        }
                    ]
                }
            ]
        }]
        };


    //通过Ajax获取数据
    $.ajax({
        type: "post",
        async:true, //异步执行
        url: '/search/ajax/count/',
        dataType: "json", //返回数据形式为json
        success: function (result) {
            if (result) {
                option.series = result.series
                myChart.hideLoading();
                myChart.setOption(option);
            }else{
                myChart.hideLoading();
                myChart.setOption(option);
            }
        },
        error: function (errorMsg) {
            alert("图表请求数据加载失败，请刷新重试!");
        }
    });
}

//详情页新闻微博微信走势
function fillDerailOpinionLine(ec,path){
        var myChart = ec.init(document.getElementById('indexopinionline'));
        myChart.showLoading({
             text:"图表正在努力加载中……"
            });
        var option = {
        title : {
        text: '一周舆情走势',
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            data:['新闻','微信','微博']
        },
        toolbox: {
            show : true,
            feature : {
                dataView : {show: true, readOnly: false},
                magicType : {show: true, type: ['line', 'bar','stack','tiled']},
            }
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : ['周一','周二','周三','周四','周五','周六','周日']
            }
        ],
        yAxis : [
            {
                type : 'value',
                axisLabel : {
                    formatter: '{value} 条'
                }
            }
        ],
        series : [
            {
                name:'新闻',
                type:'line',
                data:[120, 132, 101, 134, 90, 230, 210],
                markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                    ]
                },
                markLine : {
                    data : [
                        {type : 'average', name: '平均值'}
                    ]
                }
            },
            {
                name:'微信',
                type:'line',
                data:[220, 182, 191, 234, 290, 330, 310]
            },
            {
                name:'微博',
                type:'line',
                data:[150, 232, 201, 154, 190, 330, 410],
                markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                    ]
                },
                markLine : {
                    data : [
                        {type : 'average', name: '平均值'}
                    ]
                }
            }
        ]
    };
    //通过Ajax获取数据
    $.ajax({
        type: "post",
        async:true, //异步执行
        url: path,
        dataType: "json", //返回数据形式为json
        success: function (result) {
            if (result) {
                option.xAxis[0].data = result.week;
                option.series[0].data = result.newsresult;
                option.series[1].data = result.wechatresult;
                option.series[2].data = result.weiboresult;
                myChart.hideLoading();
                myChart.setOption(option);
            }
        },
        error: function (errorMsg) {
            alert("图表请求数据加载失败，请刷新重试!");
        }
    });

}

