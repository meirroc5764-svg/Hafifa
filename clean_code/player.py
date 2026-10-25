from mutagen.easyid3 import EasyID3
import pygame
from tkinter.filedialog import askopenfilenames
from tkinter import Button, Label, Frame, Text, Tk, WORD, END


pygame.init()



class FrameApp(Frame):
    def __init__(self,master):
        super().__init__(master)

        '''constractor'''

        self.songs_list = []
        self.songs_index = 0
        self.pausing = False
        self.SONG_END = pygame.USEREVENT + 1
        self.grid()

        '''General settings and button design
        Black color, default font'''

        self.wight_label_1 = Label(self, fg='Black',font=('Helvetica 12 bold italic',10),bg='ivory2')
        self.wight_label_1.grid(row=6,column=0)
        self.format_text_1 = Text(wrap=WORD,width=60)
        self.format_text_1.grid(row=8,column=0)
        self.create_button()


    '''functionality and function
        invocation for each button'''
    def create_button(self):

        BUTTON_WIDTH = 40

        play_song_button = Button(self, text="PLAY SONG",command=self.play_song,bg='AntiqueWhite1',width=BUTTON_WIDTH)
        play_song_button.grid(row=2,column=0)
        
        previos_song_button = Button(self, text="PREVIOUS SONG",command=self.previos_song,bg='AntiqueWhite1',width=BUTTON_WIDTH)
        previos_song_button.grid(row=4,column=0)
        
        pause_and_unpause_button = Button(self, text="PAUSE/UNPAUSE",command=self.pause_and_unpause_song,bg='AntiqueWhite1',width=BUTTON_WIDTH)
        pause_and_unpause_button.grid(row=3,column=0)
        
        next_song_button = Button(self, text="NEXT SONG",command=self.next_song,bg='AntiqueWhite1',width=BUTTON_WIDTH)
        next_song_button.grid(row=5,column=0)

        
        add_a_song_button = Button(self, text="ADD TO LIST",command= self.addToList, bg='AntiqueWhite1', width=BUTTON_WIDTH)
        add_a_song_button.grid(row=1,column=0)
        

        
        
    #################################################################################
    
    '''the function save a song to list of songs
    and veiw to user'''
    def addToList(self):
        try:

            self.directory = askopenfilenames()

            #save songs in songs_list
            self.save_songs()

            #veiw songs from user
            self.veiw_song()

        except Exception as error:
            print(error)


    def save_songs(self):
        for song_dir in self.directory:
            print(song_dir)
            self.songs_list.append(song_dir)
        self.format_text_1.delete(0.0, END)

    
    def veiw_song(self):
        for key, item in enumerate(self.songs_list):
                        song = EasyID3(item)
                        song_info = f"{key + 1}: {song['title'][0]} - {song['artist'][0]}"
                        self.format_text_1.insert(END, song_info + '\n')

    #################################################################################
    
    '''veiw the data about curent song
    return a string message witn number title and the artist the song'''
    def song_data(self):
        song_index = self.songs_list[self.songs_index]
        song_number = song_index + 1
        try:
            song = EasyID3(song_index)
            song_data = f"Now playing: Nr: {song_number}  \
                        {song['title']} +  -  + {song['artist']}"
            return song_data
        
        except Exception as error:
            print(error)
    #################################################################################
    
    '''the function find a song by index and play it'''
    def play_song(self):
        
        try:
            directory = self.songs_list[self.songs_index]
            
            pygame.mixer.music.load(directory)
            pygame.mixer.music.play(1, 0.0)
            pygame.mixer.music.set_endevent(self.SONG_END)
            
            self.pausing = False
            
            self.wight_label_1['text'] = self.song_data()
        
        except Exception as error:
            print(error)
    #################################################################################
    
    '''check if the music and if it continue next song'''
    def check_music(self):
            
        for event in pygame.event.get():
            if event.type == self.SONG_END:
                self.next_song()

    #################################################################################
    
    def pause_and_unpause_song(self):
        try:
            if self.pausing:
                pygame.mixer.music.unpause()
                pausing = False
            
            elif not pausing:
                pygame.mixer.music.pause()
                pausing = True
        
        except Exception as error:
            print(error)
    #################################################################################
    
    '''the function get to next is check if curent song
    is the last if it is not the lest add to index one else go to first'''
    def get_next_song(self):
        try:
           
            if self.songs_index + 1 < len(self.songs_list):
                return self.songs_index + 1
            
            else:
                return 0
        
        except Exception as error:
            print(error)
            return self.songs_index
    #################################################################################
    
    def next_song(self):
        try:
            self.songs_index = self.get_next_song()
            self.play_song()
        
        except Exception as error:
            print(error)
    #################################################################################
    
    def get_previous_song(self):
        
        try:
            
            if self.songs_index - 1 >= 0:
                return self.songs_index - 1
           
            else:
                return len(self.songs_list) - 1
        
        except Exception as error:
            print(error)
    #################################################################################
    
    def previos_song(self):
        try:
            self.songs_index = self.get_previous_song()
            self.play_song()
        except Exception as error:
            print(error)
    #################################################################################
    #################################################################################

window = Tk()
window.geometry("500x500")
window.title("MP3 Music Player")
    #################################################################################

app = FrameApp(window)
    #################################################################################

while True:
    # runs mainloop of program
    app.check_music()
    app.update()