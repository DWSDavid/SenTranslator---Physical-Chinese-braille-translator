# SenTranslator Troubleshooting Guide

> **Quick solutions to common issues with SenTranslator hardware and software**

---

## 🚨 Emergency Quick Fixes

### **Device Won't Start**
1. Check 5V external power supply connection
2. Verify Raspberry Pi boot (green LED should blink)
3. Ensure MicroSD card is properly inserted
4. Try different power cable

### **No Braille Output**
1. Run hardware test: `python3 tests/hardware_test.py`
2. Check servo power connections
3. Verify GPIO pin connections
4. Test individual servos: `python3 tests/servo_test.py`

### **No Audio Output**
1. Check speaker/headphone connections
2. Test system audio: `speaker-test -c2`
3. Run audio test: `python3 tests/audio_test.py`
4. Verify volume settings: `alsamixer`

---

## ⚡ Power & Electrical Issues

### **🔋 Power Supply Problems**

#### ❌ **Symptom**: Servos not moving or erratic behavior
**✅ Solutions**:
```bash
# Check power supply specifications
- Voltage: Exactly 5V DC
- Current: Minimum 3A (recommended 5A)
- Connection: Stable, no loose wires

# Verify connections
External 5V+ → Breadboard + Rail
External GND → Breadboard - Rail
Pi GND → Breadboard - Rail (CRITICAL!)
```

#### ❌ **Symptom**: Raspberry Pi reboots randomly
**✅ Solutions**:
- **NEVER** connect servos to Pi's 5V pin
- Use separate power supply for servos
- Check for power supply voltage drops
- Ensure adequate power supply current rating

#### ❌ **Symptom**: Only some servos work
**✅ Solutions**:
- Check breadboard connections
- Verify power distribution to all servos
- Test power supply under load
- Look for loose jumper wires

---

## 🔧 Hardware Issues

### **🎛️ Servo Motor Problems**

#### ❌ **Symptom**: Servo doesn't move to correct position
**✅ Solutions**:
```python
# Calibrate PWM values using servo test
python3 tests/servo_test.py

# Common PWM ranges to try:
Extend: 2.5 - 4.0
Retract: 9.0 - 12.0

# Adjust in SERVO_PWM_CONFIG:
SERVO_PWM_CONFIG = {
    17: (3.2, 10.5),  # Your calibrated values
    22: (2.8, 11.2),  # Adjust per servo
    # ...
}
```

#### ❌ **Symptom**: Servo moves but returns to wrong position
**✅ Solutions**:
- Increase response time in `SERVO_RESPONSE_TIME`
- Check for mechanical binding
- Verify servo mounting is secure
- Test with longer PWM signal duration

#### ❌ **Symptom**: Servo jitters or vibrates
**✅ Solutions**:
- Reduce PWM signal noise with capacitors
- Check power supply stability
- Ensure proper grounding
- Use shielded cables for long connections

### **🔘 Button Input Problems**

#### ❌ **Symptom**: Buttons not responding
**✅ Solutions**:
```bash
# Test button connections
python3 tests/hardware_test.py

# Check wiring:
Button → GPIO Pin
Button → Ground (with pull-up resistor)

# Verify in code:
BUTTON_PINS = {
    'next': 4,    # Check this pin number
    'audio': 27,
    'tts': 5
}
```

#### ❌ **Symptom**: Button presses register multiple times
**✅ Solutions**:
- Add hardware debouncing (100nF capacitor)
- Increase software debounce time
- Check for loose connections
- Use quality tactile switches

---

## 💻 Software Issues

### **🐍 Python & Dependencies**

#### ❌ **Symptom**: `ModuleNotFoundError`
**✅ Solutions**:
```bash
# Reinstall requirements
pip3 install -r requirements.txt --force-reinstall

# Check Python version
python3 --version  # Should be 3.7+

# Install missing system packages
sudo apt update
sudo apt install python3-pip python3-dev

# For specific modules:
pip3 install RPi.GPIO gpiozero pypinyin
```

#### ❌ **Symptom**: Permission denied for GPIO
**✅ Solutions**:
```bash
# Add user to gpio group
sudo usermod -a -G gpio pi

# Run with sudo (temporary fix)
sudo python3 SenTranslator.py

# Check GPIO permissions
ls -l /dev/gpiomem
```

#### ❌ **Symptom**: `ImportError: No module named 'RPi'`
**✅ Solutions**:
```bash
# This usually means not running on Raspberry Pi
# For development on other systems:
pip3 install fake-rpi

# Or check if running on actual Pi:
cat /proc/cpuinfo | grep Hardware
```

### **🎵 Audio & TTS Issues**

#### ❌ **Symptom**: No text-to-speech output
**✅ Solutions**:
```bash
# Check Baidu API credentials
BAIDU_APP_ID = 'your_actual_app_id'
BAIDU_API_KEY = 'your_actual_api_key'
BAIDU_SECRET_KEY = 'your_actual_secret_key'

# Test API connection
python3 tests/audio_test.py

# Verify internet connection
ping -c 3 google.com
```

#### ❌ **Symptom**: Audio crackling or poor quality
**✅ Solutions**:
```bash
# Check audio configuration
sudo raspi-config
# → Advanced Options → Audio → Force 3.5mm

# Test different audio outputs
aplay -l  # List audio devices
aplay /usr/share/sounds/alsa/Front_Left.wav

# Adjust audio settings
alsamixer  # Increase PCM volume
```

#### ❌ **Symptom**: Fixed audio file won't play
**✅ Solutions**:
```bash
# Check file exists and path
ls -la /home/pi/demo_audio.m4a

# Test manual playback
mplayer /home/pi/demo_audio.m4a

# Install missing codecs
sudo apt install mplayer

# Try different audio formats
# Convert to WAV: ffmpeg -i input.m4a output.wav
```

---

## 🔤 Translation & Braille Issues

### **📝 Chinese Text Processing**

#### ❌ **Symptom**: Incorrect Braille output
**✅ Solutions**:
```python
# Check pypinyin installation
pip3 install pypinyin --upgrade

# Verify text encoding
# Input text must be UTF-8 encoded

# Check mapping reference
# See: docs/Complete Chinese-braille mapping.md

# Test with simple characters first
# Try: 你好 (should work correctly)
```

#### ❌ **Symptom**: Some characters not converting
**✅ Solutions**:
- Check character encoding (must be UTF-8)
- Verify character is in mapping table
- Test with simplified characters first
- Check for special punctuation handling

#### ❌ **Symptom**: Wrong pinyin conversion
**✅ Solutions**:
```python
# Update pypinyin library
pip3 install pypinyin --upgrade

# Check conversion manually
from pypinyin import pinyin, Style
print(pinyin('你好', style=Style.NORMAL))

# Should output: [['nǐ'], ['hǎo']]
```

---

## 🌐 Network & Connectivity Issues

### **📡 Internet Connection Problems**

#### ❌ **Symptom**: TTS not working (network required)
**✅ Solutions**:
```bash
# Check internet connection
ping -c 3 8.8.8.8

# Test DNS resolution
nslookup ai.baidu.com

# Check firewall settings
sudo ufw status

# Verify WiFi connection
iwconfig
sudo raspi-config  # → Network Options
```

#### ❌ **Symptom**: Web content extraction fails
**✅ Solutions**:
```bash
# Test web connectivity
curl -I https://www.google.com

# Check certificates
sudo apt update
sudo apt install ca-certificates

# Test with simple URL first
# Use: http://example.com (not https)
```

---

## 🔍 Diagnostic Tools

### **🧪 Built-in Test Scripts**

```bash
# Complete hardware test
python3 tests/hardware_test.py

# Individual servo calibration
python3 tests/servo_test.py

# Audio system check
python3 tests/audio_test.py

# Quick system check
python3 -c "import RPi.GPIO; print('GPIO OK')"
```

### **📊 System Information**

```bash
# Check Pi model and memory
cat /proc/cpuinfo | grep Model
free -h

# Check GPIO status
gpio readall

# Check audio devices
aplay -l
amixer get Master

# Check USB devices
lsusb

# Check power supply voltage
vcgencmd get_throttled
vcgencmd measure_volts
```

### **📈 Performance Monitoring**

```bash
# Monitor CPU and temperature
htop
vcgencmd measure_temp

# Check memory usage
free -h
df -h

# Monitor GPIO activity
gpio read-all
```

---

## 🆘 Emergency Recovery

### **🔄 System Recovery**

#### **Complete system not responding**:
```bash
# Safe shutdown
sudo shutdown -h now

# Force restart (last resort)
# Unplug power for 10 seconds

# Check SD card
# Try different SD card
# Reflash Raspberry Pi OS
```

#### **GPIO conflicts**:
```bash
# Reset all GPIO
sudo python3 -c "import RPi.GPIO; RPi.GPIO.cleanup()"

# Reboot system
sudo reboot

# Check for other programs using GPIO
sudo lsof | grep gpiomem
```

#### **Corrupted configuration**:
```bash
# Reset to defaults
rm servo_config.json
rm audio_config.json

# Recalibrate everything
python3 tests/servo_test.py
```

---

## 📞 Getting Help

### **📋 Before Reporting Issues**

1. **Run diagnostic tests**:
   ```bash
   python3 tests/hardware_test.py
   python3 tests/audio_test.py
   ```

2. **Collect system information**:
   ```bash
   cat /proc/cpuinfo | grep Model
   python3 --version
   pip3 list | grep -E "(RPi|gpio|pypinyin)"
   ```

3. **Check error messages**:
   - Copy exact error text
   - Note when the error occurs
   - List what you were trying to do

### **🐛 Reporting Bugs**

Include this information in your issue report:
- **Pi Model**: Raspberry Pi 4B, etc.
- **OS Version**: `cat /etc/os-release`
- **Python Version**: `python3 --version`
- **Error Message**: Full error text
- **Steps to Reproduce**: What you did before the error
- **Hardware**: Servo models, power supply specs
- 
---

## 🔧 Advanced Troubleshooting

### **⚡ Electrical Testing**

```bash
# Check voltage with multimeter
# Servo VCC should read 5.0V ±0.1V
# GPIO signals should be 3.3V

# Check current draw
# Total system should be < 3A normal operation
# Peak current < 5A during servo movement
```

### **🔬 Signal Analysis**

```bash
# Monitor PWM signals with oscilloscope
# Frequency should be 50Hz (20ms period)
# Pulse width: 1-2ms (5-10% duty cycle)

# Check signal quality
# Clean square waves, no noise/ringing
# Stable frequency and amplitude
```

---

<div align="center">

**🛠️ Still having issues?**

Check our [GitHub Issues](https://github.com/DWSDavid/SenTranslator/issues) or create a new issue with detailed information.

*This guide is continuously updated based on user feedback*

</div>

