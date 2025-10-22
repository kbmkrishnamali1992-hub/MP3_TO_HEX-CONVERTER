
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
/*
  🎵 ESP32 PWM Audio Player
  -----------------------------------
  Developed by: KRISHNA B MALI

  ▶ DESCRIPTION:
  This sketch plays back 8-bit mono audio on an ESP32 using the PWM output.
  It reads audio data from a "sound.h" file generated from an MP3 file.

  -----------------------------------
  🧩 HOW TO CREATE "sound.h" FILE:
  1. Use the "MP3 → HEX Header Converter" tool developed earlier (Python GUI).
     - Input:  your .MP3 file
     - Output: "sound.h" containing 8-bit unsigned PCM array (8 kHz sample rate)

  2. The tool automatically converts your MP3 to:
       → HEX format (8-bit, 8kHz, mono)
       → sound.h file with:
          const uint8_t sound_audio[] PROGMEM = { ... };
          const unsigned int sound_audio_len = XXXX;

  3. Copy the generated "sound.h" file into the same folder as this sketch:
       📁 <Arduino_Sketch_Folder>
          ├── ESP32_PWM_Audio_Player.ino
          └── sound.h

  4. Then upload this sketch to your ESP32 board.

  -----------------------------------
  🧠 NOTES:
  • GPIO25 (default) is used for PWM audio output.
  • Connect GPIO25 → small speaker via an RC low-pass filter (1kΩ + 0.1µF).
  • Use SAMPLE_RATE = 8000 (matches converter output).
  • Audio automatically loops (you can disable in ISR).
*/

#include "sound.h"  // Include generated sound.h file with audio data

// PWM Configuration
const int AUDIO_PIN = 25;        // GPIO25 (use GPIO26 for stereo channel 2)
const int PWM_RESOLUTION = 8;    // 8-bit resolution (0-255)
const int PWM_FREQ = 78125;      // PWM frequency (~78 kHz for 8-bit)

// Audio playback variables
const int SAMPLE_RATE = 8000;   // Must match your .wav/.mp3 conversion rate
volatile uint32_t audioIndex = 0;
hw_timer_t *timer = NULL;

// Timer ISR to output audio samples
void IRAM_ATTR onTimer() {
  if (audioIndex < sizeof(sound_audio)) {
    ledcWrite(AUDIO_PIN, sound_audio[audioIndex]);
    audioIndex++;
  } else {
    audioIndex = 0;  // Loop audio (remove to play once)
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("🎧 ESP32 PWM Audio Player Starting...");
  
  // Configure LEDC PWM - NEW API for Core 3.x
  ledcAttach(AUDIO_PIN, PWM_FREQ, PWM_RESOLUTION);
  
  // Configure timer for sample rate timing - NEW API for Core 3.x
  timer = timerBegin(SAMPLE_RATE);  // Frequency in Hz
  timerAttachInterrupt(timer, &onTimer);
  timerAlarm(timer, 1, true, 0);  // Interrupt every tick, auto-reload, unlimited count
  
  Serial.println("✅ Audio playback started!");
}

void loop() {
  // Main loop is free for other tasks
  delay(100);
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
