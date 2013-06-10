var options2 = {
            chart: {
                renderTo: 'MonthTrend',
                type: 'line',
                marginRight: 130,
                marginBottom: 25
            },
            title: {
                text: 'Submission Trends',
                x: -20 //center
            },
            subtitle: {
                text: 'Date Range Here',
                x: -20
            },
            xAxis: {
            	title: {
                    text: 'Date'
                },
                categories: []
            },
            yAxis: {
                title: {
                    text: 'Count'
                },
                plotLines: [{
                    value: 1,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function() {
                        return '<b>'+ this.series.name +'</b><br/>'+
                        this.x +': '+ this.y +'Tasks';
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -10,
                y: 100,
                borderWidth: 0
            },
            series: []
        };



$.get('/static/graph/monthLine.csv', function(data) {
    // Split the lines
    var lines = data.split('\n');
    
    // Iterate over the lines and add categories or series
    $.each(lines, function(lineNo, line) {
        var items = line.split(',');
        
        // header line containes categories
        if (lineNo == 0) {
            $.each(items, function(itemNo, item) {
                if (itemNo > 0) options2.xAxis.categories.push(item);
            });
        }
        
        // the rest of the lines contain data with their name in the first position
        else {
            var series = {
                data: []
            };
            $.each(items, function(itemNo, item) {
                if (itemNo == 0) {
                    series.name = item;
                } else {
                    series.data.push(parseFloat(item));
                }
            });
            
            options2.series.push(series);
    
        }
        
    });
    
    // Create the chart2
    var chart = new Highcharts.Chart(options2);
});
