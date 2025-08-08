# 3D Models for SenTranslator

This folder contains all 3D printable components for the SenTranslator hardware. 

## Print Settings
- Material: PLA recommended
- Layer Height: 0.2m
- Infill: 15% for structural parts
- Supports: Required for some parts

# SenTranslator 3D Printable Components

## Components Overview

### 🏠 Enclosure Parts
- **Main Frame** (`main frame.stl`): Primary housing structure
- **Top Cover** (`removable cover.stl`): Removable access panel, allowing you to revise anything inside the machine

### ⚙️ Internal Components  
- **Pi Mount** (`Pi mount.stl`): Raspberry Pi 4B mounting bracket

### 🔘 User Interface
- **Button Panel** (`braille buttons cover.stl`): Control panel with 3 tactile button holes
- **Braille Buttons** (`braille buttons.stl`): Individual buttons with Braille markings (button 1-3)
- **Braille dots** (`braille buttons.stl`): Simulated Braille dots enlarged proportionally based on standard Braille ratios.

### File Locations
All 3D models are stored in the [`3D printing models`](../3D%20printing%20models/) folder.

## Print Specifications

| Component | Material | Layer Height | Infill | Supports |
|-----------|----------|--------------|--------|----------|
| Main Frame | PLA | 0.2mm | 20% | Yes |
| Top Cover | PLA | 0.2mm | 15% | No |
| Pi Mount | PLA | 0.2mm | 30% | No |
| Button Panel | PLA | 0.2mm | 100% | No |
| Braille Buttons | PLA | 0.2mm | 100% | No |
| Braille dots | PLA | 0.2mm | 100% | Yes |


## Assembly Notes
1. Print button panel with high precision for tactile quality
2. Main frame may require supports for overhangs
3. Test fit Raspberry Pi mount before final assembly
4. Braille markings should be printed with raised dots (positive relief)

## Estimated Print Time
- Total: ~8-12 hours
- Main Frame: ~4-6 hours
- Other components: ~4-6 hours combined
