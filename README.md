
# 🎵 MP3 → HEX Header Converter


A **Python GUI tool** to convert MP3 files into **8-bit PCM RAW audio** and generate a **C/C++ header file (.h)** with HEX array, ready for microcontroller projects like **Arduino** and **ESP32**.  

Includes **portable FFmpeg** and a Windows executable for easy use.

---

## ⚡ Features

- Convert MP3 → 8-bit PCM RAW audio (`.raw`)  
- Generate `.h` header file with HEX array (`PROGMEM` compatible)  
- Optional destination folder for outputs  
- Progress bar to monitor conversion  
- Open destination folder directly from the app  
- Portable: FFmpeg included  
- GUI built with **Tkinter**, user-friendly  

---

## 📥 Download Executable

[**Download MP3 → HEX Converter (Windows EXE)**](https://www.dropbox.com/scl/fi/bs5c3ucgepbh49r1aujnr/MP3_TO_HEX_V2.exe?rlkey=1tj3ru51kmptojo0gehau3a90&st=kr03bip0&dl=0)

---

## 🛠 Installation

### Option 1: Using the Executable
1. Download the `.exe` file from above.  
2. Run it directly (no Python required).  

### Option 2: Running from Python Source
1. Clone this repository:

```bash
git clone https://github.com/kbmkrishnamali1992/mp3-to-hex-converter.git
cd mp3-to-hex-converter
````

2. Ensure `ffmpeg/bin/ffmpeg.exe` exists (bundled portable FFmpeg).
3. Run the Python script:

```bash
python main.py
```

---

## 📝 How Conversion Works (FFmpeg Command)

The program uses FFmpeg to convert MP3 files into raw 8-bit PCM audio:

```bash
ffmpeg -i input.mp3 -f u8 -ar 8000 -ac 1 -acodec pcm_u8 output.raw -y
```

**Explanation:**

* `-i input.mp3` → Input MP3 file
* `-f u8` → Output as unsigned 8-bit PCM
* `-ar 8000` → Sample rate 8 kHz
* `-ac 1` → Mono channel
* `-acodec pcm_u8` → 8-bit PCM codec
* `-y` → Overwrite existing file

The raw file is then converted into a `.h` header file:

```cpp
const uint8_t sound_audio[] PROGMEM = {
  0x00, 0x12, 0x34, ...
};
const unsigned int sound_audio_len = 12345;
```

---

## 📝 Usage

1. **Select MP3 File** – Browse and select an MP3 file.
2. **Select Destination Folder (Optional)** – Choose output folder; defaults to script folder.
3. **Start Conversion** – Click **▶ Start Conversion**.
4. **Open Destination Folder** – Access your `.raw` and `.h` files.
5. **Close** – Exit the program with **✖ Close**.

---

## ⚡ Example: Playing Sound on ESP32 (Arduino)

```cpp
#include <Arduino.h>
#include "sound.h"

const int DAC_PIN = 25; // DAC output pin (GPIO25 or GPIO26)

void setup() {
  dacWrite(DAC_PIN, 0); // Initialize DAC
}

void loop() {
  for (unsigned int i = 0; i < sound_audio_len; i++) {
    dacWrite(DAC_PIN, sound_audio[i]); // Play audio sample
    delayMicroseconds(125); // 8 kHz playback rate
  }
  delay(1000); // Wait 1 sec before replay
}
```

**Notes:**

* Connect speaker or amplifier to DAC pin.
* Adjust `delayMicroseconds(125)` for correct playback speed (8 kHz in this case).
* Works for any audio converted using the FFmpeg settings above.

---

## ⚠️ Notes

* Works on **Windows** (uses `os.startfile` to open folders).
* `.h` file uses `PROGMEM` for Arduino/ESP32 compatibility.
* Ensure FFmpeg exists in `ffmpeg/bin/ffmpeg.exe` if running Python version.

---

## 📝 License

MIT License – Free to use, modify, and distribute.

---

## 👤 Author

**Krishna B Mali**

* GitHub: https://github.com/kbmkrishnamali1992-hub
