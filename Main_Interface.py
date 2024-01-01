from tkinter import Tk, Canvas, Button, PhotoImage
import matplotlib.pyplot as plt

import Utilites

ASSETS_PATH = r"./assets/frame0/"


def main():
    window = Tk()
    icon = PhotoImage(file=ASSETS_PATH + 'CircuitK.png')
    window.wm_iconphoto(True, icon)

    window.title('Circuit K')
    window.geometry("630x550+80+150")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=630, bd=0)
    canvas.place(x=0, y=0)

    # Layout:
    image_image_1 = PhotoImage(file=ASSETS_PATH + "image_1.png")  # Yellow Rect
    canvas.create_image(250.0, 276.0, image=image_image_1)

    image_image_2 = PhotoImage(file=ASSETS_PATH + "image_2.png")  # Texts
    canvas.create_image(207, 77, image=image_image_2)

    image_image_3 = PhotoImage(file=ASSETS_PATH + "image_3.png")  # Gray Rect
    canvas.create_image(188, 290, image=image_image_3)

    image_image_4 = PhotoImage(file=ASSETS_PATH + "image_4.png")  # Window Title
    canvas.create_image(250, 33, image=image_image_4)

    canvas.create_rectangle(502.0, -5.0, 507.0, 550.0, fill="#495057", outline="")  # Vertical Line

    image_image_5 = PhotoImage(file=ASSETS_PATH + "image_5.png")  # Vertical Blue Rect
    canvas.create_image(568.0, 274.0, image=image_image_5)

    image_image_11 = PhotoImage(file=ASSETS_PATH + "image_6.png")  # DC Voltage
    canvas.create_image(567.0, 66.0, image=image_image_11)

    image_image_9 = PhotoImage(file=ASSETS_PATH + "image_7.png")  # DC Current
    canvas.create_image(566.0, 152, image=image_image_9)

    image_image_10 = PhotoImage(file=ASSETS_PATH + "image_8.png")  # AC Source
    canvas.create_image(567.0, 248.0, image=image_image_10)

    image_image_7 = PhotoImage(file=ASSETS_PATH + "image_9.png")  # Resistor
    canvas.create_image(568.0, 335.0, image=image_image_7)

    image_image_8 = PhotoImage(file=ASSETS_PATH + "image_10.png")  # Capacitor
    canvas.create_image(566.0, 412, image=image_image_8)

    image_image_6 = PhotoImage(file=ASSETS_PATH + "image_11.png")  # Inductor
    canvas.create_image(568.0, 490.0, image=image_image_6)

    tips_images = [PhotoImage(file=ASSETS_PATH + 'image_12.png'),
                   PhotoImage(file=ASSETS_PATH + 'image_13.png'),
                   PhotoImage(file=ASSETS_PATH + 'image_14.png'),
                   PhotoImage(file=ASSETS_PATH + 'image_16.png'),
                   PhotoImage(file=ASSETS_PATH + 'image_17.png'),
                   PhotoImage(file=ASSETS_PATH + 'image_18.png')]

    tips = [canvas.create_image(411.0, 247.0, image=tips_images[0]),
            canvas.create_image(250.0, 378.0, image=tips_images[1]),
            canvas.create_image(381.0, 176.0, image=tips_images[2]),
            canvas.create_image(242.0, 140.0, image=tips_images[3]),
            canvas.create_image(145.0, 394.0, image=tips_images[4]),
            canvas.create_image(370.0, 394.0, image=tips_images[5])]

    for tip in tips:
        canvas.itemconfig(tip, state="hidden")
    canvas.itemconfig(tips[0], state="normal")

    # Buttons:
    process_button_image = PhotoImage(file=ASSETS_PATH + "button_1.png")
    process_button = Button(image=process_button_image, borderwidth=0,
                            command=lambda: Utilites.validate(window))
    process_button.place(x=317, y=497, width=128.0, height=46.0)

    draw_circuit_button_image = PhotoImage(file=ASSETS_PATH + "button_2.png")
    draw_circuit_button = Button(image=draw_circuit_button_image, borderwidth=0,
                                 command=lambda: draw_schema())
    draw_circuit_button.place(x=58, y=497, width=196.0, height=46.0)

    add_field_button_image = PhotoImage(file=ASSETS_PATH + "button_3.png")
    add_field_button = Button(image=add_field_button_image, borderwidth=0,
                              command=lambda: Utilites.add_fields(window, canvas, tips, next_button, skip_button))
    add_field_button.place(x=44, y=441, width=154.0, height=30.0)

    clear_all_button_image = PhotoImage(file=ASSETS_PATH + "button_5.png")
    clear_all_button = Button(image=clear_all_button_image, borderwidth=0,
                              command=lambda: Utilites.clear_all())
    clear_all_button.place(x=369, y=65, width=107.0, height=41.0)

    next_button_image = PhotoImage(file=ASSETS_PATH + "button_6.png")
    next_button = Button(image=next_button_image, borderwidth=0,
                         command=lambda: Utilites.next_tip(canvas, tips, next_button, skip_button))
    next_button.place(x=287.0, y=19.0, width=96.0, height=29.0)

    skip_button_image = PhotoImage(file=ASSETS_PATH + "button_7.png")
    skip_button = Button(image=skip_button_image, borderwidth=0,
                         command=lambda: Utilites.skip_tips(canvas, tips, next_button, skip_button))
    skip_button.place(x=390.0, y=19.0, width=96.0, height=29.0)

    window.resizable(False, False)
    window.mainloop()


def draw_schema():
    Utilites.validate(None, 'Schema')


def run_circuit():
    from Circuits import Circuit
    #plt.switch_backend('TkAgg')  # Replace Pycharm Tkinter with Anti-Grain Geometry
    main_circuit = Circuit("assets/net/net.txt")
    return main_circuit


if __name__ == '__main__':
    main()
