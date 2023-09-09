import code
import sys

print("✨BackGround Color✨ \x1b[48;5;0m\\x1b[48;5;\x1b[48;5;1m?\x1b[48;5;0mm\x1b[0m")
for i in range (0,16):
  for j in range (0,16):
    code= str(i*16+j)
    sys.stdout.write("\x1b[48;5;"+code+"m" +code.ljust(4))
  print("\x1b[0m")
  
print("✨ForeGround Color✨ \x1b[48;5;0m\\x1b[38;5;\x1b[48;5;1m?\x1b[48;5;0mm\x1b[0m")
for i in range (0,16):
  for j in range (0,16):
    code= str(i*16+j)
    sys.stdout.write("\x1b[38;5;"+code+"m" +code.ljust(4))
  print("\x1b[0m")
print("✨Reset✨ \x1b[48;5;0m\\x1b[0m\x1b[0m")