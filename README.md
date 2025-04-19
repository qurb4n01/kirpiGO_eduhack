# Preparing to International Certification Exams by Classification Methods (AI Powered)

## Overview
This prototype helps users prepare for international language certification exams through interactive, AI-powered exercises. It offers a gamified learning experience with three types of exercises: **listening comprehension**, **grammar (fill-in-the-blank)**, and **reading comprehension**. Users can practice their language skills with immediate feedback and score tracking, making learning engaging and fun.

### Key Features:
- **Listening Comprehension**: Listen to dialogues and select the most appropriate response from multiple-choice options.
- **Grammar (Fill-in-the-Blank)**: Complete sentences by filling in missing words.
- **Reading Comprehension**: Read passages or dialogues and select the correct option based on context.
- **Gamification**: Points for correct answers and tracking of user progress.
- **Speech-to-Text Integration**: Users can respond verbally, and their speech is converted to text for evaluation.
- **Text-to-Speech Integration**: The system reads aloud the dialogue and questions, aiding understanding and pronunciation.

This prototype is designed to be scalable across different languages and certification systems, enhancing preparation for language certification exams in a fun and interactive manner.

## Features
- **Interactive Learning**: Includes multiple-choice questions for listening, grammar, and reading comprehension.
- **Speech-to-Text**: Users can speak their answers, which are recognized and converted into text.
- **Text-to-Speech**: Dialogue and questions are read aloud to users using **Google Text-to-Speech (gTTS)**.
- **Gamified Experience**: Users earn points for correct answers and can track their progress.
- **Multiple Language Support**: While focused on language certification exams, this prototype can be adapted for various languages.

## Installation

1. **Install Dependencies**: Ensure Python 3.x is installed, then install the following libraries:
   - `gTTS` for text-to-speech functionality.
   - `playsound` for audio playback.
   - `SpeechRecognition` for speech-to-text functionality.
   
   Install them using `pip`:
   
   ```bash
   pip install gTTS playsound SpeechRecognition
