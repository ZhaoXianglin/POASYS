(function(){

	//freeue-0201.html和freeue-0204.html 页面访问量统计表，使用echarts
	//Echart官网：http://echarts.baidu.com/doc/example.html
	function fillVisitGraph(){
		var myChart = echarts.init(document.getElementById('js-visit-graph'));
		myChart.setOption({
		    tooltip : {
		        trigger: 'axis'
		    },
		    legend: {
		        x : 'right',
		        y : 10,
		        data:['罗纳尔多','舍普琴科']
		    },
		    toolbox: {
		        show : false,
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
		            radius : 130
		        }
		    ],
		    series : [
		        {
		            name: '完全实况球员数据',
		            type: 'radar',
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
		                    name : '舍普琴科'
		                },
		                {
		                    value : [97, 32, 74, 95, 88, 92],
		                    name : '罗纳尔多'
		                }
		            ]
		        }
		    ]

		});
	}

	//freeue-0204.html页面最新动态表
	function fillTrendGraph(){
		var myChart = echarts.init(document.getElementById('js-trend-graph'));
		myChart.setOption({
		    tooltip : {
		        trigger: 'axis'
		    },
		    legend: {
		    	x : 'right',
		    	y : 10,
		        data:['意向','预购','成交']
		    },
		    toolbox: {
		        show : false,
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
		            type : 'value'
		        }
		    ],
		    series : [
		        {
		            name:'成交',
		            type:'line',
		            smooth:true,
		            itemStyle: {normal: {areaStyle: {type: 'default'}}},
		            data:[10, 12, 21, 54, 260, 830, 710]
		        },
		        {
		            name:'预购',
		            type:'line',
		            smooth:true,
		            itemStyle: {normal: {areaStyle: {type: 'default'}}},
		            data:[30, 182, 434, 791, 390, 30, 10]
		        },
		        {
		            name:'意向',
		            type:'line',
		            smooth:true,
		            itemStyle: {normal: {areaStyle: {type: 'default'}}},
		            data:[1320, 1132, 601, 234, 120, 90, 20]
		        }
		    ]

		});
	}

	//freeue-0204.hmtl页面访问量统计的圆形表
	function fillChordGraph(){
		var myChart = echarts.init(document.getElementById('js-chord-graph'));
		myChart.setOption({
		    color : [
		        '#FBB367','#80B1D2','#FB8070','#CC99FF','#B0D961',
		        '#99CCCC','#BEBBD8','#FFCC99','#8DD3C8','#FF9999',
		        '#CCEAC4','#BB81BC','#FBCCEC','#CCFF66','#99CC66',
		        '#66CC66','#FF6666','#FFED6F','#ff7f50','#87cefa',
		    ],
		    toolbox: {
		        show : false,
		    },
		    tooltip : {
		        trigger: 'item',
		        formatter : function (params) {
		            var g1 = params[1];
		            var serie = params[0];
		            var g2 = params[3];
		            var data = params[2];
		            var data2 = params[4];
		            if (data2) {
		                if (data > data2) {
		                    return [g1, serie, g2].join(' ');
		                } else {
		                    return [g2, serie, g1].join(' ');
		                }
		            } else {
		                return g1
		            }
		        }
		    },
		    legend : {
		        data : [
		            '美国',
		            '叙利亚反对派',
		            '阿萨德',
		            '伊朗',
		            '塞西',
		            '哈马斯',
		            '以色列',
		            '穆斯林兄弟会',
		            '基地组织',
		            '俄罗斯',
		            '黎巴嫩什叶派',
		            '土耳其',
		            '卡塔尔',
		            '沙特',
		            '黎巴嫩逊尼派',
		            '',
		            '支持',
		            '反对',
		            '未表态'
		        ],
		        orient : 'vertical',
		        x : 'left',
		        y : 30
		    },
		    series : [
		        {
		            "name": "支持",
		            "type": "chord",
		            "showScaleText": false,
		            "data": [
		                {"name": "美国"},
		                {"name": "叙利亚反对派"},
		                {"name": "阿萨德"},
		                {"name": "伊朗"},
		                {"name": "塞西"},
		                {"name": "哈马斯"},
		                {"name": "以色列"},
		                {"name": "穆斯林兄弟会"},
		                {"name": "基地组织"},
		                {"name": "俄罗斯"},
		                {"name": "黎巴嫩什叶派"},
		                {"name": "土耳其"},
		                {"name": "卡塔尔"},
		                {"name": "沙特"},
		                {"name": "黎巴嫩逊尼派"}
		            ],
		            "matrix": [
		                [0,100,0,0,0,0,100,0,0,0,0,0,0,0,0],
		                [10,0,0,0,0,10,10,0,10,0,0,10,10,10,10],
		                [0,0,0,10,0,0,0,0,0,10,10,0,0,0,0],
		                [0,0,100,0,0,100,0,0,0,0,100,0,0,0,0],
		                [0,0,0,0,0,0,0,0,0,0,0,0,0,10,0],
		                [0,100,0,10,0,0,0,0,0,0,0,0,10,0,0],
		                [10,100,0,0,0,0,0,0,0,0,0,0,0,0,0],
		                [0,0,0,0,0,0,0,0,0,0,0,10,10,0,0],
		                [0,100,0,0,0,0,0,0,0,0,0,0,0,0,0],
		                [0,0,100,0,0,0,0,0,0,0,0,0,0,0,0],
		                [0,0,100,10,0,0,0,0,0,0,0,0,0,0,0],
		                [0,100,0,0,0,0,0,100,0,0,0,0,0,0,0],
		                [0,100,0,0,0,100,0,100,0,0,0,0,0,0,0],
		                [0,100,0,0,100,0,0,0,0,0,0,0,0,0,100],
		                [0,100,0,0,0,0,0,0,0,0,0,0,0,10,0]
		            ]
		        },
		        {
		            "name": "反对",
		            "type": "chord",
		            "showScaleText": false,
		            "data": [
		                {"name": "美国"},
		                {"name": "叙利亚反对派"},
		                {"name": "阿萨德"},
		                {"name": "伊朗"},
		                {"name": "塞西"},
		                {"name": "哈马斯"},
		                {"name": "以色列"},
		                {"name": "穆斯林兄弟会"},
		                {"name": "基地组织"},
		                {"name": "俄罗斯"},
		                {"name": "黎巴嫩什叶派"},
		                {"name": "土耳其"},
		                {"name": "卡塔尔"},
		                {"name": "沙特"},
		                {"name": "黎巴嫩逊尼派"}
		            ],
		            "matrix": [
		                [0,0,100,100,0,100,0,0,100,0,0,0,0,0,0],
		                [0,0,0,10,0,0,0,0,0,10,10,0,0,0,0],
		                [10,0,0,0,0,0,10,10,10,0,0,10,10,0,10],
		                [10,100,0,0,0,0,0,0,0,0,0,0,0,0,0],
		                [0,0,0,0,0,10,0,100,0,0,0,10,10,0,0],
		                [10,0,0,0,100,0,10,0,0,0,0,0,0,0,0],
		                [0,0,100,0,0,100,0,0,0,0,0,0,0,0,0],
		                [0,0,100,0,10,0,0,0,0,0,0,0,0,10,0],
		                [10,0,100,0,0,0,0,0,0,0,0,0,0,100,0],
		                [0,100,0,0,0,0,0,0,0,0,0,0,0,0,0],
		                [0,100,0,0,0,0,0,0,0,0,0,0,0,0,0],
		                [0,0,100,0,100,0,0,0,0,0,0,0,0,0,0],
		                [0,0,100,0,100,0,0,0,0,0,0,0,0,0,0],
		                [0,0,0,0,0,0,0,100,10,0,0,0,0,0,0],
		                [0,0,100,0,0,0,0,0,0,0,0,0,0,0,0]
		            ]
		        },
		        {
		            "name": "未表态",
		            "type": "chord",
		            "showScaleText": false,
		            "data": [
		                {"name": "美国"},
		                {"name": "叙利亚反对派"},
		                {"name": "阿萨德"},
		                {"name": "伊朗"},
		                {"name": "塞西"},
		                {"name": "哈马斯"},
		                {"name": "以色列"},
		                {"name": "穆斯林兄弟会"},
		                {"name": "基地组织"},
		                {"name": "俄罗斯"},
		                {"name": "黎巴嫩什叶派"},
		                {"name": "土耳其"},
		                {"name": "卡塔尔"},
		                {"name": "沙特"},
		                {"name": "黎巴嫩逊尼派"}
		            ],
		            "matrix": [
		                [0,0,0,0,100,0,0,100,0,0,0,0,0,0,0],
		                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		                [10,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		                [10,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		            ]
		        }
		    ]

		});
	}

	fillVisitGraph();
	fillTrendGraph();
	fillChordGraph();	
})();