# 🏎️ Formula One App

The **Formula One** app is a Django application that provides detailed and structured Formula One data, including races, drivers, teams, and circuits.

This app is divided into **five main sections** accessible through the website.

> ⚡ **Note:** The backend is developed manually by me, while the frontend is fully generated with AI assistance.

> ⚡ **Note:** only the times after 2018 season are in IRST others are in UTC)
---

## 📂 Data

The app uses a `data/` folder to store all datasets, structured as follows:
```
data/
├── source/ # Original datasets downloaded from Kaggle (no modifications)
└── cleaned/ # Preprocessed datasets with additional modifications, including 2025 season results
```
- **source/**: Contains the original CSV files downloaded from Kaggle.  
  > 📝 **Attribution:** Data sourced from [Kaggle](https://www.kaggle.com/)
  - [Author 1](https://www.kaggle.com/datasets/julianbloise/winners-formula-1-1950-to-2025)
  - [Author 2](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020)

- **cleaned/**: Contains processed and modified CSV files used by the app. Changes include data cleaning, formatting, and addition of recent season results (e.g., 2025 season).

---

## 🏠 Home

The Home section displays:

- Results from the **latest season**
- For each Grand Prix:
  - Winning driver
  - Winning team

This page provides a quick overview of how the most recent season unfolded without going into detailed race results.

---

## 🗺️ Circuits

### 📊 Statistics
- Total number of circuits
- Total number of countries

### 📋 Circuit List
- Displays all available circuits
- Each circuit links to a detailed view

### 📍 Circuit Details
For each circuit, you can view:
- Country
- Location
- Additional information
- Google Maps location
- All races held at the circuit (ordered by year)

Each race entry links to its **race results**.

---

## 🏁 Races

### 📊 Statistics
- Total number of races
- Total number of seasons
- Total number of circuits

### 🎯 Filtering
- Races can be filtered by **season**
- Default filter is the **latest season**

### 📋 Race List
- Displays all races for the selected season

### 🧾 Race Details
For each race, the detail page includes:
- FP1, FP2, FP3 sessions
- Qualifying
- Sprint qualifying (if available)
- Sprint race (if available)
- Race date and time
- Full race results:
  - Winner
  - Second and third positions
  - Remaining classified drivers

---

## 👤 Drivers

### 📊 Statistics
- Total number of drivers
- Total nationalities
- Total teams

### 📋 Driver List
- Paginated list (20 drivers per page)
- Search by driver name

### 🧑 Driver Details
Each driver profile includes:
- Full name
- Date of birth
- Driver number
- Nationality
- Career history
- Complete race results throughout their career
- Ability to filter race results by season

---

## 🏎️ Teams

### 📊 Statistics
- Total teams
- Nationalities
- Active teams

### 📋 Team List
- Paginated list (20 teams per page)
- Search by team name

### 🧾 Team Details
- Relevant information about each team

---

### 🎥 Video Section

https://github.com/user-attachments/assets/2e295fb5-b913-4fac-a2e8-75bcbc230510

<br>

# Future developments
- [x] include the date and time for all races (before 2018 is not available)
- [ ] fix the timezone for all races
