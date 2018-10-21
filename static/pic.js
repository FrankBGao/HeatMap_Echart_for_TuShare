function heat_map(data) {
    myChart.hideLoading();

    var visualMin = -100;
    var visualMax = 100;
    var visualMinBound = -40;
    var visualMaxBound = 40;

    convertData(data);

    function convertData(originList) {
        var min = Infinity;
        var max = -Infinity;

        for (var i = 0; i < originList.length; i++) {
            var node = originList[i];
            if (node) {
                var value = node.value;
                value[2] != null && value[2] < min && (min = value[2]);
                value[2] != null && value[2] > max && (max = value[2]);
            }
        }

        for (var i = 0; i < originList.length; i++) {
            var node = originList[i];
            if (node) {
                var value = node.value;

                // Scale value for visual effect
                if (value[2] != null && value[2] > 0) {
                    value[3] = echarts.number.linearMap(
                        value[2], [0, max], [visualMaxBound, visualMax], true
                    );
                }
                else if (value[2] != null && value[2] < 0) {
                    value[3] = echarts.number.linearMap(
                        value[2], [min, 0], [visualMin, visualMinBound], true
                    );
                }
                else {
                    value[3] = 0;
                }

                if (!isFinite(value[3])) {
                    value[3] = 0;
                }

                if (node.children) {
                    convertData(node.children);
                }
            }
        }
    }


    function isValidNumber(num) {
        return num != null && isFinite(num);
    }

    myChart.setOption(option = {
        title: {
            left: 'center',
            text: '股价热力图',
            subtext: ''
        },
        tooltip: {
            formatter: function (info) {
                var value = info.value;

                var amount = value[2];
                amount = isValidNumber(amount)
                    ? echarts.format.addCommas(amount * 1000) + ''
                    : '-';

                var amount2011 = value[1];
                amount2011 = isValidNumber(amount2011)
                    ? echarts.format.addCommas(amount2011 * 1000) + ''
                    : '-';

                var change = value[0];
                change = isValidNumber(change)
                    ? change.toFixed(2) + '%'
                    : '-';

                return [
                    '<div class="tooltip-title">' + echarts.format.encodeHTML(info.name) + '</div>',
                    '1: &nbsp;&nbsp;' + amount2011 + '<br>',
                    '2: &nbsp;&nbsp;' + amount + '<br>',
                    '3: &nbsp;&nbsp;' + change
                ].join('');
            }
        },
        series: [{
            name: '股价',
            top: 80,
            type: 'treemap',
            label: {
                show: true,
                formatter: "{b}",
                normal: {
                    textStyle: {
                        ellipsis: true
                    }
                }
            },
            upperLabel: {
                normal: {
                    show: true,//false
                    height: 30
                }
            },
            itemStyle: {
                normal: {
                    borderColor: 'grey',

                }
            },
            levels: [
                {
                    upperLabel: {
                        normal: {
                            show: false,//false
                            height: 30
                        }
                    },
                    itemStyle: {
                        normal: {
                            borderWidth: 3,
                            gapWidth: 3
                        }
                    }

                },


            ],
            data: data
        }]
    });


}