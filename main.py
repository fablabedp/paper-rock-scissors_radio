"""

A Paper, Rock, Scissors game played between two microbits via radio connection

It works with two microbits on the same radio channel.  If there are more than two, it will probably be a mess.

"""
# if we receive a number, we compare it with our hand to see who wins

def on_received_number(receivedNumber):
    global start, hand_sent
    if start:
        # we then change the game state  to "waiting", while we process the results of the game
        start = False
        if hand == 0:
            if receivedNumber == 0:
                draw()
            elif receivedNumber == 1:
                win()
            elif receivedNumber == 2:
                lose()
        elif hand == 1:
            if receivedNumber == 0:
                lose()
            elif receivedNumber == 1:
                draw()
            elif receivedNumber == 2:
                win()
        elif hand == 2:
            if receivedNumber == 0:
                win()
            elif receivedNumber == 1:
                lose()
            elif receivedNumber == 2:
                draw()
        # if the players were playing out of sink, and this microbit recieved a hand but hadn't yet sent one, we send it here to not keep the other microbit waiting.
        if not (hand_sent):
            radio.send_number(hand)
            hand_sent = True
        # wait a little bit with the game result on the display
        basic.pause(2500)
        # after processing the results of the game, we reset the variables to start again.
        init()
radio.on_received_number(on_received_number)

# if the game state is "ready", we can use the buttons to choose a hand

def on_button_pressed_a():
    global hand
    if start:
        hand += -1
        if hand < 0:
            hand = 2
        showHand()
input.on_button_pressed(Button.A, on_button_pressed_a)

def win():
    basic.show_icon(IconNames.HAPPY)
    music.play_tone(523, music.beat(BeatFraction.EIGHTH))
    basic.pause(50)
    music.play_tone(523, music.beat(BeatFraction.HALF))
def lose():
    basic.show_icon(IconNames.SAD)
def draw():
    basic.show_icon(IconNames.ASLEEP)
    music.play_tone(349, music.beat(BeatFraction.EIGHTH))
# change the game state to "ready"
# set the shake counter to 5
# choose a random hand
def init():
    global start, count, hand, hand_sent
    start = True
    # we use the "count" variable to keep track of how many times we have shaken the microbit
    count = 5
    # the "hand" variable stores what hand we want to play
    hand = randint(0, 2)
    # "hand_sent" is to know if we have sent our hand to the other player yet or not.  this way we can check at the end of the game if the other player is still waiting for us or not, in case we were shaking out of sync.
    hand_sent = False
    basic.show_icon(IconNames.YES)
# if we receive a string, it means there is another microbit wanting to connect to us.
# send a string in response, and initialise the game

def on_received_string(receivedString):
    if not (start):
        music.play_tone(523, music.beat(BeatFraction.EIGHTH))
        radio.send_string("hello!")
        init()
radio.on_received_string(on_received_string)

def on_button_pressed_b():
    global hand
    if start:
        hand += 1
        hand = hand % 3
        showHand()
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_gesture_shake():
    global count, hand_sent
    if start:
        # if the game state is ready, each time we shake the microbit we count down the shake counter
        count += -1
        if count == 4:
            # the first shake we hide the hand and replace it with a tick
            basic.show_icon(IconNames.YES)
        elif count == 3:
            music.play_tone(523, music.beat(BeatFraction.EIGHTH))
            # the next three shakes, we count down
            basic.show_number(count)
        elif count == 2:
            music.play_tone(659, music.beat(BeatFraction.EIGHTH))
            basic.show_number(count)
        elif count == 1:
            music.play_tone(784, music.beat(BeatFraction.EIGHTH))
            basic.show_number(count)
        elif count == 0:
            # on the final shake. we show our hand and send the hand number as a radio message
            showHand()
            music.play_tone(262, music.beat(BeatFraction.SIXTEENTH))
            music.play_tone(392, music.beat(BeatFraction.SIXTEENTH))
            music.play_tone(494, music.beat(BeatFraction.EIGHTH))
            music.play_tone(523, music.beat(BeatFraction.HALF))
            radio.send_number(hand)
            hand_sent = True
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

def showHand():
    if hand == 0:
        basic.show_icon(IconNames.SQUARE)
    elif hand == 1:
        basic.show_icon(IconNames.DIAMOND)
    elif hand == 2:
        basic.show_icon(IconNames.SCISSORS)
count = 0
hand_sent = False
hand = 0
start = False
# the start variable stores the game state for the microbit -
# false = "waiting": not yet connected to another microbit, or waiting for a new game to begin
# true = "ready": connected and ready to play
start = False
radio.set_group(1)
# while the microbit is not connected, keep sending a message on the radio channel until the game state changes
while not (start):
    music.play_tone(392, music.beat(BeatFraction.EIGHTH))
    radio.send_string("hello?")
    basic.show_icon(IconNames.SQUARE)
    basic.show_icon(IconNames.DIAMOND)
    basic.show_icon(IconNames.SCISSORS)
    if start:
        basic.show_icon(IconNames.YES)
# we don't need to do anything in the main program loop, everything in the code is triggered by events

def on_forever():
    pass
basic.forever(on_forever)
