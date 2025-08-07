# SenTranslator 🦯

> **World's First Chinese-to-Braille Physical Converter**  
> *Technology Conveys Human Warmth*

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi-red.svg)

---

## 📖 Overview

**SenTranslator** is the world's first localized, physical Chinese Braille real-time conversion hardware. China, home to 20% of the world's visually impaired population, has lacked a dedicated daily reading device for real-time information access throughout history.

Our mission goes beyond creating a device - we're building a barrier-free solution that breaks information boundaries, using technology to illuminate the information world for the visually impaired, ensuring everyone can equally access knowledge and perceive the world.

### 🎯 **Core Mission**
Moving beyond basic safety needs, SenTranslator aims to enhance life happiness and satisfaction for the visually impaired community, enabling equal access to technology and progressing toward higher dimensions of human needs.

---

## ✨ Core Features

🔤 **Real-time Translation**: Chinese/English/Numbers to Braille conversion  
🎬 **Audio-described Experience**: Enhanced multimedia content access  
📱 **Multi-input Support**: OCR/Web/Text input with TTS output  
🖐️ **Physical Tactile Display**: Continuous Braille character display using electronic push rod arrays  
🧠 **Proprietary Algorithm**: Self-developed Chinese Braille mapping system  

---

## 🛠️ Hardware Architecture

- **🥧 Main Controller**: Raspberry Pi 4B
- **⚡ Actuators**: Electronic push rod array (Linear servos)
- **🔧 Core Hardware**: Custom SenTranslator PCB
- **🎛️ Interface**: 3-button tactile control system
- **🔊 Audio**: TTS and audio description support

---

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/YOUR_USERNAME/SenTranslator.git
cd SenTranslator
pip install -r requirements.txt
python3 src/main.py
```

### Basic Usage
1. **Button 1**: Navigate to next Braille group
2. **Button 2**: Play audio description  
3. **Button 3**: Text-to-speech output

---

## 📁 Project Structure

```
SenTranslator/
├── src/
│   └── main.py                 # Main application
├── hardware/
│   ├── schematics/            # Circuit diagrams
│   ├── 3d_models/             # 3D printable parts
│   └── bill_of_materials.md   # Component list
├── docs/
│   └── braille_mapping.md     # Chinese Braille mapping
└── requirements.txt
```

---

## 🔤 Chinese Braille Support

Complete mapping for:
- ✅ **3,500+ Chinese characters** (Simplified)
- ✅ **English alphabet** and numbers
- ✅ **Punctuation marks**
- ✅ **Special pronunciation rules**

*Verified by Shenzhen Information Accessibility Research Institute*

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Shenzhen Information Accessibility Research Institute** - Braille mapping verification
- **Visually Impaired Community** - Invaluable feedback and testing
- **Open Source Contributors** - Making this project possible

---

## 📞 Contact

- **Email**: rwu1016@qq.com / davidwurubis@gmail.com

---

<div align="center">

**🌟Be a light in this world! - DWS🌟**

*If this project helps break information barriers, please give it a ⭐!*

</div>
