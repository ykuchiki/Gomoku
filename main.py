import tkinter

from gomoenv import GomoEnv

if __name__ == "__main__":
    app = tkinter.Tk()
    app.title("五目並べ")
    GomoEnv = GomoEnv(app)
    app.mainloop()


