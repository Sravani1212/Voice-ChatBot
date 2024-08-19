# Voice Chatbot for Car Showroom

This repository contains the implementation of a voice chatbot designed to interact with customers, gather information about their preferences, compare competitive products, and schedule appointments with sales representatives. The chatbot is tailored for use in car showrooms, whether for new or used vehicles.

# Project Overview

# Features

- Voice Interaction: The chatbot communicates with customers through voice, making inquiries about their interest in specific car models, gathering details, and answering questions.
- Product Comparison: The chatbot provides a comparison of competitive car models based on the customer's preferences, helping them make informed decisions.
- Appointment Booking: If the customer decides to proceed, the chatbot can schedule an appointment with a sales representative, ensuring a seamless transition from inquiry to action.
- API Integration: Leverages APIs from Google, Microsoft, or OpenAI for natural language processing (NLP), speech recognition, and speech synthesis.


# Use Cases

- New or used car showrooms looking to automate customer inquiries and appointment scheduling.
- Sales teams seeking to provide customers with detailed comparisons of car models based on their preferences.
- Enhancing customer experience by providing a conversational, voice-based interface.

# Repository Structure

- `src/`: Contains the source code for the chatbot, including modules for voice interaction, product comparison, and appointment scheduling.
- `data/`: Sample data and templates used for testing and training the chatbot.
- `scripts/`: Utility scripts for managing API keys, handling customer data, and integrating with showroom management systems.


# Installation

# API Setup

Ensure you have the necessary API keys for Google, OpenAI services. Set up your environment variables:

```bash
export GOOGLE_API_KEY=your_google_api_key
export OPENAI_API_KEY=your_openai_api_key
```

## Usage

# Running the Chatbot

To start the chatbot with default settings:

```bash
python src/chatbot.py --api google
```

# Appointment Scheduling

The chatbot automatically offers to schedule an appointment after the customer decides on a car model. To view scheduled appointments:

```bash
python scripts/view_appointments.py
```

