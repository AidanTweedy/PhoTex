import io
import os

from google.cloud import vision
from google.cloud.vision import types

from pathlib import Path

import PySimpleGUI as sg

import pyperclip

def setupGUI(theme):
    sg.theme(theme)

    layout = [  [sg.Text('Select file to transcribe')], 
                [sg.In(visible=False), sg.Input(key='-DIR-'), sg.FileBrowse(target='-DIR-',enable_events=True, file_types=(("JPG Files", "*.jpg"),))],
                [sg.Button('Confirm')],
                [sg.Text(''), sg.Text(size=(15,1), key='-OUTPUT-')],
                [sg.Exit()] ]
            
    myWindow = sg.Window('PhoTex', layout)

    filePath = ''

    while True:
        event, values = myWindow.read()
        filePath = values.get('Browse')
        if event == sg.WIN_CLOSED or event == 'Exit':
            exit()
            break
        if event == 'Confirm':
            myWindow['-OUTPUT-'].update('Done!')
            break
            

    myWindow.close()
    return filePath

def returnGUI(fullText, theme):
    sg.theme(theme)

    layout = [ [sg.Multiline(fullText, size=(45,5))], [sg.Button('Copy')], [sg.Exit()]]
    myWindow = sg.Window('PhoTex: Full Text', layout)

    while True:
        event, values = myWindow.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Copy':
            pyperclip.copy(fullText)
    myWindow.close()

####Format and print output to console
def print_helper(output):
    print("FULL TEXT: " + '\n' + output + '\n')

####Transcribes pictures of handwriting into text
def transcribe_hand(fileName):
    #image file path
    file_name = Path('data', fileName)

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)

    output = ''

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    if(len(word_text) == 1):
                        if (ord(word_text) >= 33 and ord(word_text)<= 47):
                            output = output[:-1]
                            output += word_text + ' '
                        else:
                            output += word_text + ' '
                    else: 
                        output += word_text + ' '


    #FULL TEXT

    print_helper(output)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    return output


if __name__ == '__main__':
    clientPath = Path('Murr_Recog-8d2925fea65c.JSON')
    client = vision.ImageAnnotatorClient.from_service_account_json(clientPath)
    filePath = setupGUI('DarkAmber')
    FULL_TXT = transcribe_hand(Path(filePath))
    returnGUI(FULL_TXT, 'DarkAmber')
