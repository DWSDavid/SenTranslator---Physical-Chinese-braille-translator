
# Complete Chinese Braille Mapping

> **Verified by Shenzhen Information Accessibility Research Institute**  
> Open-source complete Chinese Braille mapping collection

---

## 📖 Overview

This document contains the complete mapping system used by SenTranslator to convert Chinese text into Braille patterns. Each Braille cell consists of 6 dots arranged in 2 columns and 3 rows, numbered 1-6. Noting the following mapping rules and contents is universal and can be use for any other purposes.

```
Braille Cell Layout:
1 • • 4
2 • • 5  
3 • • 6
```

---

## 🎵 Initial Consonants (声母)

Chinese initials are converted to Braille patterns based on phonetic similarity and systematic organization.

| Initial | Pinyin | Braille Dots | Pattern | Notes |
|---------|--------|--------------|---------|-------|
| b | b | 1-2 | ⠃ | Basic labial |
| p | p | 1-2-3-4 | ⠏ | Aspirated labial |
| m | m | 1-3-4 | ⠍ | Nasal labial |
| f | f | 1-2-4 | ⠋ | Fricative labial |
| d | d | 1-4-5 | ⠙ | Basic dental |
| t | t | 2-3-4-5 | ⠞ | Aspirated dental |
| n | n | 1-3-4-5 | ⠝ | Nasal dental |
| l | l | 1-2-3 | ⠇ | Liquid dental |
| g | g | 1-2-4-5 | ⠛ | Basic velar |
| k | k | 1-3 | ⠅ | Aspirated velar |
| h | h | 1-2-5 | ⠓ | Fricative velar |
| j | j | 1-2-5 | ⠓ | Palatal (g→j before i/u/ü) |
| q | q | 1-3 | ⠅ | Aspirated palatal (k→q before i/u/ü) |
| x | x | 1-2-5 | ⠓ | Fricative palatal (h→x before i/u/ü) |
| zh | zh | 3-4 | ⠌ | Retroflex affricate |
| ch | ch | 1-2-3-4-5 | ⠟ | Aspirated retroflex |
| sh | sh | 1-5-6 | ⠱ | Retroflex fricative |
| r | r | 2-4-5 | ⠚ | Retroflex approximant |
| z | z | 1-3-5-6 | ⠵ | Dental affricate |
| c | c | 1-4 | ⠉ | Aspirated dental affricate |
| s | s | 2-3-4 | ⠎ | Dental fricative |
| y | y | 3-4-5-6 | ⠼ | Palatal approximant |
| w | w | 2-3-5-6 | ⠺ | Labial-velar approximant |

### Special Initial Rules
- **g/k/h → j/q/x**: When followed by i, u, or ü
- **Zero initial**: Words beginning with vowels have no initial consonant pattern

---

## 🌊 Final Vowels (韵母)

### Simple Finals

| Final | Pinyin | Braille Dots | Pattern | Description |
|-------|--------|--------------|---------|-------------|
| a | a | 3-5 | ⠔ | Open central vowel |
| o | o | 1-3-5 | ⠕ | Mid back rounded vowel |
| e | e | 2-6 | ⠢ | Mid central vowel |
| i | i | 2-4 | ⠊ | High front unrounded vowel |
| u | u | 1-3-6 | ⠥ | High back rounded vowel |
| ü | ü/v | 3-4-6 | ⠴ | High front rounded vowel |
| er | er | 1-2-3-5 | ⠗ | Rhotacized vowel |

### Compound Finals

| Final | Pinyin | Braille Dots | Pattern | Composition |
|-------|--------|--------------|---------|-------------|
| ai | ai | 2-4-6 | ⠪ | a + i |
| ei | ei | 2-3-4-6 | ⠮ | e + i |
| ui | ui | 2-4-5-6 | ⠺ | u + i |
| ao | ao | 2-3-5 | ⠖ | a + o |
| ou | ou | 1-2-3-5-6 | ⠷ | o + u |
| iu | iu | 1-2-5-6 | ⠳ | i + u |
| ie | ie | 1-5 | ⠑ | i + e |
| üe | üe/ve/ue | 2-3-4-5-6 | ⠾ | ü + e |

### Nasal Finals

| Final | Pinyin | Braille Dots | Pattern | Type |
|-------|--------|--------------|---------|------|
| an | an | 1-2-3-6 | ⠧ | Front nasal |
| en | en | 3-5-6 | ⠶ | Front nasal |
| in | in | 1-2-6 | ⠣ | Front nasal |
| un | un | 4-5-6 | ⠸ | Front nasal |
| ün | ün/vn | 4-5-6 | ⠸ | Front nasal |
| ang | ang | 2-3-6 | ⠦ | Back nasal |
| eng | eng | 3-4-5-6 | ⠼ | Back nasal |
| ing | ing | 1-6 | ⠡ | Back nasal |
| ong | ong | 2-5-6 | ⠲ | Back nasal |

### Complex Finals

| Final | Pinyin | Braille Dots | Pattern | Structure |
|-------|--------|--------------|---------|-----------|
| ia | ia | 1-2-4-6 | ⠫ | i + a |
| ua | ua | 1-2-3-4-5-6 | ⠿ | u + a |
| uo | uo | 1-3-5 | ⠕ | u + o |
| iao | iao | 3-4-5 | ⠜ | i + ao |
| uai | uai | 1-3-4-5-6 | ⠽ | u + ai |
| uan | uan | 1-2-4-5-6 | ⠻ | u + an |
| ian | ian | 1-4-6 | ⠩ | i + an |
| iang | iang | 1-3-4-6 | ⠭ | i + ang |
| uang | uang | 2-3-5-6 | ⠶ | u + ang |
| iong | iong | 1-4-5-6 | ⠹ | i + ong |
| üan | üan/van | 1-2-3-4-6 | ⠯ | ü + an |
| uen | uen | 2-5 | ⠒ | u + en |
| uei | uei | 2-4-5-6 | ⠺ | u + ei |
| ueng | ueng | 2-5-6 | ⠲ | u + eng |

### Special Final Rules
- **i omission**: After z, c, s, zh, ch, sh, r, standalone 'i' is omitted
- **üe variants**: Can be written as üe, ve, or ue depending on context

---

## 🔢 Numbers

Numbers require a special prefix indicator followed by letter patterns.

| Symbol | Braille Dots | Pattern | Description |
|--------|--------------|---------|-------------|
| # | 3-4-5-6 | ⠼ | Number prefix (required) |
| 1 | 1 | ⠁ | One |
| 2 | 1-2 | ⠃ | Two |
| 3 | 1-4 | ⠉ | Three |
| 4 | 1-4-5 | ⠙ | Four |
| 5 | 1-5 | ⠑ | Five |
| 6 | 1-2-4 | ⠋ | Six |
| 7 | 1-2-4-5 | ⠛ | Seven |
| 8 | 1-2-5 | ⠓ | Eight |
| 9 | 2-4 | ⠊ | Nine |
| 0 | 2-4-5 | ⠚ | Zero |

### Number Usage Rules
- Always prefix numbers with ⠼ (3-4-5-6)
- Consecutive numbers share one prefix: 2024 → ⠼⠃⠚⠃⠙
- Mixed text requires new prefix for each number group

---

## 🔤 English Letters

Standard English Braille (Grade 1) is used for English text within Chinese content.

| Letter | Dots | Pattern | Letter | Dots | Pattern |
|--------|------|---------|--------|------|---------|
| a | 1 | ⠁ | n | 1-3-4-5 | ⠝ |
| b | 1-2 | ⠃ | o | 1-3-5 | ⠕ |
| c | 1-4 | ⠉ | p | 1-2-3-4 | ⠏ |
| d | 1-4-5 | ⠙ | q | 1-2-3-4-5 | ⠟ |
| e | 1-5 | ⠑ | r | 1-2-3-5 | ⠗ |
| f | 1-2-4 | ⠋ | s | 2-3-4 | ⠎ |
| g | 1-2-4-5 | ⠛ | t | 2-3-4-5 | ⠞ |
| h | 1-2-5 | ⠓ | u | 1-3-6 | ⠥ |
| i | 2-4 | ⠊ | v | 1-2-3-6 | ⠧ |
| j | 2-4-5 | ⠚ | w | 2-4-5-6 | ⠺ |
| k | 1-3 | ⠅ | x | 1-3-4-6 | ⠭ |
| l | 1-2-3 | ⠇ | y | 1-3-4-5-6 | ⠽ |
| m | 1-3-4 | ⠍ | z | 1-3-5-6 | ⠵ |

---

## ❗ Punctuation Marks

| Symbol | Chinese | Braille Dots | Pattern | Usage |
|--------|---------|--------------|---------|-------|
| Period | 。 | 2-5-6 | ⠲ | End of sentence |
| Comma | ， | 2 | ⠂ | Pause in sentence |
| Question Mark | ？ | 2-3-6 | ⠦ | Interrogative |
| Exclamation | ！ | 2-3-5 | ⠖ | Emphasis |
| Colon | ： | 2-5 | ⠒ | Introduction |
| Semicolon | ； | 2-3 | ⠆ | Major pause |
| Opening Quote | " | 2-3-6 | ⠦ | Begin quotation |
| Closing Quote | " | 2-3-5-6 | ⠶ | End quotation |
| Opening Paren | （ | 2-3-5-6 | ⠶ | Begin parenthesis |
| Closing Paren | ） | 2-3-5-6 | ⠶ | End parenthesis |
| Em Dash | —— | - | - | Long pause (no dots) |
| Ellipsis | …… | - | - | Trailing off (no dots) |
| Chinese Comma | 、 | 3-4 | ⠌ | Series separator |

---

## 🎯 Tone Markers (Optional)

Chinese tones can be indicated with special markers before syllables.

| Tone | Description | Braille Dots | Pattern | Example |
|------|-------------|--------------|---------|---------|
| 1st | High level (ā) | - | - | No marker needed |
| 2nd | Rising (á) | 2 | ⠂ | ⠂⠍⠁ (má) |
| 3rd | Dipping (ǎ) | 2-3 | ⠆ | ⠆⠍⠁ (mǎ) |
| 4th | Falling (à) | 2-5 | ⠒ | ⠒⠍⠁ (mà) |
| 5th | Neutral (a) | 3 | ⠄ | ⠄⠍⠁ (ma) |

*Note: Tone markers are optional in most Braille texts as context usually provides sufficient information.*

---

## 📝 Conversion Examples

### Example 1: Simple Chinese
**Input**: 你好世界  
**Process**:
- 你 (nǐ) → n + i = ⠝ + ⠊
- 好 (hǎo) → h + ao = ⠓ + ⠖  
- 世 (shì) → sh + i = ⠱ + ⠊
- 界 (jiè) → j + ie = ⠓ + ⠑

**Output**: ⠝⠊ ⠓⠖ ⠱⠊ ⠓⠑

### Example 2: Mixed Content
**Input**: 2024年中国  
**Process**:
- 2024 → ⠼ + ⠃⠚⠃⠙ (number prefix + digits)
- 年 (nián) → n + ian = ⠝ + ⠩
- 中 (zhōng) → zh + ong = ⠌ + ⠲
- 国 (guó) → g + uo = ⠛ + ⠕

**Output**: ⠼⠃⠚⠃⠙ ⠝⠩ ⠌⠲ ⠛⠕

### Example 3: With Punctuation
**Input**: 你好，世界！  
**Process**:
- 你好 → ⠝⠊ ⠓⠖
- ， → ⠂
- 世界 → ⠱⠊ ⠓⠑
- ！ → ⠖

**Output**: ⠝⠊ ⠓⠖⠂ ⠱⠊ ⠓⠑⠖

---

## ⚙️ ! Implementation Notes

### SenTranslator Algorithm Features
1. **Automatic Pinyin Conversion**: Uses pypinyin library for accurate pronunciation
2. **Contextual Rules**: Applies g→j, k→q, h→x transformations automatically
3. **Smart Spacing**: Optimizes Braille cell usage for reading efficiency
4. **Error Handling**: Gracefully handles unknown characters and edge cases

### Performance Optimizations
- **Lookup Tables**: Pre-computed mappings for 3,500+ common characters
- **Caching**: Frequently used conversions stored for speed
- **Batch Processing**: Efficient handling of long texts
- **Memory Management**: Optimized for Raspberry Pi hardware constraints

---

## 📚 References & Standards

### Authoritative Sources
- **Chinese National Standard**: GB/T 15720-2008 "Information Technology - Chinese Braille"
- **Shenzhen Information Accessibility Research Institute**: Verification and validation
- **International Council on English Braille**: English letter standards
- **World Blind Union**: International Braille standards

### Validation Process
1. **Expert Review**: Verified by certified Braille instructors
2. **User Testing**: Validated with visually impaired community members
3. **Cross-Reference**: Compared against existing Chinese Braille materials from both online and offlin

---

## 📄 License & Usage

This mapping table is released under the MIT License as part of the SenTranslator project. You are free to:
- ✅ Use in educational materials
- ✅ Integrate into accessibility software
- ✅ Modify for specific regional requirements
- ✅ Redistribute with attribution

**Attribution Required**: Please credit "SenTranslator"

---

## 🆘 Support & Contributions

### Report Issues
If you find errors or have suggestions for improvements:
- **Email**: rwu1016@qq.com/davidwurubis@gmail.com

---

<div align="center">

**🌟 Be a light in this world - Rubi 🌟**

*This mapping serves millions of Chinese-speaking visually impaired individuals worldwide*

</div>

---

*Last Updated: August 2025 | Version 3.0 |
