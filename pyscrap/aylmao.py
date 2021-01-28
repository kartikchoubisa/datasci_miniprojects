class RadioButton:
    def __init__(self, location = (0,0), color = "#000000", text = "B"):
        self.location = location
        self.color = color
        self.text = text

        self.on = False
        self.size = (100,50)
        self.font_name = "Roboto-Regular.ttf"

        self.draw()

    def toggle(self):
        self.on = not self.on
        if self.on:
            self.font_name = "Roboto-Bold.ttf"
        else:
            self.font_name = "Roboto-Regular.ttf"

    def draw(self):
        print(f"pfunc: font loaded. {self.font_name=}")#font = loadFont(self.font_name)
        print(f"pfunc: text initialized. {self.size=}")#textFont(font, self.size)
        print(f"pfunc: text drawn. {self.text=}, {self.location=}")#text(self.text, self.location[0], self.location[1])

    def button_clicked(self):
        self.toggle()
        self.draw()

    def __repr__(self):
        return str(self.__dict__)

red_button = RadioButton(location = (5,5), color = "#FF0000", text="R")
print(red_button)
print("")

print(red_button.toggle())
print(red_button)


