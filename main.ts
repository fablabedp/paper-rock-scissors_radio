/**
 * A Paper, Rock, Scissors game played between two microbits via radio connection
 * 
 * It works with two microbits on the same radio channel.  If there are more than two, it will probably be a mess.
 */
// if we receive a number, we compare it with our hand to see who wins
radio.onReceivedNumber(function (receivedNumber) {
    if (start) {
        // we then change the game state  to "waiting", while we process the results of the game
        start = false
        if (hand == 0) {
            if (receivedNumber == 0) {
                draw()
            } else if (receivedNumber == 1) {
                win()
            } else if (receivedNumber == 2) {
                lose()
            }
        } else if (hand == 1) {
            if (receivedNumber == 0) {
                lose()
            } else if (receivedNumber == 1) {
                draw()
            } else if (receivedNumber == 2) {
                win()
            }
        } else if (hand == 2) {
            if (receivedNumber == 0) {
                win()
            } else if (receivedNumber == 1) {
                lose()
            } else if (receivedNumber == 2) {
                draw()
            }
        }
        // if the players were playing out of sink, and this microbit recieved a hand but hadn't yet sent one, we send it here to not keep the other microbit waiting.
        if (!(hand_sent)) {
            radio.sendNumber(hand)
            hand_sent = true
        }
        // wait a little bit with the game result on the display
        basic.pause(2500)
        // after processing the results of the game, we reset the variables to start again.
        init()
    }
})
// if the game state is "ready", we can use the buttons to choose a hand
input.onButtonPressed(Button.A, function () {
    if (start) {
        hand += -1
        if (hand < 0) {
            hand = 2
        }
        showHand()
    }
})
function win () {
    basic.showIcon(IconNames.Happy)
    music.playTone(523, music.beat(BeatFraction.Eighth))
    basic.pause(50)
    music.playTone(523, music.beat(BeatFraction.Half))
}
function lose () {
    basic.showIcon(IconNames.Sad)
}
function draw () {
    basic.showIcon(IconNames.Asleep)
    music.playTone(349, music.beat(BeatFraction.Eighth))
}
// change the game state to "ready"
// set the shake counter to 5
// choose a random hand
function init () {
    start = true
    // we use the "count" variable to keep track of how many times we have shaken the microbit
    count = 5
    // the "hand" variable stores what hand we want to play
    hand = randint(0, 2)
    // "hand_sent" is to know if we have sent our hand to the other player yet or not.  this way we can check at the end of the game if the other player is still waiting for us or not, in case we were shaking out of sync.
    hand_sent = false
    basic.showIcon(IconNames.Yes)
}
// if we receive a string, it means there is another microbit wanting to connect to us.
// send a string in response, and initialise the game
radio.onReceivedString(function (receivedString) {
    if (!(start)) {
        music.playTone(523, music.beat(BeatFraction.Eighth))
        radio.sendString("hello!")
        init()
    }
})
input.onButtonPressed(Button.B, function () {
    if (start) {
        hand += 1
        hand = hand % 3
        showHand()
    }
})
input.onGesture(Gesture.Shake, function () {
    if (start) {
        // if the game state is ready, each time we shake the microbit we count down the shake counter
        count += -1
        if (count == 4) {
            // the first shake we hide the hand and replace it with a tick
            basic.showIcon(IconNames.Yes)
        } else if (count == 3) {
            music.playTone(523, music.beat(BeatFraction.Eighth))
            // the next three shakes, we count down
            basic.showNumber(count)
        } else if (count == 2) {
            music.playTone(659, music.beat(BeatFraction.Eighth))
            basic.showNumber(count)
        } else if (count == 1) {
            music.playTone(784, music.beat(BeatFraction.Eighth))
            basic.showNumber(count)
        } else if (count == 0) {
            // on the final shake. we show our hand and send the hand number as a radio message
            showHand()
            music.playTone(262, music.beat(BeatFraction.Sixteenth))
            music.playTone(392, music.beat(BeatFraction.Sixteenth))
            music.playTone(494, music.beat(BeatFraction.Eighth))
            music.playTone(523, music.beat(BeatFraction.Half))
            radio.sendNumber(hand)
            hand_sent = true
        }
    }
})
function showHand () {
    if (hand == 0) {
        basic.showIcon(IconNames.Square)
    } else if (hand == 1) {
        basic.showIcon(IconNames.Diamond)
    } else if (hand == 2) {
        basic.showIcon(IconNames.Scissors)
    }
}
let count = 0
let hand_sent = false
let hand = 0
let start = false
// the start variable stores the game state for the microbit -
// false = "waiting": not yet connected to another microbit, or waiting for a new game to begin
// true = "ready": connected and ready to play
start = false
radio.setGroup(1)
// while the microbit is not connected, keep sending a message on the radio channel until the game state changes
while (!(start)) {
    music.playTone(392, music.beat(BeatFraction.Eighth))
    radio.sendString("hello?")
    basic.showIcon(IconNames.Square)
    basic.showIcon(IconNames.Diamond)
    basic.showIcon(IconNames.Scissors)
    if (start) {
        basic.showIcon(IconNames.Yes)
    }
}
// we don't need to do anything in the main program loop, everything in the code is triggered by events
basic.forever(function () {
	
})
