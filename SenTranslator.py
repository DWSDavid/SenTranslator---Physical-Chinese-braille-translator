#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SenTranslator - World's First Chinese Braille Translator
========================================================

This is the main control software for SenTranslator, a Raspberry Pi-based
Chinese Braille translator that converts Chinese text into tactile Braille
output using linear servo motors.

Hardware Requirements:
- Raspberry Pi 4B (4GB RAM recommended)
- 12x Linear servo motors for Braille display
- 3x Push buttons for user interaction
- Audio output (speakers/headphones)
- Optional: USB microphone for voice input

Author: SenTranslator Project
License: MIT License
Version: 1.0.0
"""

import RPi.GPIO as GPIO
import time
import os
import re
from gpiozero import Button
from pypinyin import pinyin, Style
from aip import AipSpeech
import requests
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image
import subprocess


# Global variable for audio process control
audio_process = None

# Initialize GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Hardware Configuration - Two groups of servo motors
SERVO_PINS_GROUP1 = [17, 22, 24, 12, 6, 25]  # First group (left Braille cell)
SERVO_PINS_GROUP2 = [16, 19, 26, 13, 20, 21]  # Second group (right Braille cell)

# Button pin configuration
BUTTON_PINS = {
    'next': 4,    # Navigate to next Braille unit
    'audio': 27,  # Play fixed audio file
    'tts': 5      # Play text-to-speech
}

# Baidu Speech API Configuration (Replace with your own API credentials)
# Sign up at https://ai.baidu.com/ to get your API keys
BAIDU_APP_ID = 'YOUR_APP_ID'
BAIDU_API_KEY = 'YOUR_API_KEY'
BAIDU_SECRET_KEY = 'YOUR_SECRET_KEY'

# Fixed audio file path (replace with your audio file)
FIXED_AUDIO_PATH = "/home/pi/demo_audio.m4a"

# Chinese Braille Initial Consonant Mapping
# Each number represents a Braille dot position (1-6)
initial_map = {
    "b": [1, 2],
    "m": [1, 3, 4],
    "d": [1, 4, 5],
    "n": [1, 3, 4, 5],
    "g": [1, 2, 4, 5],
    "h": [1, 2, 5],
    "x": [1, 2, 5],     # Same as 'h' in some contexts
    "j": [1, 2, 5],     # Transformed from 'g' before i/u/ü
    "ch": [1, 2, 3, 4, 5],
    "r": [2, 4, 5],
    "c": [1, 4],
    "p": [1, 2, 3, 4],
    "f": [1, 2, 4],
    "t": [2, 3, 4, 5],
    "l": [1, 2, 3],
    "k": [1, 3],
    "q": [1, 3],        # Same as 'k' in some contexts
    "zh": [3, 4],
    "sh": [1, 5, 6],
    "z": [1, 3, 5, 6],
    "s": [2, 3, 4],
    "y": [3, 4, 5, 6],
    "w": [2, 3, 5, 6]
}

# Chinese Braille Final Vowel Mapping
final_map = {
    # Basic vowels
    "a": [3, 5],
    "i": [2, 4],
    "ü": [3, 4, 6],
    "v": [3, 4, 6],     # Alternative representation for ü
    "ai": [2, 4, 6],
    "ei": [2, 3, 4, 6],
    "ia": [1, 2, 4, 6],
    "ie": [1, 5],
    "e": [2, 6],
    "u": [1, 3, 6],
    "er": [1, 2, 3, 5],
    "ao": [2, 3, 5],
    "ou": [1, 2, 3, 5, 6],
    "iao": [3, 4, 5],
    "iu": [1, 2, 5, 6],
    
    # Extended vowel combinations
    "o": [1, 3, 5],
    "ui": [2, 4, 5, 6],
    "an": [1, 2, 3, 6],
    "en": [3, 5, 6],
    "in": [1, 2, 6],
    "un": [4, 5, 6],
    "ün": [4, 5, 6],
    "vn": [4, 5, 6],
    "ang": [2, 3, 6],
    "eng": [3, 4, 5, 6],
    "ing": [1, 6],
    "ong": [2, 5, 6],
    "ua": [1, 2, 3, 4, 5, 6],
    "uo": [1, 3, 5],
    "uai": [1, 3, 4, 5, 6],
    "uei": [2, 4, 5, 6],
    "uan": [1, 2, 4, 5, 6],
    "uen": [2, 5],
    "uang": [2, 3, 5, 6],
    "ueng": [2, 5, 6],
    "ian": [1, 4, 6],
    "iang": [1, 3, 4, 6],
    "iong": [1, 4, 5, 6],
    "üan": [1, 2, 3, 4, 6],
    "van": [1, 2, 3, 4, 6],
    "üe": [2, 3, 4, 5, 6],
    "ve": [2, 3, 4, 5, 6],
    "ue": [2, 3, 4, 5, 6]
}

# Punctuation mark mapping
punctuation_map = {
    "。": {"dots": [2, 5, 6]},      # Period
    "，": {"dots": [2]},            # Comma
    "？": {"dots": [2, 3, 6]},      # Question mark
    "！": {"dots": [2, 3, 5]},      # Exclamation mark
    "：": {"dots": [2, 5]},         # Colon
    "；": {"dots": [2, 3]},         # Semicolon
    """: {"dots": [2, 3, 6]},       # Opening quotation mark
    """: {"dots": [2, 3, 5, 6]},    # Closing quotation mark
    "（": {"dots": [2, 3, 5, 6]},   # Opening parenthesis
    "）": {"dots": [2, 3, 5, 6]},   # Closing parenthesis
    "——": {"dots": None},           # Em dash (no dots)
    "……": {"dots": None},           # Ellipsis (no dots)
    "、": {"dots": [3, 4]}          # Chinese comma
}

# Number system mapping
number_prefix = {"dots": [3, 4, 5, 6]}  # Number indicator prefix
number_map = {
    "0": [2, 4, 5],
    "1": [1],
    "2": [1, 2],
    "3": [1, 4],
    "4": [1, 4, 5],
    "5": [1, 5],
    "6": [1, 2, 4],
    "7": [1, 2, 4, 5],
    "8": [1, 2, 5],
    "9": [2, 4]
}

# English alphabet mapping (Grade 1 Braille)
english_map = {
    "a": [1],
    "b": [1, 2],
    "c": [1, 4],
    "d": [1, 4, 5],
    "e": [1, 5],
    "f": [1, 2, 4],
    "g": [1, 2, 4, 5],
    "h": [1, 2, 5],
    "i": [2, 4],
    "j": [2, 4, 5],
    "k": [1, 3],
    "l": [1, 2, 3],
    "m": [1, 3, 4],
    "n": [1, 3, 4, 5],
    "o": [1, 3, 5],
    "p": [1, 2, 3, 4],
    "q": [1, 2, 3, 4, 5],
    "r": [1, 2, 3, 5],
    "s": [2, 3, 4],
    "t": [2, 3, 4, 5],
    "u": [1, 3, 6],
    "v": [1, 2, 3, 6],
    "w": [2, 4, 5, 6],
    "x": [1, 3, 4, 6],
    "y": [1, 3, 4, 5, 6],
    "z": [1, 3, 5, 6]
}

# Servo Motor PWM Configuration
# NOTE: Each servo motor may require different PWM values for extend/retract positions
# You may need to adjust these values based on your specific servo motors
# Format: GPIO_PIN: (extend_pwm, retract_pwm)
SERVO_PWM_CONFIG = {
    17: (3, 10),    # Adjust these values for your servo
    22: (3, 12),    # Adjust these values for your servo
    24: (3, 10),    # Adjust these values for your servo
    12: (3, 12),    # May require special values
    6: (3, 12),     # Adjust these values for your servo
    25: (3, 10),    # Adjust these values for your servo
    13: (3, 10),    # Adjust these values for your servo
    19: (3, 10),    # Adjust these values for your servo
    26: (4, 11),    # Adjust these values for your servo
    16: (3, 10),    # Adjust these values for your servo
    20: (3, 10),    # Adjust these values for your servo
    21: (3, 10),    # Adjust these values for your servo
}

# Servo Response Time Configuration
# Some servos may be slower and need more time to reach position
SERVO_RESPONSE_TIME = {
    6: 1.5,     # GPIO 6 needs 1.5 seconds response time
    12: 1.5,    # GPIO 12 needs 1.5 seconds response time
    # Other GPIOs use default 0.5 seconds
}


class LinearServo:
    """
    Enhanced linear servo motor control class
    
    This class manages individual linear servo motors used for Braille dot display.
    Each servo can extend (dot raised) or retract (dot lowered).
    """
    
    def __init__(self, pin):
        """
        Initialize a linear servo motor
        
        Args:
            pin (int): GPIO pin number for the servo
        """
        self.pin = pin
        self.current_state = 0  # Track current state: 0=retracted, 1=extended
        
        # Get servo-specific PWM configuration
        self.pwm_extend, self.pwm_retract = SERVO_PWM_CONFIG.get(pin, (3, 10))
        
        # Get servo-specific response time
        self.response_time = SERVO_RESPONSE_TIME.get(pin, 0.7)
        
        # Initialize GPIO and PWM
        GPIO.setup(pin, GPIO.OUT)
        self.servo = GPIO.PWM(pin, 50)  # 50Hz frequency for servo control
        
        # Initialize to retracted position
        self.servo.start(self.pwm_retract)
        time.sleep(self.response_time)
        self.servo.ChangeDutyCycle(0)  # Stop PWM signal but maintain position

    def set_state(self, state, force=False):
        """
        Set servo motor state
        
        Args:
            state (int): Target state (0=retract, 1=extend)
            force (bool): Force execution even if already in target state
        """
        # Skip if already in target state and not forcing
        if self.current_state == state and not force:
            return
        
        # Use initialized PWM values
        duty = self.pwm_extend if state == 1 else self.pwm_retract
        
        # Special handling for slower servos
        if self.pin in [6, 12]:
            # Send PWM signal
            self.servo.ChangeDutyCycle(duty)
            # Use longer wait time for slower servos
            time.sleep(self.response_time)
            # Optional: Send signal again to ensure position
            self.servo.ChangeDutyCycle(duty)
            time.sleep(0.4)
        else:
            # Normal handling for other servos
            self.servo.ChangeDutyCycle(duty)
            time.sleep(self.response_time)
        
        # Maintain position (stop PWM signal)
        self.servo.ChangeDutyCycle(0)
        self.current_state = state

    def get_state(self):
        """Get current servo state"""
        return self.current_state

    def stop(self):
        """Stop PWM signal and cleanup"""
        self.servo.ChangeDutyCycle(0)
        self.servo.stop()


def initialize_servos():
    """
    Initialize both groups of servo motors
    
    Returns:
        tuple: (group1_servos, group2_servos) - Lists of LinearServo objects
    """
    print("Initializing servo system...")
    group1 = [LinearServo(pin) for pin in SERVO_PINS_GROUP1]
    group2 = [LinearServo(pin) for pin in SERVO_PINS_GROUP2]
    
    # Test each servo individually to avoid excessive current draw
    print("Testing first servo group...")
    for i, servo in enumerate(group1):
        servo.set_state(1, force=True)  # Extend
        time.sleep(0.1)
        servo.set_state(0, force=True)  # Retract
        time.sleep(0.1)
    
    print("Testing second servo group...")
    for i, servo in enumerate(group2):
        servo.set_state(1, force=True)  # Extend
        time.sleep(0.1)
        servo.set_state(0, force=True)  # Retract
        time.sleep(0.1)
    
    print("Servo initialization complete")
    return group1, group2


def batch_control_servos(servos, states, batch_size=2):
    """
    Control servos in batches to avoid excessive current draw
    
    Args:
        servos (list): List of LinearServo objects
        states (list): Target states corresponding to each servo
        batch_size (int): Number of servos to control simultaneously
    """
    for i in range(0, len(servos), batch_size):
        batch_servos = servos[i:i+batch_size]
        batch_states = states[i:i+batch_size]
        
        # Check if this batch contains slow servos
        has_slow_servo = any(servo.pin in [6, 12] for servo in batch_servos)
        
        # Control this batch simultaneously
        for servo, state in zip(batch_servos, batch_states):
            servo.set_state(state)
        
        # Extra wait time if batch contains slow servos
        if has_slow_servo:
            time.sleep(0.3)
        
        # Delay between batches
        if i + batch_size < len(servos):
            time.sleep(0.2)


def display_braille_optimized(servos, dots, previous_dots=None):
    """
    Optimized Braille display function - only changes dots that need changing
    
    Args:
        servos (list): List of LinearServo objects
        dots (list): List of dot positions to display (1-6)
        previous_dots (list): Previous dot positions (for optimization)
    
    Returns:
        list: Current dot positions (for next call optimization)
    """
    # Determine target state for each servo
    target_states = [0] * 6  # Default all retracted
    for dot in dots:
        if 1 <= dot <= 6:
            target_states[dot-1] = 1  # Set to extended
    
    # Control servos in batches
    batch_control_servos(servos, target_states, batch_size=2)
    
    return dots


def display_dual_braille_optimized(servos_group1, servos_group2, 
                                  dots1, dots2, 
                                  char_info1=None, char_info2=None):
    """
    Optimized dual-group Braille display with character information
    
    Args:
        servos_group1 (list): First group of servos (left cell)
        servos_group2 (list): Second group of servos (right cell)
        dots1 (list): Dots for first cell
        dots2 (list): Dots for second cell
        char_info1 (str): Character information for first cell
        char_info2 (str): Character information for second cell
    """
    # Print detailed information
    print(f"\nDisplaying Braille:")
    if char_info1:
        print(f"  Left cell - {char_info1}: {dots1}")
    else:
        print(f"  Left cell: {dots1}")
    
    if dots2 and char_info2:
        print(f"  Right cell - {char_info2}: {dots2}")
    elif dots2:
        print(f"  Right cell: {dots2}")
    else:
        print(f"  Right cell: Empty")
    
    # Process both groups separately
    display_braille_optimized(servos_group1, dots1)
    
    if dots2 is not None:
        # Short delay before processing second group
        time.sleep(0.1)
        display_braille_optimized(servos_group2, dots2)


def reset_all_servos_batch(servos_group1, servos_group2):
    """
    Reset all servos to retracted position in batches
    
    Args:
        servos_group1 (list): First group of servos
        servos_group2 (list): Second group of servos
    """
    print("\nResetting all servos in batches...")
    all_servos = servos_group1 + servos_group2
    all_states = [0] * len(all_servos)  # All retracted
    
    # Reset in batches of 2
    batch_control_servos(all_servos, all_states, batch_size=2)
    print("All servos reset")


def text_to_speech(text):
    """
    Convert text to speech using Baidu TTS API
    
    Args:
        text (str): Text to convert to speech
    """
    try:
        client = AipSpeech(BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY)
        result = client.synthesis(text, 'zh', 1, {
            'vol': 5, 'spd': 5, 'pit': 5, 'per': 4
        })

        if not isinstance(result, dict):
            with open('/tmp/tts_temp.wav', 'wb') as f:
                f.write(result)
            os.system('mplayer /tmp/tts_temp.wav >/dev/null 2>&1')
            print("TTS playback completed")
        else:
            print("TTS error:", result)
    except Exception as e:
        print("TTS failed:", str(e))


def play_fixed_audio():
    """
    Play fixed audio file (can be interrupted)
    """
    global audio_process
    
    if audio_process and audio_process.poll() is None:
        # If already playing, stop it
        audio_process.terminate()
        audio_process = None
        print("Audio stopped")
        return
    
    if os.path.exists(FIXED_AUDIO_PATH):
        try:
            audio_process = subprocess.Popen(
                ['mplayer', FIXED_AUDIO_PATH],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("Fixed audio playback started")
        except Exception as e:
            print(f"Failed to play fixed audio: {str(e)}")
    else:
        print(f"Error: Fixed audio file not found at {FIXED_AUDIO_PATH}")


def split_pinyin(py):
    """
    Split pinyin into initial consonant and final vowel with special rules
    
    Args:
        py (str): Pinyin string
    
    Returns:
        tuple: (initial, final) - Initial consonant and final vowel
    """
    if not py:
        return None, py
    
    # Sort initials by length (longest first) to match correctly
    initials_list = sorted(initial_map.keys(), key=lambda x: -len(x))
    
    # Match longest initial first (zh, ch, sh)
    for ini in initials_list:
        if py.startswith(ini):
            initial = ini
            final = py[len(ini):]
            
            # Apply special pronunciation rules
            # 1. g/k/h change to j/q/x before i/u/ü
            if initial == 'g' and final and final[0] in ['i', 'u', 'ü', 'v']:
                initial = 'j'
            elif initial == 'k' and final and final[0] in ['i', 'u', 'ü', 'v']:
                initial = 'q'
            elif initial == 'h' and final and final[0] in ['i', 'u', 'ü', 'v']:
                initial = 'x'
            
            # 2. Standalone 'i' is omitted after z/c/s/zh/ch/sh/r
            if initial in ['z', 'c', 's', 'zh', 'ch', 'sh', 'r']:
                if final == 'i':
                    final = ''  # Omit standalone i
            
            return initial, final
    
    # No initial consonant found
    return None, py


def convert_chinese_char_to_braille_units(char):
    """
    Convert a single Chinese character to Braille unit sequence
    
    Args:
        char (str): Single character to convert
    
    Returns:
        tuple: (char_type, braille_units, descriptions)
    """
    # Handle punctuation marks
    if char in punctuation_map:
        units = [punctuation_map[char]["dots"]] if punctuation_map[char]["dots"] else []
        return ('punctuation', units, [char])

    # Handle digits
    if char.isdigit():
        units = []
        descs = []
        units.append(number_prefix["dots"])  # Number indicator
        descs.append('#')
        if char in number_map:
            units.append(number_map[char])
            descs.append(char)
        return ('number', units, descs)

    # Handle English letters
    if char.isalpha() and ord(char) < 128:
        lower_char = char.lower()
        if lower_char in english_map:
            return ('english', [english_map[lower_char]], [char])
        return ('other', [], [])

    # Handle Chinese characters
    if '\u4e00' <= char <= '\u9fa5':
        # Get pinyin using pypinyin
        py_list = pinyin(char, style=Style.NORMAL, errors=lambda x: [[x]])
        if py_list and py_list[0]:
            py = py_list[0][0].lower()
        else:
            return ('other', [], [])

        # Validate pinyin format
        if re.match(r'^[a-z]+$', py) is None:
            return ('other', [], [])

        # Split into initial and final
        initial, final = split_pinyin(py)

        # Generate Braille unit sequence and descriptions
        braille_units = []
        descs = []

        # 1. Initial consonant unit (if exists)
        if initial and initial in initial_map:
            braille_units.append(initial_map[initial])
            descs.append(f"{char}-{initial}")

        # 2. Final vowel unit (if exists)
        if final and final in final_map:
            braille_units.append(final_map[final])
            descs.append(f"{char}-{final}")

        return ('chinese', braille_units, descs)
    
    # Other characters
    return ('other', [], [])


def convert_text_to_display_sequence(text):
    """
    Convert text to display sequence with optimized display logic
    
    Args:
        text (str): Input text to convert
    
    Returns:
        tuple: (display_sequence, char_data) - Display sequence and character data
    """
    # First convert all characters to Braille units
    char_data = []
    in_number_mode = False
    
    for i, ch in enumerate(text):
        char_type, units, descs = convert_chinese_char_to_braille_units(ch)
        
        # Handle consecutive numbers (share number indicator)
        if char_type == 'number':
            if not in_number_mode:
                in_number_mode = True
                char_data.append((char_type, ch, units, descs))
            else:
                # Consecutive number, only need the digit itself
                if len(units) > 1:
                    char_data.append((char_type, ch, [units[1]], [descs[1]]))
                else:
                    char_data.append((char_type, ch, [], []))
        else:
            in_number_mode = False
            char_data.append((char_type, ch, units, descs))
    
    # Generate display sequence
    display_sequence = []
    i = 0
    
    while i < len(char_data):
        char_type, char, units, descs = char_data[i]
        
        if char_type == 'chinese':
            # Chinese characters: initial on first group, final on second group
            if len(units) >= 2:
                display_sequence.append((units[0], units[1], descs[0], descs[1]))
            elif len(units) == 1:
                display_sequence.append((units[0], None, descs[0], None))
            i += 1
            
        elif char_type in ['english', 'number']:
            # English and numbers: check if can be paired for display
            if i + 1 < len(char_data):
                next_type, next_char, next_units, next_descs = char_data[i + 1]
                
                # If next is also English or number, can pair them
                if next_type in ['english', 'number'] and len(units) > 0 and len(next_units) > 0:
                    # Display two characters together
                    display_sequence.append((
                        units[0], next_units[0], 
                        descs[0] if descs else char, 
                        next_descs[0] if next_descs else next_char
                    ))
                    i += 2
                else:
                    # Display alone
                    if len(units) > 0:
                        display_sequence.append((
                            units[0], None, 
                            descs[0] if descs else char, 
                            None
                        ))
                    i += 1
            else:
                # Last character, display alone
                if len(units) > 0:
                    display_sequence.append((
                        units[0], None, 
                        descs[0] if descs else char, 
                        None
                    ))
                i += 1
                
        else:
            # Other types, display individually
            for j, unit in enumerate(units):
                display_sequence.append((
                    unit, None, 
                    descs[j] if j < len(descs) else char, 
                    None
                ))
            i += 1
    
    return display_sequence, char_data


def extract_text_from_url(url):
    """
    Extract text content from a webpage
    
    Args:
        url (str): URL to extract text from
    
    Returns:
        str: Extracted text (limited to 300 characters)
    """
    try:
        response = requests.get(url, timeout=10)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style tags
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract text
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:300]  # Limit length
    except Exception as e:
        return f"Extraction failed: {str(e)}"


def extract_text_from_file(filepath):
    """
    Extract text from a file
    
    Args:
        filepath (str): Path to the file
    
    Returns:
        str: Extracted text (limited to 300 characters)
    """
    try:
        if filepath.endswith('.txt'):
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()[:300]
        else:
            return "Currently only supports .txt files"
    except Exception as e:
        return f"File read failed: {str(e)}"


def ocr_from_image(image_path):
    """
    Extract text from an image using OCR
    
    Args:
        image_path (str): Path to the image file
    
    Returns:
        str: Extracted text (limited to 300 characters)
    """
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        return text.strip()[:300]
    except Exception as e:
        return f"OCR failed: {str(e)}"


def voice_prompt(text):
    """
    Provide voice prompt to user
    
    Args:
        text (str): Text to speak
    """
    text_to_speech(text)
    time.sleep(0.5)


def get_input_method(buttons):
    """
    Let user select input method via button presses
    
    Args:
        buttons (dict): Dictionary of Button objects
    
    Returns:
        str: Selected input method ('keyboard', 'web', or 'ocr')
    """
    voice_prompt("Welcome to SenTranslator. Please select input method. Button 1 for keyboard input, Button 2 for web extraction, Button 3 for image recognition")
    
    while True:
        if buttons['next'].is_pressed:
            voice_prompt("You selected keyboard input")
            buttons['next'].wait_for_release()
            return 'keyboard'
        elif buttons['audio'].is_pressed:
            voice_prompt("You selected web extraction")
            buttons['audio'].wait_for_release()
            return 'web'
        elif buttons['tts'].is_pressed:
            voice_prompt("You selected image recognition")
            buttons['tts'].wait_for_release()
            return 'ocr'
        time.sleep(0.1)


def get_input_text(input_method):
    """
    Get input text based on selected method
    
    Args:
        input_method (str): Selected input method
    
    Returns:
        str: Input text to be converted
    """
    if input_method == 'keyboard':
        voice_prompt("Please enter text in the terminal")
        return input("Please enter text to convert: ")
    
    elif input_method == 'web':
        voice_prompt("Please enter webpage URL in the terminal")
        url = input("Please enter webpage URL: ")
        print("Extracting text from webpage...")
        text = extract_text_from_url(url)
        print(f"Extracted text: {text[:50]}...")
        return text
    
    elif input_method == 'ocr':
        voice_prompt("Please enter image path in the terminal")
        path = input("Please enter image path: ")
        print("Recognizing text from image...")
        text = ocr_from_image(path)
        print(f"Recognized text: {text[:50]}...")
        return text


def main():
    """
    Main function - Entry point of the SenTranslator application
    
    This function initializes hardware, handles user interaction,
    and manages the main application loop.
    """
    try:
        # Initialize hardware components
        servos_group1, servos_group2 = initialize_servos()
        buttons = {name: Button(pin) for name, pin in BUTTON_PINS.items()}
        
        while True:  # Main application loop
            try:
                # Get input method selection from user
                input_method = get_input_method(buttons)
                
                # Get input text based on selected method
                text = get_input_text(input_method)
                
                # Exit condition
                if text.lower() == 'q':
                    voice_prompt("Thank you for using SenTranslator. See you next time!")
                    break
                
                # Convert text to display sequence
                display_sequence, char_data = convert_text_to_display_sequence(text)

                if not display_sequence:
                    print("Error: Unable to convert input text to Braille")
                    voice_prompt("Conversion failed, please try again")
                    continue

                voice_prompt("Conversion successful. Now press button 1 to display next Braille group, button 2 to play audio description, button 3 to read input text content")
                print(f"\nTotal {len(display_sequence)} groups to display")
                
                # Display conversion details
                print("\nDisplay plan:")
                for i, (unit1, unit2, desc1, desc2) in enumerate(display_sequence):
                    if unit2 and desc2:
                        print(f"Group {i+1}: {desc1}{unit1} + {desc2}{unit2}")
                    elif desc1:
                        print(f"Group {i+1}: {desc1}{unit1} + Empty")
                    else:
                        print(f"Group {i+1}: {unit1} + Empty")

                current_group = 0
                print("\nWaiting for button press to start display...")
                
                # Display loop - show each Braille group
                while current_group < len(display_sequence):
                    if buttons['next'].is_pressed:
                        # Display current group
                        unit1, unit2, desc1, desc2 = display_sequence[current_group]
                        print(f"\nDisplaying group {current_group + 1}/{len(display_sequence)}")
                        
                        # Use optimized display function
                        display_dual_braille_optimized(
                            servos_group1, servos_group2, 
                            unit1, unit2,
                            desc1, desc2
                        )
                        
                        # Wait for button release
                        buttons['next'].wait_for_release()
                        current_group += 1
                        
                        # Notify when all content is displayed
                        if current_group >= len(display_sequence):
                            print("\nAll content has been displayed!")
                            voice_prompt("Display complete")
                            
                    elif buttons['audio'].is_pressed:
                        play_fixed_audio()
                        buttons['audio'].wait_for_release()
                        
                    elif buttons['tts'].is_pressed:
                        text_to_speech(text)
                        buttons['tts'].wait_for_release()
                        
                    time.sleep(0.1)

                # Wait for user confirmation before reset
                print("\nDisplay complete, press any button to reset all servos...")
                while not buttons['next'].is_pressed:
                    if buttons['audio'].is_pressed:
                        play_fixed_audio()
                        buttons['audio'].wait_for_release()
                    elif buttons['tts'].is_pressed:
                        text_to_speech(text)
                        buttons['tts'].wait_for_release()
                    time.sleep(0.1)
                
                # Reset all servos in batches
                reset_all_servos_batch(servos_group1, servos_group2)
                
                # Prepare for next round
                voice_prompt("Welcome to continue using SenTranslator")
                print("\n" + "="*50 + "\n")
                
            except Exception as e:
                print(f"\nProcessing error: {str(e)}")
                voice_prompt("An error occurred, please try again")
                continue

    except KeyboardInterrupt:
        print("\n\nProgram interrupted")
        voice_prompt("Program interrupted")
    finally:
        # Cleanup resources
        if 'servos_group1' in locals() and 'servos_group2' in locals():
            print("Resetting all servos...")
            reset_all_servos_batch(servos_group1, servos_group2)
            for servo in servos_group1 + servos_group2:
                servo.stop()
        print("Resources released")


if __name__ == '__main__':
    """
    Program entry point
    
    Run this script directly to start the SenTranslator application.
    Make sure all hardware connections are properly set up before running.
    
    Usage:
        python3 sentranslator_main.py
    
    Hardware Setup:
        1. Connect 12 linear servo motors to specified GPIO pins
        2. Connect 3 push buttons to specified GPIO pins
        3. Connect audio output (speakers/headphones)
        4. Ensure stable 5V power supply for servos
        
    Dependencies:
        - RPi.GPIO: Raspberry Pi GPIO control
        - gpiozero: Simplified GPIO interface
        - pypinyin: Chinese pinyin conversion
        - aip: Baidu AI Platform SDK (for TTS)
        - requests, beautifulsoup4: Web scraping
        - pytesseract, Pillow: OCR functionality
    """
    main()