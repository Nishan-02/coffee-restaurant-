# ☕ Brew Haven Café – Smart Coffee Shop Web Application

## Overview

**Brew Haven Café** is an interactive web application that simulates a modern premium coffee shop experience. The platform allows users to explore a digital café environment, view menu items, place orders, and interact with an intelligent chatbot assistant.

The application is built using **Streamlit** and integrates a conversational chatbot powered by an **n8n automation workflow**. The goal of the project is to demonstrate how modern web technologies and automation tools can enhance customer engagement in café or restaurant environments.

---

# Project Objectives

The main objectives of the project are:

- Provide a modern digital café browsing experience.
- Allow users to explore menu items visually.
- Simulate a simplified ordering system.
- Provide automated customer assistance through a chatbot.
- Demonstrate integration between UI frameworks and automation platforms.

---

# Key Features

## 1. Interactive Café Homepage

The homepage provides a welcoming café experience with:

- Hero section introducing the café
- High-quality coffee imagery
- Description of the café philosophy
- Navigation to menu and other sections

This page is designed to simulate the landing page of a premium café website.

---

## 2. Digital Menu System

The menu page displays all available items categorized into:

- Hot Coffee
- Cold Coffee
- Pastries

Each menu item includes:

- Product image
- Description
- Price
- Card-based UI layout

The layout improves the browsing experience and visually represents products similar to modern café websites.

---

## 3. Order Simulation System

Users can simulate placing a coffee order by selecting:

- Drink type
- Cup size (Tall, Grande, Venti)
- Milk preference

Once an order is confirmed, the system provides a confirmation message and visual feedback.

This simulates a simplified café ordering experience.

---

## 4. Analytics Dashboard

The dashboard demonstrates basic business analytics using charts.

It shows:

- Popular drink orders
- Order distribution
- Data visualization using interactive charts

This feature helps stakeholders understand how analytics can be integrated into digital restaurant platforms.

---

## 5. AI Chatbot Assistant

The platform includes a floating **chatbot assistant** that provides instant responses to user queries.

The chatbot can assist users with:

- Menu recommendations
- Café timings
- Drink suggestions
- General café questions

### Chatbot Architecture

```
User → Chat Widget → Local Proxy → n8n Webhook → AI Workflow → Response
```

The local proxy server helps bypass browser CORS limitations and securely forwards requests to the automation workflow.

---

# Technology Stack

The project uses the following technologies:

### Frontend / UI

- Python
- Streamlit

### Data Handling

- Pandas

### Data Visualization

- Plotly

### Chatbot Integration

- n8n Automation Platform
- Webhook-based API communication
- Local HTTP proxy server

### Backend Components

- Python HTTP Server
- Requests library
- JSON data handling

---

# System Architecture

```
User Interface
      ↓
Streamlit Application
      ↓
Local Chat Proxy Server
      ↓
n8n Automation Workflow
      ↓
AI Response Returned to User
```

This architecture enables chatbot automation without exposing direct API calls from the browser.

---

# Installation and Setup

## Step 1: Install Python Dependencies

Install the required libraries:

```bash
pip install streamlit pandas plotly requests
```

---

## Step 2: Run the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

The application will open automatically in a browser at:

```
http://localhost:8501
```

---

# Target Users

The application is designed for:

- Café and restaurant businesses
- Hospitality industry stakeholders
- Developers exploring AI chatbot integrations
- Students learning modern web application development
- Entrepreneurs building digital restaurant platforms

---

# Benefits for Stakeholders

## Improved Customer Engagement

Customers can interact with the café digitally before visiting.

## Automated Customer Support

The chatbot provides automated assistance, reducing the need for manual customer support.

## Data Insights

The analytics dashboard demonstrates how business data can be visualized to support decision-making.

## Scalable Architecture

The system can easily integrate additional automation workflows or AI models.

---

# Future Improvements

The current version represents a prototype. Future versions may include:

### AI-Powered Recommendations
Integration of advanced AI models to suggest drinks based on user preferences.

### Online Payment Integration
Adding payment gateways for real café transactions.

### User Accounts
Allow customers to create profiles and track orders.

### Real Order Management
Integration with kitchen management systems.

### Inventory Management
Track ingredient availability in real time.

### Personalized Marketing
Use user interaction data to provide personalized offers.

### Mobile Optimization
Enhance responsiveness for mobile users.

### Voice Assistant Integration
Allow voice-based ordering through speech recognition.

---

# Possible Business Extensions

This platform could evolve into a complete **digital café management platform** with:

- Smart ordering systems
- Customer loyalty programs
- AI-driven sales insights
- Automated customer support

---

# Conclusion

Brew Haven Café demonstrates how modern technologies such as **Streamlit, automation workflows, and chatbot integrations** can create engaging digital experiences for the hospitality industry.

The project highlights the potential of combining **interactive web applications and intelligent automation** to improve customer experience and business efficiency.

---

# Author

Developed as a demonstration project for modern café web application development.
