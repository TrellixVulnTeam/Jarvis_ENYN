import time
import pyautogui
chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
"t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
"O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9",
"!", "§", "$", "%", "&", "/", "(", ")", "=", ".", "-", ",", "@", "€", "[", "]"]

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
done = False

def test(param, rep):
    if rep < 5:
        for n in numbers:
            print(param + str(n))
            #pyautogui.write(param+str(n))
            #pyautogui.press('enter')
            #pyautogui.click()
            #time.sleep(5)
            test(param + str(n), rep+1)
            """if [pyautogui.pixel(5,5)] != old_color:
                exit()
            else:
                old_color = [pyautogui.pixel(5,5)]"""


def testChars(param, rep):
    global old_color
    if rep < 10:
        for n in chars:
            print(param + str(n))
            #pyautogui.write(param+str(chars))
            #pyautogui.press('enter')
            #pyautogui.click()
            #time.sleep(5)
            test(param + str(n), rep+1)
            if [pyautogui.pixel(5,5)] != old_color:
                exit()
            else:
                old_color = [pyautogui.pixel(5,5)]

old_color = [pyautogui.pixel(5,5)]
#time.sleep(10)
test("", 0)
testChars("", 0)

