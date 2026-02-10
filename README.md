# 🔍 FSA Language Identifier - Timor-Leste

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen.svg)

## 🌟 Overview

A desktop application using **Finite State Automata (FSA)** to validate Timor-Leste student data patterns with mobile operator detection.

**Live Features:**
- ✅ Validate NRE (10-digit student ID)
- ✅ Academic email validation (@student.edu.tl)
- ✅ Mobile number validation with operator detection
- ✅ Course code recognition
- ✅ Date format validation (DD/MM/YYYY)
- ✅ GPA validation (0.00-4.00)

## 📱 Operator Detection
- **73, 74** → **Telkomcel** 🔵
- **75, 76** → **Telemor** 🟢  
- **77, 78** → **Timor Telecom** 🟠

## 🚀 Quick Start

### Installation
```bash
# Clone repository
git clone https://github.com/KituDoutel/FSA-Language-Identifier-TL.git

# Install dependencies
pip install Pillow

# Run application

python fsa_app.py
