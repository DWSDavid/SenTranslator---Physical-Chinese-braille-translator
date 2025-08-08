#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SenTranslator Complete Hardware Test Suite
=========================================

This script provides comprehensive testing for all SenTranslator hardware:
1. Individual servo motor testing and calibration
2. Button input testing
3. Audio output testing
4. Complete system integration testing
5. Braille pattern validation

Author: SenTranslator Project
Version: 1.0.0
"""

import RPi.GPIO as GPIO
import time
import json
import subprocess
from gpiozero import Button
from aip import AipSpeech

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Hardware configuration from main code
SERVO_PINS_GROUP1 = [17, 22, 24, 12, 6, 25]  # Left Braille cell
SERVO_PINS_GROUP2 = [16, 19, 26, 13, 20, 21]  # Right Braille cell
ALL_SERVO_PINS = SERVO_PINS_GROUP1 + SERVO_PINS_GROUP2

BUTTON_PINS = {
    'next': 4,    # Navigate/confirm button
    'audio': 27,  # Audio playback button
    'tts': 5      # Text-to-speech button
}

# Test Braille patterns
TEST_PATTERNS = {
    'all_dots': [1, 2, 3, 4, 5, 6],
    'no_dots': [],
    'top_row': [1, 4],
    'middle_row': [2, 5],
    'bottom_row': [3, 6],
    'left_column': [1, 2, 3],
    'right_column': [4, 5, 6],
    'letter_a': [1],
    'letter_b': [1, 2],
    'number_sign': [3, 4, 5, 6]
}

class HardwareTester:
    """Complete hardware testing and validation class"""
    
    def __init__(self):
        self.servos = {}
        self.buttons = {}
        self.servo_config = self.load_servo_config()
        self.init_hardware()
        print("🔧 Hardware Tester initialized")

    def load_servo_config(self):
        """Load servo configuration from file"""
        try:
            with open("servo_config.json", 'r') as f:
                config = json.load(f)
            print("📁 Loaded servo configuration")
            return config
        except FileNotFoundError:
            print("📁 Using default servo configuration")
            return {}

    def init_hardware(self):
        """Initialize all hardware components"""
        print("🔧 Initializing hardware...")
        
        # Initialize servos
        for pin in ALL_SERVO_PINS:
            try:
                GPIO.setup(pin, GPIO.OUT)
                servo = GPIO.PWM(pin, 50)
                servo.start(0)
                self.servos[pin] = servo
                print(f"✅ Servo GPIO {pin} initialized")
            except Exception as e:
                print(f"❌ Servo GPIO {pin} failed: {str(e)}")
        
        # Initialize buttons
        for name, pin in BUTTON_PINS.items():
            try:
                self.buttons[name] = Button(pin)
                print(f"✅ Button '{name}' (GPIO {pin}) initialized")
            except Exception as e:
                print(f"❌ Button '{name}' (GPIO {pin}) failed: {str(e)}")

    def test_servo_movement(self, pin, extend_pwm=3, retract_pwm=10, duration=1.5):
        """Test individual servo movement"""
        if pin not in self.servos:
            print(f"❌ Servo GPIO {pin} not initialized")
            return False
        
        servo = self.servos[pin]
        
        try:
            print(f"🔧 Testing servo GPIO {pin}: Extend")
            servo.ChangeDutyCycle(extend_pwm)
            time.sleep(duration)
            
            print(f"🔧 Testing servo GPIO {pin}: Retract")
            servo.ChangeDutyCycle(retract_pwm)
            time.sleep(duration)
            
            servo.ChangeDutyCycle(0)  # Stop PWM
            print(f"✅ Servo GPIO {pin} test completed")
            return True
            
        except Exception as e:
            print(f"❌ Servo GPIO {pin} test failed: {str(e)}")
            return False

    def test_all_servos_sequential(self):
        """Test all servos one by one"""
        print("\n🔧 SEQUENTIAL SERVO TEST")
        print("=" * 35)
        
        results = {}
        
        for i, pin in enumerate(ALL_SERVO_PINS, 1):
            print(f"\n📍 Testing Servo {i}/12 (GPIO {pin})")
            
            # Use custom config if available
            if str(pin) in self.servo_config:
                config = self.servo_config[str(pin)]
                extend_pwm = config.get('extend_pwm', 3)
                retract_pwm = config.get('retract_pwm', 10)
                response_time = config.get('response_time', 1.5)
            else:
                extend_pwm, retract_pwm, response_time = 3, 10, 1.5
            
            success = self.test_servo_movement(pin, extend_pwm, retract_pwm, response_time)
            results[pin] = success
            
            # Brief pause between servos
            time.sleep(0.5)
        
        # Summary
        passed = sum(results.values())
        total = len(results)
        print(f"\n📊 Servo Test Results: {passed}/{total} servos working")
        
        for pin, success in results.items():
            status = "✅" if success else "❌"
            print(f"   GPIO {pin}: {status}")
        
        return results

    def test_braille_patterns(self):
        """Test various Braille patterns on both cells"""
        print("\n⠿ BRAILLE PATTERN TEST")
        print("=" * 30)
        
        for pattern_name, dots in TEST_PATTERNS.items():
            print(f"\n🔤 Testing pattern: {pattern_name} {dots}")
            
            # Display on both cells
            self.display_braille_pattern(SERVO_PINS_GROUP1, dots)
            time.sleep(2)
            
            self.display_braille_pattern(SERVO_PINS_GROUP2, dots)
            time.sleep(2)
            
            # Clear both cells
            self.clear_braille_cells()
            time.sleep(1)
        
        print("✅ Braille pattern test completed")

    def display_braille_pattern(self, servo_pins, dots):
        """Display a Braille pattern on specified servo group"""
        # First retract all dots in the group
        for i, pin in enumerate(servo_pins, 1):
            if pin in self.servos:
                retract_pwm = 10
                if str(pin) in self.servo_config:
                    retract_pwm = self.servo_config[str(pin)].get('retract_pwm', 10)
                self.servos[pin].ChangeDutyCycle(retract_pwm)
        
        time.sleep(0.5)
        
        # Then extend specified dots
        for dot in dots:
            if 1 <= dot <= 6:
                pin = servo_pins[dot - 1]
                if pin in self.servos:
                    extend_pwm = 3
                    if str(pin) in self.servo_config:
                        extend_pwm = self.servo_config[str(pin)].get('extend_pwm', 3)
                    self.servos[pin].ChangeDutyCycle(extend_pwm)
        
        time.sleep(0.5)
        
        # Stop all PWM signals but maintain position
        for pin in servo_pins:
            if pin in self.servos:
                self.servos[pin].ChangeDutyCycle(0)

    def clear_braille_cells(self):
        """Retract all Braille dots"""
        for pin in ALL_SERVO_PINS:
            if pin in self.servos:
                retract_pwm = 10
                if str(pin) in self.servo_config:
                    retract_pwm = self.servo_config[str(pin)].get('retract_pwm', 10)
                self.servos[pin].ChangeDutyCycle(retract_pwm)
        
        time.sleep(1)
        
        # Stop all PWM signals
        for pin in ALL_SERVO_PINS:
            if pin in self.servos:
                self.servos[pin].ChangeDutyCycle(0)

    def test_button_inputs(self):
        """Test all button inputs"""
        print("\n🔘 BUTTON INPUT TEST")
        print("=" * 25)
        
        print("Press each button when prompted...")
        print("(Press Ctrl+C to skip button tests)")
        
        for name, button in self.buttons.items():
            if button is None:
                print(f"❌ Button '{name}' not available")
                continue
            
            print(f"\n🔘 Press the '{name}' button...")
            
            try:
                # Wait for button press with timeout
                start_time = time.time()
                while not button.is_pressed and (time.time() - start_time) < 10:
                    time.sleep(0.1)
                
                if button.is_pressed:
                    print(f"✅ Button '{name}' working correctly")
                    button.wait_for_release()  # Wait for release
                else:
                    print(f"⚠️ Button '{name}' not pressed (timeout)")
                    
            except KeyboardInterrupt:
                print("\n⏭️ Button test skipped")
                break
            except Exception as e:
                print(f"❌ Button '{name}' test failed: {str(e)}")

    def test_audio_basic(self):
        """Basic audio output test"""
        print("\n🔊 BASIC AUDIO TEST")
        print("=" * 25)
        
        try:
            # Test system beep
            print("Testing system beep...")
            subprocess.run(['speaker-test', '-t', 'sine', '-f', '1000', '-l', '1'], 
                         capture_output=True, timeout=10)
            
            heard = input("Did you hear the test beep? (y/n): ").lower().strip()
            if heard in ['y', 'yes']:
                print("✅ Basic audio output working")
                return True
            else:
                print("❌ Audio output issue detected")
                return False
                
        except Exception as e:
            print(f"⚠️ Audio test failed: {str(e)}")
            return False

    def integration_test(self):
        """Complete system integration test"""
        print("\n🎯 INTEGRATION TEST")
        print("=" * 25)
        print("Testing complete SenTranslator functionality...")
        
        # Test sequence: Display "Hello" in Braille with audio
        test_sequence = [
            ("H", [1, 2, 5]),           # Letter H
            ("e", [1, 5]),              # Letter e  
            ("l", [1, 2, 3]),           # Letter l
            ("l", [1, 2, 3]),           # Letter l
            ("o", [1, 3, 5])            # Letter o
        ]
        
        print("\n🔤 Displaying 'Hello' in Braille...")
        
        for i, (letter, dots) in enumerate(test_sequence):
            print(f"Displaying '{letter}': {dots}")
            
            # Alternate between left and right cells
            if i % 2 == 0:
                self.display_braille_pattern(SERVO_PINS_GROUP1, dots)
            else:
                self.display_braille_pattern(SERVO_PINS_GROUP2, dots)
            
            # Hold for 2 seconds
            time.sleep(2)
            
            # Brief pause between letters
            time.sleep(0.5)
        
        # Clear all cells
        self.clear_braille_cells()
        
        print("✅ Integration test completed")

    def stress_test(self, cycles=10):
        """Stress test all servos with rapid cycling"""
        print(f"\n💪 STRESS TEST ({cycles} cycles)")
        print("=" * 30)
        
        print("⚠️ This test will rapidly cycle all servos")
        confirm = input("Continue? (y/n): ").lower().strip()
        
        if confirm not in ['y', 'yes']:
            print("⏭️ Stress test skipped")
            return
        
        for cycle in range(cycles):
            print(f"Cycle {cycle + 1}/{cycles}")
            
            # Extend all servos
            for pin in ALL_SERVO_PINS:
                if pin in self.servos:
                    extend_pwm = 3
                    if str(pin) in self.servo_config:
                        extend_pwm = self.servo_config[str(pin)].get('extend_pwm', 3)
                    self.servos[pin].ChangeDutyCycle(extend_pwm)
            
            time.sleep(0.5)
            
            # Retract all servos
            for pin in ALL_SERVO_PINS:
                if pin in self.servos:
                    retract_pwm = 10
                    if str(pin) in self.servo_config:
                        retract_pwm = self.servo_config[str(pin)].get('retract_pwm', 10)
                    self.servos[pin].ChangeDutyCycle(retract_pwm)
            
            time.sleep(0.5)
            
            # Stop all PWM
            for pin in ALL_SERVO_PINS:
                if pin in self.servos:
                    self.servos[pin].ChangeDutyCycle(0)
            
            time.sleep(0.2)
        
        print("✅ Stress test completed")

    def cleanup(self):
        """Clean up all hardware resources"""
        print("\n🧹 Cleaning up hardware...")
        
        # Stop all servo PWM
        for pin, servo in self.servos.items():
            try:
                servo.ChangeDutyCycle(0)
                servo.stop()
            except:
                pass
        
        # Clean up GPIO
        GPIO.cleanup()
        print("✅ Hardware cleanup completed")


def main():
    """Main hardware testing interface"""
    print("🔧 SenTranslator Hardware Testing Suite")
    print("=" * 50)
    print("Complete hardware validation for SenTranslator")
    print("⚠️  Ensure all hardware is properly connected!")
    print("⚠️  Use external 5V power supply for servos!")
    
    tester = HardwareTester()
    
    try:
        while True:
            print(f"\n🛠️ HARDWARE TEST MENU")
            print("-" * 30)
            print("1. Test all servos sequentially")
            print("2. Test Braille patterns")
            print("3. Test button inputs")
            print("4. Test basic audio")
            print("5. Complete integration test")
            print("6. Stress test (advanced)")
            print("7. Run comprehensive test")
            print("0. Exit")
            
            choice = input("\nSelect option (0-7): ").strip()
            
            if choice == '1':
                tester.test_all_servos_sequential()
            elif choice == '2':
                tester.test_braille_patterns()
            elif choice == '3':
                tester.test_button_inputs()
            elif choice == '4':
                tester.test_audio_basic()
            elif choice == '5':
                tester.integration_test()
            elif choice == '6':
                cycles = int(input("Enter number of stress cycles (1-50): ") or "10")
                tester.stress_test(min(cycles, 50))
            elif choice == '7':
                # Run all tests
                print("\n🎯 COMPREHENSIVE HARDWARE TEST")
                print("=" * 40)
                tester.test_all_servos_sequential()
                tester.test_braille_patterns()
                tester.test_button_inputs()
                tester.test_audio_basic()
                tester.integration_test()
                print("\n🎉 Comprehensive test completed!")
            elif choice == '0':
                print("👋 Exiting hardware tester")
                break
            else:
                print("❌ Invalid choice!")
                
    except KeyboardInterrupt:
        print("\n🛑 Hardware testing interrupted")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
    finally:
        tester.cleanup()


if __name__ == '__main__':
    main()