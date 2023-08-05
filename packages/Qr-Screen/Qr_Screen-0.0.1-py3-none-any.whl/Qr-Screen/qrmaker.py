import qrcode

def qrmake(for_what_to_generate, filename):
    img = qrcode.make(for_what_to_generate)
    img.save(filename)