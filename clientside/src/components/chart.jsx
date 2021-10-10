import React, { Component } from 'react';
import { range } from '../utils';
import { io } from 'socket.io-client';


class ChartComponent extends Component {
    constructor(props) {
        super(props)
        this.state = {
            epoch: 5,
            maskCompliance: 50,
            cells: [],
            infected: [],
            masked: [],
            normal: [],
            numInfected: 0,
            percentageInfected: 0,
            minutes: 0,
            hours: 0,
            numberOfPeople: 0
        }
        this.rowsNum = 20
        this.colsNum = 20
        this.rows = range(0, this.rowsNum)
        this.cols = range(0, this.colsNum)
        this.socket = null
    }

    componentDidMount() {
        const url = "http://localhost:5000/"
        this.socket = io(url, {
            reconnection: false,
            timeout: 3000
        })
        this.socket.on("connect", () => {
            console.log("connected to socket ", this.socket.id);
        })
        /*
        this.socket.on("cells", (data) => {
            this.setState({ cells: data })
        })
        */
        this.socket.on("cells_data", (data) => {
            this.setState({
                masked: data.masked,
                infected: data.infected,
                normal: data.normal,
            })
        })
        this.socket.on("stats", (data) => {
            this.setState({
                numberOfPeople: data.numberOfPeople,
                maskCompliance: data.maskCompliance,
                numInfected: data.numInfected,
                percentageInfected: data.percentageInfected,
                hours: data.hours,
                minutes: data.minutes,
                epoch: data.epoch
            })
        })
        this.socket.on("message", (data) => {
            alert(String(data))
        })
        this.socket.on("disconnect", () => {
            console.log("disconnected to socket!");
        })
    }

    componentWillUnmount() {
        this.socket.close()
    }

    getClass(row, col) {
        if (this.state.infected.indexOf(`${row},${col}`) + 1) {
            return "infected"
        }
        else if (this.state.masked.indexOf(`${row},${col}`) + 1) {
            return "masked"
        }
        else if (this.state.normal.indexOf(`${row},${col}`) + 1) {
            return "normal"
        } else {
            return "blank"
        }
    }

    render() {
        return (
            <React.Fragment>
                <div className="container py-3">
                    <h1 className="text-center">Covid 19 Simulator</h1>
                    <p className="text-center">A simulation of the spread of covid 19 in a room Using, Python and React!</p>
                    <div className="row py-2">
                        <div className="col-lg-8 border-1 border-dark">
                        {
                            this.rows.map((row, rowNum) => (
                                <div className="row" key={row}>
                                    {
                                        this.cols.map((col, colNum) => (
                                            <div key={col} className={`col-md-1 cell ${this.getClass(row,col)}`}>
                                            </div>
                                        ))
                                    }
                                </div>
                            ))
                        }
                    </div>
                        <div className="col-lg-4">
                            <div className="key row">
                                <div className="col-lg-4">
                                    <i className="bx bx-square bg-warning"></i> Wearing Mask
                                </div>
                                <div className="col-lg-4">
                                    <i className="bx bx-square bg-secondary"></i> Not Wearing Mask
                                </div>
                                <div className="col-lg-4">
                                    <i className="bx bx-square bg-danger"></i> Infected
                                </div>
                            </div>
                            <p>Mask Complience Rate { this.state.maskCompliance }</p>
                            <p>Total number of people { this.state.numberOfPeople }</p>
                            <p>Number of people infected { this.state.numInfected }</p>
                            <p>Time elapsed { this.state.hours }h { this.state.minutes }m</p>
                            <p>Epoch { this.state.epoch }</p>
                            <p>Most recent trials: </p>
                        </div>
                    </div>
                </div>
            </React.Fragment>
        )
    }
}

export default ChartComponent
