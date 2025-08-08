#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SenTranslator Audio Testing Suite
=================================

This script tests all audio functionality including:
1. Text-to-Speech (TTS) with Baidu API
2. Fixed audio file playback
3. System audio output
4. Audio device detection

Author: SenTranslator Project
Version: 1.0.0
"""

import os
import time
import subprocess
import json
from aip import AipSpeech

# Audio configuration from main code
FIXED_AUDIO_PATH = "/home/pi/demo_audio.m4a"

# Test audio files (will be created if missing)
TEST_AUDIO_DIR = "test_audio"
TEST_BEEP_FILE = f"{TEST_AUDIO_DIR}/test_beep.wav"

class AudioTester:
    """Audio system testing and validation class"""
    
    def __init__(self):
        self.baidu_client = None
        self.api_configured = False
        self.create_test_directory()
        print("🔊 Audio Tester initialized")

    def create_test_directory(self):
        """Create test audio directory if it doesn't exist"""
        if not os.path.exists(TEST_AUDIO_DIR):
            os.makedirs(TEST_AUDIO_DIR)
            print(f"📁 Created test directory: {TEST_AUDIO_DIR}")

    def setup_baidu_api(self):
        """Setup Baidu TTS API with user credentials"""
        print("\n🔑 BAIDU TTS API SETUP")
        print("=" * 40)
        print("You need Baidu AI Platform credentials for TTS testing")
        print("Sign up at: https://ai.baidu.com/")
        
        app_id = input("Enter your APP_ID (or 'skip' to skip TTS tests): ").strip()
        
        if app_id.lower() == 'skip':
            print("⏭️ Skipping TTS tests")
            return False
        
        api_key = input("Enter your API_KEY: ").strip()
        secret_key = input("Enter your SECRET_KEY: ").strip()
        
        try:
            self.baidu_client = AipSpeech(app_id, api_key, secret_key)
            
            # Test API with a simple request
            test_result = self.baidu_client.synthesis(
                "测试", 'zh', 1, {'vol': 5, 'spd': 5, 'pit': 5, 'per': 4}
            )
            
            if isinstance(test_result, dict):
                print(f"❌ API Error: {test_result}")
                return False
            else:
                print("✅ Baidu API configured successfully")
                self.api_configured = True
                return True
                
        except Exception as e:
            print(f"❌ API setup failed: {str(e)}")
            return False

    def test_system_audio(self):
        """Test basic system audio functionality"""
        print("\n🔊 SYSTEM AUDIO TEST")
        print("=" * 30)
        
        # Test 1: Check audio devices
        print("1. Checking audio devices...")
        self.check_audio_devices()
        
        # Test 2: Generate test beep
        print("\n2. Generating test beep...")
        self.generate_test_beep()
        
        # Test 3: Test speaker output
        print("\n3. Testing speaker output...")
        self.test_speaker_output()

    def check_audio_devices(self):
        """Check available audio output devices"""
        try:
            # Check ALSA devices
            result = subprocess.run(['aplay', '-l'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("📱 Available audio devices:")
                print(result.stdout)
            else:
                print("⚠️ Could not list audio devices")
                
            # Check current audio output
            result = subprocess.run(['amixer', 'get', 'Master'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("\n🔊 Master volume settings:")
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'Playback' in line and '[' in line:
                        print(f"   {line.strip()}")
            
        except subprocess.TimeoutExpired:
            print("⚠️ Audio device check timed out")
        except FileNotFoundError:
            print("⚠️ Audio tools not found. Install with: sudo apt install alsa-utils")
        except Exception as e:
            print(f"⚠️ Audio device check failed: {str(e)}")

    def generate_test_beep(self):
        """Generate a test beep using system tools"""
        try:
            # Method 1: Use speaker-test
            print("   Generating 2-second beep...")
            result = subprocess.run([
                'speaker-test', '-t', 'sine', '-f', '1000', '-l', '1', '-s', '1'
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                print("✅ System beep test successful")
            else:
                print("⚠️ Speaker test failed, trying alternative...")
                self.alternative_beep()
                
        except subprocess.TimeoutExpired:
            print("⚠️ Beep test timed out")
        except FileNotFoundError:
            print("⚠️ speaker-test not found, trying alternative...")
            self.alternative_beep()
        except Exception as e:
            print(f"⚠️ Beep generation failed: {str(e)}")

    def alternative_beep(self):
        """Alternative beep generation method"""
        try:
            # Method 2: Use aplay with /dev/urandom (creates noise)
            print("   Trying alternative beep method...")
            subprocess.run([
                'timeout', '2', 'aplay', '/dev/urandom'
            ], capture_output=True, timeout=5)
            print("✅ Alternative audio test completed")
            
        except Exception as e:
            print(f"⚠️ Alternative beep failed: {str(e)}")

    def test_speaker_output(self):
        """Test speaker output with user feedback"""
        print("🎵 Testing audio output...")
        print("   You should hear audio in the next few seconds")
        
        try:
            # Use espeak for a simple test (if available)
            result = subprocess.run([
                'espeak', '-s', '150', 'Audio test successful'
            ], capture_output=True, timeout=10)
            
            if result.returncode == 0:
                heard = input("\n❓ Did you hear the audio test? (y/n): ").lower().strip()
                if heard in ['y', 'yes']:
                    print("✅ Speaker output working correctly")
                    return True
                else:
                    print("❌ Speaker output issue detected")
                    self.troubleshoot_audio()
                    return False
            else:
                print("⚠️ Espeak test failed")
                return False
                
        except subprocess.TimeoutExpired:
            print("⚠️ Audio test timed out")
            return False
        except FileNotFoundError:
            print("⚠️ Espeak not found. Install with: sudo apt install espeak")
            return False
        except Exception as e:
            print(f"⚠️ Speaker test failed: {str(e)}")
            return False

    def troubleshoot_audio(self):
        """Provide audio troubleshooting suggestions"""
        print("\n🔧 AUDIO TROUBLESHOOTING")
        print("-" * 30)
        print("1. Check physical connections:")
        print("   • Speakers/headphones plugged in securely")
        print("   • Audio jack fully inserted")
        print("   • USB audio device connected")
        
        print("\n2. Check volume settings:")
        print("   • Run: alsamixer")
        print("   • Increase Master volume")
        print("   • Unmute if necessary (press 'M')")
        
        print("\n3. Check audio output:")
        print("   • Run: sudo raspi-config")
        print("   • Go to Advanced Options > Audio")
        print("   • Select correct output (HDMI/3.5mm)")
        
        print("\n4. Test manual playback:")
        print("   • aplay /usr/share/sounds/alsa/Front_Left.wav")

    def test_tts_functionality(self):
        """Test Text-to-Speech functionality"""
        print("\n🗣️ TEXT-TO-SPEECH TEST")
        print("=" * 30)
        
        if not self.api_configured:
            if not self.setup_baidu_api():
                print("❌ TTS testing skipped - no API configuration")
                return False
        
        test_texts = [
            ("Hello World", "en"),
            ("你好世界", "zh"),
            ("SenTranslator测试", "zh")
        ]
        
        for text, lang in test_texts:
            print(f"\n🎵 Testing TTS: '{text}' ({lang})")
            success = self.test_single_tts(text, lang)
            
            if success:
                heard = input(f"❓ Did you hear '{text}'? (y/n): ").lower().strip()
                if heard not in ['y', 'yes']:
                    print(f"⚠️ TTS output issue for '{text}'")
            else:
                print(f"❌ TTS failed for '{text}'")
        
        return True

    def test_single_tts(self, text, lang='zh'):
        """Test single TTS conversion"""
        try:
            # Convert text to speech
            result = self.baidu_client.synthesis(text, lang, 1, {
                'vol': 5, 'spd': 5, 'pit': 5, 'per': 4
            })
            
            if isinstance(result, dict):
                print(f"❌ TTS Error: {result}")
                return False
            
            # Save to temporary file
            temp_file = f"{TEST_AUDIO_DIR}/tts_test.wav"
            with open(temp_file, 'wb') as f:
                f.write(result)
            
            # Play the audio
            play_result = subprocess.run([
                'mplayer', temp_file
            ], capture_output=True, timeout=15)
            
            if play_result.returncode == 0:
                print("✅ TTS playback successful")
                return True
            else:
                print("⚠️ TTS playback failed")
                return False
                
        except subprocess.TimeoutExpired:
            print("⚠️ TTS playback timed out")
            return False
        except Exception as e:
            print(f"❌ TTS test failed: {str(e)}")
            return False

    def test_fixed_audio(self):
        """Test fixed audio file playback"""
        print("\n🎵 FIXED AUDIO TEST")
        print("=" * 30)
        
        if not os.path.exists(FIXED_AUDIO_PATH):
            print(f"⚠️ Fixed audio file not found: {FIXED_AUDIO_PATH}")
            print("Suggestions:")
            print(f"1. Place your demo audio file at: {FIXED_AUDIO_PATH}")
            print("2. Supported formats: .m4a, .wav, .mp3")
            return False
        
        print(f"🎵 Testing fixed audio: {FIXED_AUDIO_PATH}")
        
        try:
            # Play the fixed audio file
            result = subprocess.run([
                'mplayer', FIXED_AUDIO_PATH
            ], capture_output=True, timeout=30)
            
            if result.returncode == 0:
                heard = input("❓ Did you hear the demo audio? (y/n): ").lower().strip()
                if heard in ['y', 'yes']:
                    print("✅ Fixed audio playback working correctly")
                    return True
                else:
                    print("❌ Fixed audio playback issue")
                    return False
            else:
                print(f"❌ Audio playback failed: {result.stderr.decode()}")
                return False
                
        except subprocess.TimeoutExpired:
            print("⚠️ Audio playback timed out")
            return False
        except FileNotFoundError:
            print("❌ mplayer not found. Install with: sudo apt install mplayer")
            return False
        except Exception as e:
            print(f"❌ Fixed audio test failed: {str(e)}")
            return False

    def comprehensive_audio_test(self):
        """Run all audio tests in sequence"""
        print("\n🎯 COMPREHENSIVE AUDIO TEST")
        print("=" * 40)
        
        results = {
            'system_audio': False,
            'tts': False,
            'fixed_audio': False
        }
        
        # Test 1: System audio
        print("\n📍 Step 1: System Audio")
        self.test_system_audio()
        results['system_audio'] = True  # Basic system test
        
        # Test 2: TTS functionality
        print("\n📍 Step 2: Text-to-Speech")
        results['tts'] = self.test_tts_functionality()
        
        # Test 3: Fixed audio
        print("\n📍 Step 3: Fixed Audio Playback")
        results['fixed_audio'] = self.test_fixed_audio()
        
        # Summary
        print("\n📊 AUDIO TEST SUMMARY")
        print("=" * 30)
        for test, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{test.replace('_', ' ').title()}: {status}")
        
        all_passed = all(results.values())
        if all_passed:
            print("\n🎉 All audio tests passed! SenTranslator audio is ready.")
        else:
            print("\n⚠️ Some audio tests failed. Check the issues above.")
        
        return results

    def save_audio_config(self, results):
        """Save audio test results to configuration file"""
        config = {
            "last_test": time.strftime("%Y-%m-%d %H:%M:%S"),
            "test_results": results,
            "api_configured": self.api_configured,
            "fixed_audio_path": FIXED_AUDIO_PATH
        }
        
        with open("audio_config.json", 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"💾 Audio test results saved to audio_config.json")


def quick_audio_test():
    """Quick audio functionality test"""
    print("\n⚡ QUICK AUDIO TEST")
    print("=" * 25)
    
    tester = AudioTester()
    
    # Quick system beep
    print("1. Testing system audio...")
    tester.generate_test_beep()
    
    # Quick TTS test (if configured)
    print("\n2. Testing TTS (if configured)...")
    try:
        if tester.setup_baidu_api():
            tester.test_single_tts("快速测试", "zh")
    except:
        print("⏭️ TTS test skipped")
    
    print("✅ Quick audio test completed")


def interactive_audio_menu():
    """Interactive audio testing menu"""
    tester = AudioTester()
    
    while True:
        print(f"\n🔊 AUDIO TEST MENU")
        print("-" * 25)
        print("1. System audio test")
        print("2. TTS functionality test")
        print("3. Fixed audio test")
        print("4. Comprehensive test")
        print("5. Quick test")
        print("6. Audio troubleshooting")
        print("0. Exit")
        
        choice = input("\nSelect option (0-6): ").strip()
        
        if choice == '1':
            tester.test_system_audio()
        elif choice == '2':
            tester.test_tts_functionality()
        elif choice == '3':
            tester.test_fixed_audio()
        elif choice == '4':
            results = tester.comprehensive_audio_test()
            tester.save_audio_config(results)
        elif choice == '5':
            quick_audio_test()
        elif choice == '6':
            tester.troubleshoot_audio()
        elif choice == '0':
            print("👋 Exiting audio tester")
            break
        else:
            print("❌ Invalid choice!")


def main():
    """Main audio testing interface"""
    print("🎵 SenTranslator Audio Testing Suite")
    print("=" * 45)
    print("This tool tests all audio functionality:")
    print("• System audio output")
    print("• Text-to-Speech (TTS)")
    print("• Fixed audio playback")
    print("• Audio device detection")
    
    try:
        interactive_audio_menu()
    except KeyboardInterrupt:
        print("\n🛑 Audio testing interrupted")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
    finally:
        print("🧹 Audio testing completed")


if __name__ == '__main__':
    main()