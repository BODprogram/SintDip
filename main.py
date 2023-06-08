import pydub
from pydub import AudioSegment
import winsound
import simpleaudio
import PySimpleGUI as sg
import random

# py -m pip install simpleaudio
DEFAULT_SOUND_1_SEC = 'Soundpacks\\Default\\T1.wav'
DEFAULT_SOUND_10_MS = 'Soundpacks\\Default\\T01.wav'
DEFAULT_TIMELESS_SOUND = 'Soundpacks\\Default\\Timeless.wav'
SOUND_MAP_GUIDE= 'Карта нот заполняется построчно, по 3 значения в строку. Первое это название ноты, такое же, как и в наборах звуков. Второе – время включения ноты, третье'
SOUND_MAP_GUIDE2='громкость. Ноты лучше располагать по порядку от начала мелодии до конца. В конце карты нот всегда идёт ключевое слово “end”, без дополнительных сопроводительных символов.'
SOUND_PACK_GUIDE= 'Для корректной работы указательный текстовый файл звукового набора должен лежать в папке Soundpacks, там-же должен лежать и одноимённая папка со звуками. Текстовый'
SOUND_PACK_GUIDE2='файл заполняется построчно, парами значений “название ноты” + “название файла ноты”. Название файла ноты указывается вместе с типом файла.'

# ------------------
CurrentSoundMap = [['note', 2.20, 100]]  # нота, время старта, громкость
CurrentSoundPack = {'do': 'notaname', 're': 'notaname'}  # пары нота: звук


def NewSilenceTrack(MS):  # длина в секундах
    sound1 = pydub.AudioSegment.from_file(DEFAULT_SOUND_1_SEC, format="wav")
    file_handle = sound1.export(DEFAULT_TIMELESS_SOUND, format="wav")
    for index in range(MS - 1):
        sound1 = pydub.AudioSegment.from_file(DEFAULT_TIMELESS_SOUND, format="wav")
        sound2 = pydub.AudioSegment.from_file(DEFAULT_SOUND_1_SEC, format="wav")
        combined = sound1 + sound2
        # simple export
        file_handle = combined.export(DEFAULT_TIMELESS_SOUND, format="wav")
    return (DEFAULT_TIMELESS_SOUND)

def AddLongSilence(name, MS):  # Требует адресное имя и добавляет нужную длину тишины.
    NewSilenceTrack(MS)
    sound1 = pydub.AudioSegment.from_file(name, format="wav")
    sound2 = pydub.AudioSegment.from_file(NewSilenceTrack(MS), format="wav")
    combined = sound1 + sound2
    # simple export
    file_handle = combined.export(name, format="wav")
    return ('done')

def AddToSoundPack(note, adress):
    global CurrentSoundPack
    CurrentSoundPack.insert(len(CurrentSoundPack), [note, adress])
    return CurrentSoundPack

def AddToSoundMap(note, time, volume):
    global CurrentSoundMap
    CurrentSoundMap.insert(len(CurrentSoundMap), [note, time, volume])
    return CurrentSoundMap

def DelToSoundMap(id):
    global CurrentSoundMap
    del (CurrentSoundMap[id])
    return CurrentSoundMap


def PlaySoundWav(filename):
    wave_object = simpleaudio.WaveObject.from_wave_file(filename)
    play_object = wave_object.play()
    play_object.wait_done()
    return ('done')


def CombineSoundWav(music1, music2, position, filename):  # starting at position into music1)
    music1 = pydub.AudioSegment.from_file(music1, format="wav")
    music2 = pydub.AudioSegment.from_file(music2, format="wav")
    output = music1.overlay(music2, position)
    output.export(filename, format="wav")
    return ('done')

def SaveSoundMap(name):
    global CurrentSoundMap
    f = open('Maps\\' + name + '.txt', 'w')
    for index in range(len(CurrentSoundMap)):
        f.write(CurrentSoundMap[index][0] + ' ' + CurrentSoundMap[index][1] + ' ' + CurrentSoundMap[index][2] + '\n')
    return ('done')

def LoadSoundMap(name):
    global CurrentSoundMap
    f = open('Maps\\' + name + '.txt', 'r')
    CurrentSoundMap.clear()
    CurrentSoundMap = []
    Fileline = ''
    while Fileline != 'end':
        Fileline = f.readline()
        if not Fileline:
            break
        if Fileline == 'end':
            break
        Fileline = Fileline.split()
        AddToSoundMap(Fileline[0], Fileline[1], Fileline[2])
    return ('done')


def LoadSoundPack(name):
    global CurrentSoundPack
    f = open('Soundpacks\\' + name + '.txt', 'r')
    CurrentSoundPack.clear()
    CurrentSoundPack = []
    while True:
        Fileline = f.readline()
        if not Fileline:
            break
        Fileline = Fileline.split()
        StringName = 'Soundpacks\\' + name + '\\' + Fileline[1]
        AddToSoundPack(Fileline[0], StringName)
    return ('done')


def CompileSoundWav(name):
    global CurrentSoundMap
    global CurrentSoundPack
    name = 'Export\\' + name + '.wav'
    MS = CurrentSoundMap[len(CurrentSoundMap) - 1][1]
    MS = float(MS)
    MS = int(round(MS))
    MS = MS + 4
    sound_ex = pydub.AudioSegment.from_file(NewSilenceTrack(MS), format="wav")
    sound_ex.export(name, format="wav")
    for index in range(len(CurrentSoundMap)):
        # FileNotFoundError: [Errno 2] No such file or directory: 'do'
        # место для проверки нот и определения нужного звука
        # print(CurrentSoundMap[index])
        Choose_note = CurrentSoundPack[0][1]
        # print(CurrentSoundMap[index][0])
        for index2 in range(len(CurrentSoundPack)):
            if CurrentSoundMap[index][0] == CurrentSoundPack[index2][0]:
                Choose_note = CurrentSoundPack[index2][1]
                # print (CurrentSoundPack[index2][0])
        CombineSoundWav(name, Choose_note, float(CurrentSoundMap[index][1]) * 1000, name)  # mix sound2 with sou
    return ('done')

# обрабатываем нажатие на кнопку

def MainMenuWindow():
    # что будет внутри окна
    # первым описываем кнопку и сразу указываем размер шрифта
    layout = [[sg.Text('Меню', key='-text-', font='Helvetica 16',background_color='#ed9a6d')],
              [sg.Button('Редактор мелодий', enable_events=True, key='-FUNCTION1-', font='Helvetica 16',button_color='#81735b')],
              [sg.Button('Редактор наборов звука', enable_events=True, key='-FUNCTION2-', font='Helvetica 16',button_color='#81735b')],
              [sg.Button('Редактор карт нот', enable_events=True, key='-FUNCTION3-', font='Helvetica 16',button_color='#81735b')],
              [sg.Button('Выход', enable_events=True, key='-FUNCTION4-', font='Helvetica 16',button_color='#81735b')] ]
    WinClose=0;
    # рисуем окно
    window = sg.Window('Музыкальный синтезатор с системой простого взаимодействия', layout, size=(800, 500), element_justification='c',background_color='#ed9a6d', icon='logo.ico')
    # запускаем основной бесконечный цикл
    while True:
        # получаем события, произошедшие в окне
        event, values = window.read()
        # если нажали на крестик
        if event in (sg.WIN_CLOSED, 'Exit'):
            WinClose = 1
            # выходим из цикла
            break
        # если нажали на кнопку
        if event == '-FUNCTION1-':
            # запускаем связанную функцию
            MelodyEditorWindow()
        if event == '-FUNCTION2-':
            # запускаем связанную функцию
            SoundPackEditorWindow()
        if event == '-FUNCTION3-':
            # запускаем связанную функцию
            SoundMapEditorWindow()
        if event == '-FUNCTION4-':
            WinClose = 1
        if (WinClose==1):
            break
    # закрываем окно и освобождаем используемые ресурсы
    window.close()
def MelodyEditorWindow():
    layout = [[sg.Text('Редактор мелодий', key='-text-', font='Helvetica 16',background_color='#ed9a6d')],
              [sg.Text('Используемая карта нот:', key='-text-', font='Helvetica 14',background_color='#ed9a6d')],
              [sg.Input('', enable_events=True, key='-INPUT1-', font=('Arial Bold', 20),  justification='left')],
              [sg.Text('Используемый набор звуков:', key='-text-', font='Helvetica 14',background_color='#ed9a6d')],
              [sg.Input('', enable_events=True, key='-INPUT2-', font=('Arial Bold', 20), justification='left')],
              [sg.Text('Название итоговой песни:', key='-text-', font='Helvetica 14',background_color='#ed9a6d')],
              [sg.Input('', enable_events=True, key='-INPUT3-', font=('Arial Bold', 20), justification='left')],
              [sg.Button('Собрать итоговую песню', enable_events=True, key='-FUNCTION1_compile_sound-', font='Helvetica 16',button_color='#81735b')],
              [sg.Button('Проиграть итоговую песню', enable_events=True, key='-FUNCTION2_play_sound-', font='Helvetica 16',button_color='#81735b')],
              [sg.Button('Выход в меню', enable_events=True, key='-FUNCTION3_to_menu-', font='Helvetica 16',button_color='#81735b')]]
    WinClose = 0;
    # рисуем окно
    window = sg.Window('Музыкальный синтезатор с системой простого взаимодействия', layout, size=(800, 500), icon='logo.ico',
                       element_justification='c',background_color='#ed9a6d')
    # запускаем основной бесконечный цикл
    while True:
        # получаем события, произошедшие в окне
        event, values = window.read()
        # если нажали на крестик
        if event in (sg.WIN_CLOSED, 'Exit'):
            WinClose = 1
            # выходим из цикла
            break
        # если нажали на кнопку

        if event == '-FUNCTION1_compile_sound-':
            try:
                LoadSoundPack(values.get('-INPUT1-'))
                LoadSoundMap(values.get('-INPUT2-'))
                CompileSoundWav(values.get('-INPUT3-'))
                print("к12")
            except:
                ErrorWindow()
        if event == '-FUNCTION2_play_sound-':
            try:
                PlaySoundWav('Export\\'+values.get('-INPUT3-')+'.wav')
            except:
                ErrorWindow()
        if event == '-FUNCTION3_to_menu-':
            WinClose = 1
        if (WinClose == 1):
            break
    # закрываем окно и освобождаем используемые ресурсы
    window.close()
def ErrorWindow():
    # что будет внутри окна
    # первым описываем кнопку и сразу указываем размер шрифта
    layout = [[sg.Text('Были введены некорректные данные.', key='-text-', font='Helvetica 16',background_color='#f44336')],
              [sg.Button('Ок', enable_events=True, key='-FUNCTION1-', font='Helvetica 16')]]
    # рисуем окно
    window = sg.Window('Предупреждение', layout, size=(450, 100),background_color='#f44336', icon='logo.ico')
    # запускаем основной бесконечный цикл
    while True:
        # получаем события, произошедшие в окне
        event, values = window.read()
        # если нажали на крестик
        if event in (sg.WIN_CLOSED, 'Exit'):
            # выходим из цикла
            break
        # если нажали на кнопку
        if event == '-FUNCTION1-':
            # запускаем связанную функцию
            break
    window.close()

def SoundPackEditorWindow():
    def PackGuideWindow():
        layout = [[sg.Text('О редактировании наборов звуков', key='-text-', font='Helvetica 16', background_color='#ed9a6d')],
                  [sg.Text(SOUND_PACK_GUIDE, key='-text-', font='Helvetica 8', background_color='#ed9a6d')],
                  [sg.Text(SOUND_PACK_GUIDE2, key='-text-', font='Helvetica 8', background_color='#ed9a6d')],
                  [sg.Button('Ок', enable_events=True, key='-FUNCTION1-', font='Helvetica 16')]]
        # рисуем окно
        window = sg.Window('Музыкальный синтезатор с системой простого взаимодействия', layout, size=(1000, 500), icon='logo.ico',
                           background_color='#ed9a6d')
        # запускаем основной бесконечный цикл
        while True:
            # получаем события, произошедшие в окне
            event, values = window.read()
            # если нажали на крестик
            if event in (sg.WIN_CLOSED, 'Exit'):
                # выходим из цикла
                break
            # если нажали на кнопку
            if event == '-FUNCTION1-':
                break
        window.close()
    WinClose = 0;
    t1 = sg.Input(visible=False, enable_events=True, key='-T1-', font=('Helvetica 16', 10), expand_x=True)
    t2 = sg.Input(visible=False, enable_events=True, key='-T2-', font=('Helvetica 16', 10), expand_x=True)
    t3 = sg.Multiline("", enable_events=True, key='-INPUT-',
                       expand_x=True, expand_y=True, justification='left')
    layout = [[sg.Text('Редактор набора звуков', key='-text-', font='Helvetica 16',background_color='#ed9a6d')],
        [t1, sg.FilesBrowse('Найти файл набора звуков',button_color='#81735b')],
              [t3],
              [t2, sg.FileSaveAs('Сохранить файл набора звуков',button_color='#81735b')],
    [sg.Button('Выход в меню', enable_events=True, key='-FUNCTION3_to_menu-', font='Helvetica 16', button_color='#81735b'),
     sg.Button('О редактировании наборов звуков', enable_events=True, key='-FUNCTION4_to_guide-', font='Helvetica 16', button_color='#81735b')
     ]
              ]
    window = sg.Window('Музыкальный синтезатор с системой простого взаимодействия', layout, size=(800, 500),background_color='#ed9a6d', icon='logo.ico')
    while True:
        event, values = window.read()
        if event == '-T1-':
            file = open(t1.get())
            txt = file.read()
            window['-INPUT-'].Update(value=txt)
        if event == '-T2-':
            file = open(t2.get(), "w")
            file.write(t3.get())
            file.close()
        if event == '-FUNCTION4_to_guide-':
            PackGuideWindow()
        if event == '-FUNCTION3_to_menu-':
            WinClose = 1
        if (WinClose == 1):
            break
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    window.close()

def SoundMapEditorWindow():
    def MapGuideWindow():
        layout = [[sg.Text('О редактировании карт нот', key='-text-', font='Helvetica 16', background_color='#ed9a6d')],
                  [sg.Text(SOUND_MAP_GUIDE, key='-text-', font='Helvetica 8', background_color='#ed9a6d')],
                  [sg.Text(SOUND_MAP_GUIDE2, key='-text-', font='Helvetica 8', background_color='#ed9a6d')],
                  [sg.Button('Ок', enable_events=True, key='-FUNCTION1-', font='Helvetica 16')]]
        # рисуем окно
        window = sg.Window('Музыкальный синтезатор с системой простого взаимодействия', layout, size=(1000, 500), icon='logo.ico',
                           background_color='#ed9a6d')
        # запускаем основной бесконечный цикл
        while True:
            # получаем события, произошедшие в окне
            event, values = window.read()
            # если нажали на крестик
            if event in (sg.WIN_CLOSED, 'Exit'):
                # выходим из цикла
                break
            # если нажали на кнопку
            if event == '-FUNCTION1-':
                break
        window.close()
    WinClose = 0;
    t1 = sg.Input(visible=False, enable_events=True, key='-T1-', font=('Helvetica 16', 10), expand_x=True)
    t2 = sg.Input(visible=False, enable_events=True, key='-T2-', font=('Helvetica 16', 10), expand_x=True)
    t3 = sg.Multiline("", enable_events=True, key='-INPUT-',
                       expand_x=True, expand_y=True, justification='left')
    layout = [[sg.Text('Редактор Карт нот', key='-text-', font='Helvetica 16',background_color='#ed9a6d')],
        [t1, sg.FilesBrowse('Найти файл карт нот',button_color='#81735b')],
              [t3],
              [t2, sg.FileSaveAs('Сохранить файл карт нот',button_color='#81735b')],
    [sg.Button('Выход в меню', enable_events=True, key='-FUNCTION3_to_menu-', font='Helvetica 16', button_color='#81735b'),
     sg.Button('О редактировании карт нот', enable_events=True, key='-FUNCTION4_to_guide-', font='Helvetica 16', button_color='#81735b')
     ]
              ]
    window = sg.Window('Музыкальный синтезатор с системой простого взаимодействия', layout, size=(800, 500),background_color='#ed9a6d', icon='logo.ico')
    while True:
        event, values = window.read()
        if event == '-T1-':
            file = open(t1.get())
            txt = file.read()
            window['-INPUT-'].Update(value=txt)
        if event == '-T2-':
            file = open(t2.get(), "w")
            file.write(t3.get())
            file.close()
        if event == '-FUNCTION4_to_guide-':
            MapGuideWindow()
        if event == '-FUNCTION3_to_menu-':
            WinClose = 1
        if (WinClose == 1):
            break
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    window.close()

# PlaySoundWav("mixed_sounds.wav")

# AudioSegment.converter = "C:\\ProgramData\\Anaconda3\\Lib\\ffmpeg\\bin\\ffmpeg.exe"
##    AudioSegment.from_wav("mixed_sounds.wav").export("mixed_sounds.mp3", format="mp3")
#TestWindow()
MainMenuWindow()
print("конец")
''' name = '11'
LoadSoundMap(name)
SaveSoundMap('12')
LoadSoundPack('Piano4')
CompileSoundWav('PianoTest1')
# PlaySoundWav('Export\\PianoTest1.wav')

LoadSoundMap('imperial_marsh')
CompileSoundWav('imperial_marsh_test')
PlaySoundWav('Export\\imperial_marsh_test.wav') '''
