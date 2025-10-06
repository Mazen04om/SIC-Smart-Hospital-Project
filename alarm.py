from gpiozero import Button, LED

button1 = Button(16, pull_up = True)
button2 = Button(26, pull_up = True)
led1 = LED(24)
led2 = LED(25)

def get_help():
    try:
        if button1.is_pressed:
            led1.toggle()
        if button2.is_pressed:
            led2.toggle()
        print(button1.value,led1.value)
        return led1.value, led2.value


    except KeyboardInterrupt:
        print("\n Stopped by user.")

    return None, None
