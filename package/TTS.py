from pydub import AudioSegment
from pydub.playback import play
from tqdm import tqdm
import json
import shutil
import os
import edge_tts
from io import BytesIO

class Loading:
    def __init__(self) -> None:
        pass

    def setting_progress_bar(self):
        total_steps = 100   
        progress_bar = tqdm(total=total_steps, dynamic_ncols=True)
        return progress_bar, total_steps

    def update_progress_bar(self, total_steps, progress_bar, percentage):
        steps_to_add = (total_steps * percentage) / 100
        if progress_bar.n + steps_to_add > total_steps:
            steps_to_add = total_steps - progress_bar.n
        progress_bar.update(steps_to_add)

class TextToSpeech:
    def __init__(self) -> None:
        self.VOICE = "ko-KR-HyunsuNeural"
        self.Loading = Loading()
        if self.VOICE == "ko-KR-HyunsuNeural":
            self.CHUNK_REMOVE = -1000
        elif self.VOICE == "ko-KR-InJoonNeural":
            self.CHUNK_REMOVE = -1000
        elif self.VOICE == "ko-KR-SunHiNeural":
            self.CHUNK_REMOVE = -500
    
    """
    --------------------
    Name: Microsoft Server Speech Text to Speech Voice (ko-KR, HyunsuNeural)
    ShortName: ko-KR-HyunsuNeural
    Gender: Male
    Locale: ko-KR
    Chunck Removmental Time: [:-500]
    --------------------
    Name: Microsoft Server Speech Text to Speech Voice (ko-KR, InJoonNeural)
    ShortName: ko-KR-InJoonNeural [:-1000]
    Gender: Male
    Locale: ko-KR
    --------------------
    Name: Microsoft Server Speech Text to Speech Voice (ko-KR, SunHiNeural)
    ShortName: ko-KR-SunHiNeural
    Gender: Female
    Locale: ko-KR
    --------------------
    """
    
    async def downloading(self):
        folder_path = 'Siosk/assets/audio'
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
            os.mkdir(folder_path)
        else:
            os.mkdir(folder_path)
        progress_bar, total_steps = self.Loading.setting_progress_bar()
        with open('Siosk/package/conversation.json', 'r', encoding='utf-8') as file:
            target_datas = json.load(file)
            for target_data_index, target_data_val in enumerate(target_datas):
                target_data_que = str(target_data_val).split(' | ')[0]
                target_data_ans = str(target_data_val).split(' | ')[1]
                if '?' or ' ' in target_data_ans:
                    target_data_ans = target_data_ans.replace('?', ";")
                communicate = edge_tts.Communicate(target_data_ans, self.VOICE)
                await communicate.save(f"Siosk/assets/audio/{target_data_ans}.mp3")
                self.Loading.update_progress_bar(total_steps, progress_bar, 100 / len(target_datas))

    async def voice(
            self, 
            target: str, 
            resultment: str, 
            flag: bool
        ) -> None: # model.py line 70

        """Main function"""
        if flag == True: 
            print("Audio Usage")
            audio = AudioSegment.from_file(resultment, format="mp3")[:self.CHUNK_REMOVE]
            play(audio)
        elif flag == False:
            communicate = edge_tts.Communicate(target, self.VOICE)
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            try:
                await play(AudioSegment.from_file(BytesIO(audio_data), format="mp3")[:self.CHUNK_REMOVE])
            except:
                pass


