export const range = (start,stop, step=1) => {
    const array = []
    while (start < stop) {
        array.push(start)
        start += step
    }
    return array
}

export const random = (max) => {
    return parseInt(Math.random()*max)
}

export class Cell {
    constructor(x, y, infected, mask) {
        this.x = x
        this.y = y
        this.infected = infected
        this.mask = mask
    }
    
    color() {
        if (this.infected) {
            return "red"
        }
        else if (this.mask) {
            return "yellow"
        }
        else {
            return "gray"
        }
    }
}