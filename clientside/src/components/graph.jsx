import React from 'react';
import Highcharts from 'highcharts';
import { random } from '../utils';

class Graph extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            series: [
                {
                    name: 'Female',
                    color: 'red',
                    data: [[151.2, 53.1], [157.3, 51.0], [169.5, 69.2], 
                    [147.0, 50.0], [175.8, 83.6],
                    [150.0, 51.0], [151.1, 57.9], [156.0, 79.8], [146.2, 
                    46.8], [158.1, 74.9],
                    ]
                },
                {
                    name: 'Male',
                    color: 'blue',
                    data: [[172.0, 63.7], [165.3, 72.7], [183.5, 79.2], 
                    [176.5, 75.7], [177.2, 85.8],
                    [171.5, 64.8], [181, 82.4], [174.5, 77.4], [177.0, 61.0], 
                    [174.0, 83.7],
                    ]
                }
            ]
        }
    }

    highChartsRender() {
        Highcharts.chart({
            chart: {
              type: 'scatter',
              renderTo: 'atmospheric-composition'
            },
            title: {
              verticalAlign: 'middle',
              floating: true,
              text: 'Earth\'s Atmospheric Composition',
              style: {
                fontSize: '10px',
              }
            },
            plotOptions: {
              scatter: {
                dataLabels: {
                    format: '{point.name}: {point.percentage:.1f} %'
                },
                innerSize: '70%'
              }
            },
            series: this.state.series
        });
    }

    componentDidMount() {
        this.highChartsRender();
        
        setInterval(() => {
            this.setState({
                series: [
                    {
                        name: 'Female',
                        color: 'red',
                        data: [[random(40), random(40)], [random(40), random(40)], [random(40), random(40)], 
                        [random(40), random(40)], [random(40), random(40)],
                        [random(40), random(40)], [random(40), random(40)], [random(40), 79.8], [random(40), 
                        random(40)], [random(40), random(40)],
                        ]
                    },
                    {
                        name: 'Male',
                        color: 'blue',
                        data: [[random(40), random(40)], [random(40), random(40)], [random(40), random(40)], 
                        [random(40), random(40)], [random(40), random(40)],
                        [random(40), random(40)], [random(40), random(40)], [random(40), 79.8], [random(40), 
                        random(40)], [random(40), random(40)],
                        ]
                    }
                ]
            })
            this.highChartsRender()
        }, 2000)
    }

   	render() {
       	return (
            <div className="container">
                <div className="row">
                    <div className="col-md-6 mx-auto">
                        <div id="atmospheric-composition"></div>
                    </div>
                </div>
            </div>
       	);
   	}
}

export default Graph;