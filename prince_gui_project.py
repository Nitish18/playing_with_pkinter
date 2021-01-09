import tkinter as tk
import PIL.Image, PIL.ImageTk
import cv2

from tkinter import messagebox
from tkinter import filedialog
from tkinter import Frame, Canvas, TOP, BOTTOM, NW



class HandleVideo():
    def __init__(self, window=None, video_frame=None, display_info_to_play_video=None):
        # defining canvas and frames

        self.window = window
        self.display_info_to_play_video = display_info_to_play_video

        self.top_frame = Frame(master=video_frame)
        self.top_frame.pack(side=TOP, pady=5)

        self.bottom_frame = Frame(master=video_frame)
        self.bottom_frame.pack(side=BOTTOM, pady=5)

        self.canvas = Canvas(self.top_frame)
        self.canvas.pack()

        self.pause = False
        self.cap = None

        self.delay = 1

    # Create an event handler
    def handle_select_file(self):
        print("Button is pressed - select file")

        self.pause = False
        filename = filedialog.askopenfilename(title="Select file", filetypes=(("MP4 files", "*.mp4"),
                                                                                            ("WMV files", "*.wmv"), ("AVI files", "*.avi")))
        # Open the video file
        self.cap = cv2.VideoCapture(filename)

        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.canvas.config(width = width, height =height)

        # showing info to play video
        self.display_info_to_play_video.pack()

    # Create an event handler
    def handle_play_video(self):
        # Get a frame from the video source, and go to the next frame automatically
        ret, frame = self.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = NW)

        if not self.pause:
            self.window.after(self.delay, self.handle_play_video)


    # Create an event handler
    def handle_pause_video(self):
        print("Button is pressed - pause video")
        self.pause = True


    # Create an event handler
    def handle_resume_video(self):
        print("Button is pressed - resume video")
        self.pause = False
        self.handle_play_video()


    def get_frame(self):   # get only one frame
        try:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        except:
            messagebox.showerror(title='Video file not found', message='Please select a video file.')


def main():
    window = tk.Tk()

    # defining 3 frames
    # frame 1: Project heading
    # frame 2: All buttons
    # frame 3: Screen where Video will be played
    frame1 = tk.Frame(master=window, width=100, height=30)
    frame1.pack()

    frame2 = tk.Frame(master=window, width=100, height=50)
    frame2.pack()

    frame3 = tk.Frame(master=window, width=100, height=50)
    frame3.pack()

    # main project heading
    main_project_heading = tk.Label(
        master=frame1,
        text="----------------------My Python GUI Project----------------------",
        fg="white",
        bg="black",
    )
    main_project_heading.pack()

    # text widget
    file_selected_name = tk.Label(
        master=frame1,
        text="----------------------File selected, click on Play to play the Video----------------------",
        fg="white",
        bg="black",
    )

    handle_video_obj = HandleVideo(window=window, video_frame=frame3, display_info_to_play_video=file_selected_name)

    # creating buttons - Select file button
    btn_select_file = tk.Button(text="Select File", command=handle_video_obj.handle_select_file, master=frame2)
    btn_select_file.pack()

    # creating buttons - Play video button
    btn_play_video = tk.Button(text="Play", command=handle_video_obj.handle_play_video, master=frame2)
    btn_play_video.pack()

    # creating buttons - Pause video button
    btn_pause_video = tk.Button(text="Pause", command=handle_video_obj.handle_pause_video, master=frame2)
    btn_pause_video.pack()

    # creating buttons - Resume video button
    btn_resume_video = tk.Button(text="Resume", command=handle_video_obj.handle_resume_video, master=frame2)
    btn_resume_video.pack()

    # creating buttons - Close window
    btn_close_window = tk.Button(text="Close window", command=window.destroy, master=frame2)
    btn_close_window.pack()


    # event listener
    window.mainloop()

if __name__ == "__main__":
    main()
