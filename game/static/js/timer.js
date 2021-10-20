let announceRound1 = true
let announceRound2 = true
let announceRound3 = true
let announceRound4 = true
let minute_multiplier = 60

function timer(roundZeroEndTime, roundOneEndTime, roundTwoEndTime, roundThreeEndTime){
    console.log("-----Timer")
    var now = new Date().getTime() / 1000
    now = Math.round(now)
    var endTime0 = roundZeroEndTime
    var timeLeft0 = endTime0 - now
    var min0 = Math.floor(timeLeft0/60)
    var sec0 = timeLeft0 % 60
    if(sec0 < 10) sec0 = "0"+sec0

    var endTime1 = roundOneEndTime
    var timeLeft1 = endTime1 - now 
    var min1 = Math.floor(timeLeft1/60)
    var sec1 = timeLeft1 % 60
    if(sec1 < 10) sec1 = "0"+sec1
    // document.getElementById('timer1').innerHTML = min1+":"+sec1
    var endTime2 = roundTwoEndTime
    var timeLeft2 = endTime2 - now 
    var min2 = Math.floor(timeLeft2/60)
    var sec2 = timeLeft2 % 60
    if(sec2 < 10) sec2 = "0"+sec2
    // document.getElementById('timer2').innerHTML = min2+":"+sec2
    var endTime3 = roundThreeEndTime
    var timeLeft3 = endTime3 - now 
    var min3 = Math.floor(timeLeft3/60)
    var sec3 = timeLeft3 % 60
    if(sec3 < 10) sec3 = "0"+sec3
    // document.getElementById('timer3').innerHTML = min3+":"+sec3
    if (roundOneEndTime == 0){
        document.getElementById('timer').innerHTML = "00:00"
        document.getElementById('round').innerHTML = "Get Ready"
    } else if(timeLeft0 > 0){
        document.getElementById('timer').innerHTML = min0+":"+sec0
        document.getElementById('round').innerHTML = "Pregame"
    } else if(timeLeft1 > 0){
        document.getElementById('timer').innerHTML = min1+":"+sec1
        document.getElementById('round').innerHTML = 1
    } else if(timeLeft2 > 0){
        document.getElementById('timer').innerHTML = min2+":"+sec2
        document.getElementById('round').innerHTML = 2
    } else if(timeLeft3 > 0){
        document.getElementById('timer').innerHTML = min3+":"+sec3
        document.getElementById('round').innerHTML = 3    
    } else {
        document.getElementById('timer').innerHTML = "00:00"
        document.getElementById('round').innerHTML = "Game Over"
    }

    let round = document.getElementById('round').innerHTML
    if(round == "1" && announceRound1 == true){
        console.log("round 1 start")
        announceRound1 = false
        var xhttp = new XMLHttpRequest()
        xhttp.open("GET", "/new_round/1", true)
        xhttp.send()        
    }
    else if(round == "2" && announceRound2 == true){
        console.log("round 2 start")
        announceRound2 = false
        var xhttp = new XMLHttpRequest()
        xhttp.open("GET", "/new_round/2", true)
        xhttp.send()        
    } else if(round == "3" && announceRound3 == true){
        console.log("round 3 start")
        announceRound3 = false
        var xhttp = new XMLHttpRequest()
        xhttp.open("GET", "/new_round/3", true)
        xhttp.send()        
    } else if(round == "Game Over" && announceRound4 == true) {
        console.log("---- round 4 hit")
        const url = "/new_round/4"
        fetch(url)
    }    

}  

