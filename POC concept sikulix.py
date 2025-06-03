from sikuli import *
import time

exe_path = "C:\\Users\\GrootSven\\AppData\\Local\\Programs\\Kadaster KLIC-viewer\\Kadaster KLIC-viewer.exe"

App.open(exe_path)
wait(10)
    

type(Key.ENTER)
   
if exists("1747135797760.png", 2):
   click("1747135797760.png")
   wait(1.5)
   pos = Env.getMouseLocation()
   new_x = pos.getX() + 40
   new_y = pos.getY()

   click(Location(new_x, new_y))
   
type(Key.BACKSPACE)


type('C:\Users\GrootSven\Downloads\\25G0020817_1')
type(Key.ENTER)
wait(0.2)
type(Key.TAB)
type(Key.ENTER)

wait(2.5)
type(Key.TAB)
type(Key.TAB)
type(Key.TAB)
type(Key.ENTER)
wait(1)

pattern = "1747136829995.png"
match = exists(pattern, 3)
wait(0.5)
if match:
    print("succes")
else: 
    print("no succes")


