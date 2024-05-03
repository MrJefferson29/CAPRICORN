
if 1 : #Modules Import
    from dotenv import load_dotenv as env
    import numpy as np  , time
    from threading import Thread as th
    import tkinter as tk , pygame
    from keras.models import load_model 
    from tkinter import ttk
    import google.generativeai as genai , os 
    api = 'AIzaSyBMcT7V-h74b7hyk_IlzM_ZJ3oNd3uSy3Y'

if 1 :
    sky_blue = ( 30 , 30 , 60)
    red =  (  255 , 0 , 0)
    white =  ( 255 ,255 ,255)
    black = ( 0 , 0  ,0)
    blue = ( 0 , 0 , 255)
    green = ( 0 , 255 , 0)
    yellow =  ( 255 , 255 , 0)
    catoon_soil = ( 250 , 190 , 200)

pygame.init ( )
size = pygame.display.Info ( )
screen_size = [size.current_w , size.current_h ]

def center_rect ( rect ) :
    x , y , w , h = rect
    return [x + w // 2 , y + h // 2]

def top ( center , dim ) :
    cx , cy , w , h = center + dim
    return [cx - w // 2 , cy - h // 2]


class text_holder : # Store  Of Info For Easy Thread Malnupulation 
    def __init__ ( self , text : str = '' , maxlen = 50 , delay : int =  .05 , Ai = None , box_words : int = 30  ) :
        self.text , self.written , self.max  = text , '' , maxlen
        self.delay , self.Ai , self.word_count = delay , Ai , box_words
        self.done_text = 1
        self.command , self.done = '' , 1
        self.buttons = None
        self.before = self.after = ''
        self.npkt = None
        self.printed  = 0
    def configure ( self , npkt : list ) :
        self.npkt = npkt
        
class clicks  : # Button Clicks Mananger
    def __init__ ( self , butt : tk.Button , bot : text_holder = text_holder ( )  ) :
        self.butt , self.bot = butt , bot
    def click ( self ) :
        while 1:
            if self.bot.done :
                npk = self.bot.npkt
                s = sum ( npk )
                npkt = np.array ( [npk]) / s
                    
                while not self.bot.done_text : pass
                self.bot.before =f"""
For the Following NPK ( {npk[0] },{npk[1] },{npk[2] } )  , it's concluded that (Offline Mode) :
***{self.butt.name} has a { round ( self.butt.model.predict( npkt )[0][0] * 100  ) + .1 }% of doing well under such coditions.
                
For More Details ( Wait A While) : Status > Connecting to Server...
                """
                self.bot.done = self.bot.done_text = 0
                while not self.bot.done_text : pass
                self.bot.command = f'recomend a good fertilizer to my custommer\'s {self.butt.name} as though you are me  , the farm yard has an NPK  of {npk} , in less than 5000 charecters , to my customer , just go straight to the point , no explaination needed also give him some cameroonian crops that might do well in such conditions if and only if any , make sure you give him the fertilizer if any otherwise tell him  whether there\'s need or not , the npk values are in kg/ha , do not miss out any of this points .No need calling his or my name  '
                break
            else : 0

def typing ( t : text_holder , label : tk.Text  ) : #Type Writter Effect , (Generator)
    while 1 :
        delay = t.delay
        max_len = t.max
        if t.text : print ( t.text )
        text , on = list ( t.text ) , list (t.written)
        
        text = list ( text )
        t.text = ''
        t.done = 1
        if text : 
            l = len ( label.get ( '1.0' , tk.END  ))
            if l > max_len : label.delete ( '1.0' , f'{l - max_len +1 }.0')
        t.done_text = 0
        while 1 :
            if not text : break
            label.insert(f'{l + 1}.0' ,  text[0])  , label.see( tk.END)
            l += 1 
            text.pop( 0 )
            time.sleep ( delay ) 
        t.done_text = 1
        t.text = t.before +  interact ( t  , t.command ) + t.after
        t.command = ''
        t.before = t.after = ''
        if t.text : 
            t.text  +=  '\n' + '_'*t.word_count + '\n\n'
        t.command = ''
        t.written = on        

def rgb ( *color  ) :#RGB To Hex 
    return '#{:02x}{:02x}{:02x}'.format ( *color )

if 1: #Gemini (AI) Setup
    def interact ( Ai_bot : text_holder , command  ) :
        if not command : return ''
        if command  : 
            try : 
                print ( 'start')
                Ai_bot.Ai = model.start_chat( history=[] ) 
                res =  Ai_bot.Ai.send_message ( command ).text 
                print ( res )
                return res
            except Exception as e : 
                return f'***{e} .If Connection Issues Pessist , Consider Restarting ( Server Overloaded ) Or Checking Your Internet Bundle'
            
    
    genai.configure ( api_key=api )

    model = genai.GenerativeModel ( 'gemini-pro' )
    chat = model.start_chat( history=[] )
    
if 1 : #Files
    Crops = r'Capricon $'

root = tk.Tk()


sdim = np.array ( screen_size )

root.title ( 'Capricon Productions$' )
root.resizable ( False , False)



size = np.array ( [751.3 , 537.6] )

pos = [int (char ) for char in top ( center_rect ( [0 , 0] + screen_size ) , list ( size) )]
size = [int ( char ) for char in size]
bg = rgb ( 50 , 50 , 50) # in hexadecimal
bgw = rgb ( 220 , 200 , 220)
root.geometry(f'{size[0]}x{size[1]}+{pos[0]}+{pos[1]}')
root.configure ( bg= bgw )



if 1 : #NPK Manangement ( GUI )
    if 0 : 
        word_count = int ( 9 * size[0] / 100  )
        fl = tk.Label ( root , text = '-- Display Box --' , foreground=  rgb ( *green ) , font = 30 , bg = rgb ( 255 , 255 , 255 ) , width = word_count)
        fl.grid ( column = 0 , row= 0 , pady = int ( .1 * size[1] / 100)   )
    
    if 1 : #Entry label 
        style = ttk.Style ( )
        style.configure ( "RoundedFrame.TFrame" , background = 'black' , borderwidth = 10 , relief = 'solid' , borderRadius = 10 )
        frame = ttk.Frame ( root , style="RoundedFrame.TFrame" , border= 10 , relief = 'flat')
        frame.grid ( column=0, row=2 , columnspan=2  )
        fontsize = 30
        word_count = int ( 10.55 * size[0] / 100  )
        chat_box = tk.Text ( frame , width = word_count , height=20 , font=fontsize , bg=bg  , wrap='word'  )
        chat_box.grid ( column=0, row=2 , sticky = 'nsew' , columnspan=1 )
        scroll = tk.Scrollbar ( frame  , orient = 'vertical' , command=chat_box.yview , width=10  , relief='sunken' , activebackground=rgb(*green)  )
        scroll.grid( row=2 ,  column= 1 , sticky='ns'  )
        chat_box.config ( yscrollcommand=scroll.set)

if 1 : # common crops buttons 
    pre_label = tk.Label ( root , text = '--- Click On A Button To Get More Info On Crop ---' , foreground=rgb ( *green ) , font = 30 , bg = rgb ( 20 , 10 , 5) )
    pre_label.grid ( row = 3 , column= 0 , pady = int ( 2 * size[1] / 100) )
    dirs = os.listdir ( Crops )
    crops = [char.split ('.')[0].title ( ) for char in  dirs]
    dirsp = [os.path.join ( Crops , char ) for char in dirs ] #Path To Saved Models
    clic_ = [ ]
    word_count = max ( [ len ( char ) for char in crops ] ) + 1
    frame = tk.Frame ( root , bg=rgb ( 225 , 210 , 180) , border=10   )
    frame.grid ( column=0, row = 4 )
    mycrops = [ ]
    max_columns = 5
    row = col  = 0
    for i in range ( len ( crops ) ) :
        name , Model  = crops[i] , load_model ( dirsp[i] )
        butt = tk.Button ( frame  , text= name  , width=word_count , bg = rgb ( 225 , 100 , 150)  )
        _click = clicks ( butt )
        clic_.append ( _click ) , butt.configure ( command=_click.click)
        butt.name , butt.model = name , Model #Adding My Own Properties
        mycrops.append ( butt ) , butt.grid ( column= col , row=row , padx=int ( .2 * size[0] / 100) , pady = int ( .2 * size[1] / 100) )
        col += 1
        if col > max_columns :
            col = 0
            row += 1




bot = text_holder ( '' , 5000  , .005  , chat , word_count )
bot.before = ' Hi . Thanks For Using CAPRICONS@work We Are Delighted To Assist You Get Great Crop Yield !\n\n'
bot.done = bot.done_text = 0
th( target= typing , args= [ bot , chat_box ] , daemon=1).start(  )
bot.configure ( [140 , 28 , 90] )
bot.command = ''
for char in clic_ :
    char.bot  = bot 


root.mainloop( )