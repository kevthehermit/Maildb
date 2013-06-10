var Attoptions = {
            chart: {
                renderTo: 'attReport',
                type: 'bar'
            },
            title: {
                text: 'File Attatchments'
            },
            xAxis: {
                categories: []
            },
            yAxis: {
            	tickInterval: 1,
                min: 0,
                title: {
                    text: 'No Of Tasks'
                }
            },
            legend: {
                backgroundColor: '#FFFFFF',
                reversed: true
            },
            tooltip: {
                formatter: function() {
                    return ''+
                        this.series.name +': '+ this.y +'';
                }
            },
            plotOptions: {
                series: {
                    stacking: 'normal'
                }
            },
                series: []
        };




$.get('/static/graph/attReport.csv', function(data) {
    // Split the lines
    var lines = data.split('\n');
    
    // Iterate over the lines and add categories or series
    $.each(lines, function(lineNo, line) {
        var items = line.split(',');
        
        // header line containes categories
        if (lineNo == 0) {
            $.each(items, function(itemNo, item) {
                if (itemNo > 0) Attoptions.xAxis.categories.push(item);
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
            
            Attoptions.series.push(series);
    
        }
        
    });
    
    // Create the chart
    var chart = new Highcharts.Chart(Attoptions);
});
