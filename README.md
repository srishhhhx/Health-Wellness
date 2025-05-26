# Wellness Score Calculator

Track your daily wellness using a simple and interactive tool. The **Wellness Score Calculator** is a lightweight app that calculates a daily wellness score (0–100) using three metrics: **Sleep Hours**, **Daily Steps**, and **Mood Rating**. It combines rule-based scoring logic with a trained ML model (Random Forest) and displays results in a beautiful interactive dashboard.

![Wellness Dashboard](app/assets/dashboard.png)

---

## Project pipeline

This project merges domain knowledge with machine learning to produce a robust and intuitive scoring system. It starts with synthetic data generation, followed by model training and visualization through a Streamlit dashboard.

---

## Synthetic Dataset Generation

Since real-world wellness datasets with labeled scores are scarce, a synthetic dataset was created based on clearly defined scoring rules:

Inputs Simulated:

- Sleep Hours: 0–12 hours
- Daily Steps: 0–25,000 steps
- Mood Rating: 1–10 scale

Edge Cases Handled:

- Extremely low/high sleep durations (e.g., 0, 2, 12 hrs)
- Step counts near inactivity (e.g., 0–500) and excessive activity
- Mood extremes (1–2 for bad, 9–10 for excellent)
- Combination scenarios (e.g., good mood with low sleep, or high steps with poor mood)

Each synthetic record was scored using a rule-based function (details below) to create labeled training data for the ML model.

Notebook : [Synthetic Data Generation](notebooks/synthetic_data.ipynb)

---

## Scoring Logic

Each input metric contributes to the final score based on predefined weights:

| Metric       | Ideal Range     | Weight   | Logic                                                             |
|--------------|------------------|---------|-------------------------------------------------------------------|
| Sleep Hours  | 7–9 hrs          | 0.40    | Penalized for less than 6 or more than 10 hrs                     |
| Step Count   | >8000 steps      | 0.30    | Scaled linearly up to 25,000 steps                                |
| Mood Rating  | 1–10 scale       | 0.30    | Captures subjective daily emotional state                         |

The final score = weighted average of individual metric scores.  

This distribution is grounded in health science research emphasizing the foundational role of sleep in physical and mental health. Here's why:

1. Sleep Quality Strongly Influences Mood and Physical Recovery
Sleep deprivation negatively impacts:

Emotional regulation and cognitive performance
Physical recovery and immune function
Long-term risks of chronic conditions (e.g., heart disease, diabetes)


[Walker, M. (2017). *Why We Sleep* – Sleep's central role in well-being](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2656292/)
[Harvard Medical School – Sleep and Mental Health](https://www.health.harvard.edu/newsletter_article/sleep-and-mental-health)


2. Physical Activity (Steps) Is Important but Secondary to Recovery
While regular activity is a strong predictor of overall wellness and longevity, its benefits are compromised if recovery (via sleep) is insufficient.

[World Health Organization – Physical Activity Guidelines](https://www.who.int/news-room/fact-sheets/detail/physical-activity)  

3. Mood Reflects but Also Depends on Sleep and Activity
Mood is highly subjective and influenced by both physiological (sleep, exercise) and external factors. While critical, it’s weighted slightly lower due to its variability and dependence on other inputs.

[APA – Sleep and Mood: The Bidirectional Link](https://www.apa.org/news/press/releases/stress/2013/sleep)

Conclusion: The 40-30-30 split ensures that sleep, as a root factor for both emotional and physical health, drives the score more heavily, while steps and mood still contribute substantially to reflect a well-rounded wellness assessment.

Notebook : [WellnessScore_generator](notebooks/WellnessScore_generator.ipynb)

---

## ML Model Training

Using the synthetic dataset with labeled scores, multiple regression models were trained to approximate the rule-based function and allow slight non-linear generalization:

Models Tested:

Linear Regression – fast but too simplistic for non-linear interactions.

Decision Tree Regressor – interpretable but prone to overfitting.

Random Forest Regressor – best generalization, low MSE, handles edge cases well.

Why Random Forest?

Captures feature interactions without manual tuning and performs better on mixed linear/non-linear relationships

The selected Random Forest Regressor is integrated in the dashboard to provide real-time predictions.

Notebook : [Model_training](notebooks/Model_training.ipynb)


## Features

- Interactive Streamlit dashboard
- Instant feedback via real-time wellness score (gauge)
- Slider inputs for:
  - Sleep Hours (0–12 hrs)
  - Daily Steps (0–25,000)
  - Mood Rating (1–10)
- Personalized health tips and motivation
- All processing is local — no sensitive data collected

---

## Hybrid Approach 

Combining rule-based logic with a machine learning model offers the best of both worlds. The rule-based system ensures interpretability, making the scoring process transparent and easy to trust. At the same time, the ML model adds flexibility, capturing subtle patterns and variations that rigid rules may miss. This hybrid approach also enhances robustness, allowing the model to handle edge cases and overlapping input conditions more smoothly. Most importantly, the rule-based framework enables data bootstrapping by generating a large volume of labeled synthetic data, which is critical for effectively training the initial ML model without requiring real-world labels.

--- 

## Running the App Locally

Prerequisites:


Python 3.8+

pip


Steps:

### 1. Clone the Repo

git clone https://github.com/srishhhhx/Health-Wellness.git

cd Health-Wellness/app

### 2. Create a Virtual Environment


python -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3. Install Required Packages


pip install -r requirements.txt

### 4. Run the Streamlit App


streamlit run app.py
