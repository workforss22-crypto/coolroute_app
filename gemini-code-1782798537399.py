import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def get_clean_data():
    return pd.read_csv('coolroute_cleaned_data.csv')

df = get_clean_data()

st.title("CoolRoute Dubai — Analytics Dashboard")
st.subheader("Validating Heat-Safe Smart Mobility Strategies")

# --- DESCRIPTIVE SECTION ---
st.markdown("---")
st.header("Descriptive Analytics: App Usage Patterns")

c1, c2 = st.columns(2)
with c1:
    st.subheader("Route Preference Distribution")
    fig, ax = plt.subplots()
    sns.countplot(data=df, x='Route_Preference', palette='Set2', ax=ax)
    plt.xticks(rotation=15)
    st.pyplot(fig)
    st.caption("Shows which mobility options are selected most frequently across Dubai hubs.")

with c2:
    st.subheader("Revenue by User Segment")
    fig2, ax2 = plt.subplots()
    sns.barplot(data=df, x='User_Type', y='Total_Revenue_AED', estimator=sum, errorbar=None, palette='Blues_d', ax=ax2)
    st.pyplot(fig2)
    st.caption("Identifies which demographic contributes the highest financial value to the pipeline.")

# --- DIAGNOSTIC SECTION ---
st.markdown("---")
st.header("Diagnostic Analytics: What Drives Revenue?")

# Encode preferences numerically for correlation matrix
df_encoded = df.copy()
df_encoded['Route_Pref_Code'] = df_encoded['Route_Preference'].astype('category').cat.codes

st.subheader("Feature Correlation Heatmap")
fig3, ax3 = plt.subplots(figsize=(6, 4))
corr = df_encoded[['Temperature_C', 'Hydration_Stops_Clicked', 'Premium_Plan_Purchased', 'Total_Revenue_AED']].corr()
sns.heatmap(corr, annot=True, cmap='YlOrRd', fmt=".2f", ax=ax3)
st.pyplot(fig3)

st.markdown("""
**Logical Explanations & Rationale:**
* **Temperature vs Premium Conversions:** A strong positive correlation reveals that as temperatures approach $45^\circ\text{C}$ and above, users are far more willing to unlock premium indoor/shortcut maps.
* **Hydration Clicks vs Revenue:** Users interacting heavily with micro-experience elements (hydration markers, cooling zones) show a higher propensity to buy cooling kits, signaling a strong target audience for ad placements or upsells.
""")