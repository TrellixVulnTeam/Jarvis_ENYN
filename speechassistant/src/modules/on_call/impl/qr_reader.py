import qrcode

e = qrcode.Encoder()
image = e.encode("woah!", version=15, mode=e.mode.BINARY, eclevel=e.eclevel.H)
image.save("out.png")

d = qrcode.Decoder()
if d.decode("./resources/out.png"):
    print("result: " + d.result)
else:
    print("error: " + d.error)
