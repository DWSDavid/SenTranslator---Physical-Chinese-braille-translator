#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SenTranslator Servo Testing Suite
=================================

This script tests individual servo motors and allows PWM calibration.
Use this to:
1. Test if each servo is working properly
2. Find optimal PWM values for extend/retract positions
3. Calibrate response times for different servo models

Author: SenTranslator Project
Version: 1.0.0
"""

import RPi.GPIO as GPIO
import time
import json
import os
from gpiozero import Button

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Servo pin configurations from main code
SERVO_PINS_GROUP1 = [17, 22, 24, 12, 6, 25]  # First Braille cell
SERVO_PINS_GROUP2 = [16, 19, 26, 13, 20, 21]  # Second Braille cell
ALL_SERVO_PINS = SERVO_PINS_GROUP1 + SERVO_PINS_GROUP2

# Default PWM configuration (from main code)
DEFAULT_PWM_CONFIG = {
    17: (3, 10), 22: (3, 12), 24: (3, 10), 12: (3, 12),
    6: (3, 12), 25: (3, 10), 13: (3, 10), 19: (3, 10),
    26: (4, 11), 16: (3, 10), 20: (3, 10), 21: (3, 10)
}

# Default response times (from main code)
DEFAULT_RESPONSE_TIME = {
    6: 1.5, 12: 1.5
}

# Test button configuration
TEST_BUTTON_PIN = 4  # Use same pin as 'next' button in main code

class ServoTester:
    """Individual servo testing and calibration class"""
    
    def __init__(self, pin):
        self.pin = pin
        self.pwm_extend, self.pwm_retract = DEFAULT_PWM_CONFIG.get(pin, (3, 10))
        self.response_time = DEFAULT_RESPONSE_TIME.get(pin, 0.7)
        
        # Initialize GPIO and PWM
        GPIO.setup(pin, GPIO.OUT)
        self.servo = GPIO.PWM(pin, 50)  # 50Hz frequency
        self.servo.start(0)  # Start with 0 duty cycle
        
        print(f"✅ Servo GPIO {pin} initialized")
        print(f"   Default PWM: Extend={self.pwm_extend}, Retract={self.pwm_retract}")
        print(f"   Response time: {self.response_time}s")

    def test_movement(self, duty_cycle, duration=2.0):
        """Test servo movement with specific PWM duty cycle"""
        print(f"🔧 Testing GPIO {self.pin} with PWM {duty_cycle}% for {duration}s...")
        
        self.servo.ChangeDutyCycle(duty_cycle)
        time.sleep(duration)
        self.servo.ChangeDutyCycle(0)  # Stop PWM signal
        
        print(f"   Movement test completed")

    def calibrate_positions(self):
        """Interactive calibration for optimal PWM values"""
        print(f"\n🎯 CALIBRATING SERVO GPIO {self.pin}")
        print("=" * 50)
        
        # Test extend position
        print("\n📏 EXTEND POSITION CALIBRATION")
        extend_pwm = self.find_optimal_pwm("EXTEND", self.pwm_extend)
        
        # Test retract position  
        print("\n📏 RETRACT POSITION CALIBRATION")
        retract_pwm = self.find_optimal_pwm("RETRACT", self.pwm_retract)
        
        # Test response time
        print("\n⏱️ RESPONSE TIME CALIBRATION")
        response_time = self.find_optimal_timing()
        
        return extend_pwm, retract_pwm, response_time

    def find_optimal_pwm(self, position, start_value):
        """Find optimal PWM value through user feedback"""
        current_pwm = start_value
        
        print(f"\nFinding optimal {position} PWM for GPIO {self.pin}")
        print("Controls: w(+0.5) s(-0.5) e(+0.1) d(-0.1) q(done)")
        
        while True:
            print(f"\nCurrent PWM: {current_pwm}")
            
            # Test current PWM value
            self.servo.ChangeDutyCycle(current_pwm)
            time.sleep(self.response_time)
            self.servo.ChangeDutyCycle(0)
            
            # Get user input
            user_input = input("Adjust PWM (w/s/e/d) or confirm (q): ").lower().strip()
            
            if user_input == 'w':
                current_pwm += 0.5
            elif user_input == 's':
                current_pwm = max(0, current_pwm - 0.5)
            elif user_input == 'e':
                current_pwm += 0.1
            elif user_input == 'd':
                current_pwm = max(0, current_pwm - 0.1)
            elif user_input == 'q':
                print(f"✅ {position} PWM set to: {current_pwm}")
                return current_pwm
            else:
                print("Invalid input! Use w/s/e/d/q")
            
            # Safety limits
            if current_pwm > 15:
                current_pwm = 15
                print("⚠️ PWM limited to 15% for safety")
            elif current_pwm < 0:
                current_pwm = 0

    def find_optimal_timing(self):
        """Find optimal response time through user feedback"""
        current_time = self.response_time
        
        print(f"\nFinding optimal response time for GPIO {self.pin}")
        print("Controls: w(+0.1s) s(-0.1s) e(+0.5s) d(-0.5s) q(done)")
        
        while True:
            print(f"\nCurrent response time: {current_time}s")
            
            # Test current timing with extend/retract cycle
            print("Testing extend...")
            self.servo.ChangeDutyCycle(self.pwm_extend)
            time.sleep(current_time)
            self.servo.ChangeDutyCycle(0)
            
            time.sleep(0.5)
            
            print("Testing retract...")
            self.servo.ChangeDutyCycle(self.pwm_retract)
            time.sleep(current_time)
            self.servo.ChangeDutyCycle(0)
            
            # Get user input
            user_input = input("Adjust timing (w/s/e/d) or confirm (q): ").lower().strip()
            
            if user_input == 'w':
                current_time += 0.1
            elif user_input == 's':
                current_time = max(0.1, current_time - 0.1)
            elif user_input == 'e':
                current_time += 0.5
            elif user_input == 'd':
                current_time = max(0.1, current_time - 0.5)
            elif user_input == 'q':
                print(f"✅ Response time set to: {current_time}s")
                return current_time
            else:
                print("Invalid input! Use w/s/e/d/q")
            
            # Safety limits
            if current_time > 5.0:
                current_time = 5.0
                print("⚠️ Time limited to 5.0s for safety")

    def continuous_test(self, cycles=5, delay=1.0):
        """Continuous extend/retract testing"""
        print(f"\n🔄 CONTINUOUS TEST: {cycles} cycles with {delay}s delay")
        
        for i in range(cycles):
            print(f"Cycle {i+1}/{cycles}: Extend")
            self.servo.ChangeDutyCycle(self.pwm_extend)
            time.sleep(self.response_time)
            self.servo.ChangeDutyCycle(0)
            
            time.sleep(delay)
            
            print(f"Cycle {i+1}/{cycles}: Retract")
            self.servo.ChangeDutyCycle(self.pwm_retract)
            time.sleep(self.response_time)
            self.servo.ChangeDutyCycle(0)
            
            time.sleep(delay)
        
        print("✅ Continuous test completed")

    def cleanup(self):
        """Clean up GPIO resources"""
        self.servo.ChangeDutyCycle(0)
        self.servo.stop()
        print(f"🧹 GPIO {self.pin} cleaned up")


def test_individual_servo():
    """Test a single servo interactively"""
    print("\n" + "="*60)
    print("🔧 INDIVIDUAL SERVO TEST")
    print("="*60)
    
    # Select servo to test
    print("\nAvailable servos:")
    print("Group 1 (Left cell):", SERVO_PINS_GROUP1)
    print("Group 2 (Right cell):", SERVO_PINS_GROUP2)
    
    while True:
        try:
            pin = int(input(f"\nEnter GPIO pin to test (from {ALL_SERVO_PINS}): "))
            if pin in ALL_SERVO_PINS:
                break
            else:
                print(f"❌ Invalid pin! Choose from: {ALL_SERVO_PINS}")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Initialize servo tester
    tester = ServoTester(pin)
    
    try:
        while True:
            print(f"\n🎛️ SERVO GPIO {pin} TEST MENU")
            print("-" * 30)
            print("1. Quick extend/retract test")
            print("2. Custom PWM test")
            print("3. Calibrate optimal settings")
            print("4. Continuous cycling test")
            print("5. Save current settings")
            print("0. Exit")
            
            choice = input("\nSelect option (0-5): ").strip()
            
            if choice == '1':
                # Quick test with default settings
                print("\n🚀 Quick Test")
                tester.test_movement(tester.pwm_extend, 2.0)
                time.sleep(1)
                tester.test_movement(tester.pwm_retract, 2.0)
                
            elif choice == '2':
                # Custom PWM test
                try:
                    pwm = float(input("Enter PWM duty cycle (0-15): "))
                    duration = float(input("Enter test duration (seconds): "))
                    if 0 <= pwm <= 15 and 0.1 <= duration <= 10:
                        tester.test_movement(pwm, duration)
                    else:
                        print("❌ Invalid values! PWM: 0-15, Duration: 0.1-10")
                except ValueError:
                    print("❌ Please enter valid numbers")
                    
            elif choice == '3':
                # Calibration mode
                extend_pwm, retract_pwm, response_time = tester.calibrate_positions()
                tester.pwm_extend = extend_pwm
                tester.pwm_retract = retract_pwm
                tester.response_time = response_time
                
            elif choice == '4':
                # Continuous test
                try:
                    cycles = int(input("Enter number of cycles (1-20): "))
                    if 1 <= cycles <= 20:
                        tester.continuous_test(cycles)
                    else:
                        print("❌ Invalid cycle count! Use 1-20")
                except ValueError:
                    print("❌ Please enter a valid number")
                    
            elif choice == '5':
                # Save settings
                save_servo_config(pin, tester.pwm_extend, tester.pwm_retract, tester.response_time)
                
            elif choice == '0':
                break
            else:
                print("❌ Invalid choice!")
                
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    finally:
        tester.cleanup()


def test_all_servos():
    """Test all servos sequentially"""
    print("\n" + "="*60)
    print("🔧 ALL SERVOS TEST")
    print("="*60)
    
    print("\nPress ENTER to continue to next servo, Ctrl+C to stop")
    
    testers = []
    
    try:
        for pin in ALL_SERVO_PINS:
            print(f"\n📍 Testing Servo GPIO {pin}")
            print("-" * 30)
            
            tester = ServoTester(pin)
            testers.append(tester)
            
            # Quick extend/retract test
            print("Testing extend position...")
            tester.test_movement(tester.pwm_extend, 1.5)
            
            time.sleep(0.5)
            
            print("Testing retract position...")
            tester.test_movement(tester.pwm_retract, 1.5)
            
            # Wait for user confirmation
            input(f"✅ GPIO {pin} test complete. Press ENTER for next servo...")
            
    except KeyboardInterrupt:
        print("\n🛑 Test sequence interrupted")
    finally:
        # Clean up all testers
        for tester in testers:
            tester.cleanup()


def save_servo_config(pin, extend_pwm, retract_pwm, response_time):
    """Save calibrated servo configuration to file"""
    config_file = "servo_config.json"
    
    # Load existing config if it exists
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        config = {}
    
    # Update config for this servo
    config[str(pin)] = {
        "extend_pwm": extend_pwm,
        "retract_pwm": retract_pwm,
        "response_time": response_time
    }
    
    # Save config
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration saved to {config_file}")
    print(f"   GPIO {pin}: Extend={extend_pwm}, Retract={retract_pwm}, Time={response_time}s")


def load_servo_config():
    """Load servo configuration from file"""
    config_file = "servo_config.json"
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        print(f"📁 Loaded configuration from {config_file}")
        for pin, settings in config.items():
            print(f"   GPIO {pin}: {settings}")
        return config
    else:
        print(f"📁 No configuration file found ({config_file})")
        return {}


def main():
    """Main testing interface"""
    print("🎯 SenTranslator Servo Testing Suite")
    print("="*50)
    print("This tool helps you test and calibrate servo motors")
    print("⚠️  Make sure all hardware is properly connected!")
    print("⚠️  Use external 5V power supply for servos!")
    
    # Load existing configuration
    load_servo_config()
    
    try:
        while True:
            print(f"\n🛠️ MAIN MENU")
            print("-" * 20)
            print("1. Test individual servo")
            print("2. Test all servos")
            print("3. Load saved configuration")
            print("0. Exit")
            
            choice = input("\nSelect option (0-3): ").strip()
            
            if choice == '1':
                test_individual_servo()
            elif choice == '2':
                test_all_servos()
            elif choice == '3':
                load_servo_config()
            elif choice == '0':
                print("👋 Exiting servo tester")
                break
            else:
                print("❌ Invalid choice!")
                
    except KeyboardInterrupt:
        print("\n🛑 Program interrupted")
    finally:
        # Final cleanup
        GPIO.cleanup()
        print("🧹 GPIO cleanup completed")


if __name__ == '__main__':
    main()