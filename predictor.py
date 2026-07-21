import math
import streamlit as st

# --- APPLICATION WEB PAGE TITLE CONFIG ---
st.set_page_config(
    page_title="Pro Football Predictor Engine",
    page_icon="⚽",
    layout="centered"
)

# --- BROAD COMPREHENSIVE TEAM DATABASE (WORLD RANKINGS TIERING) ---
TEAM_DATABASE = {
    "Spain": {
        "attack": 3.8, "defense": 0.5, "tier": "Elite",
        "formation": "4-3-3 Attacking", "tactic": "Tiki-Taka (Dominant Ball Possession & Rapid Passing)",
        "stars": ["Lamine Yamal", "Nico Williams", "Rodri", "Pau Cubarsí"]
    },
    "Argentina": {
        "attack": 3.5, "defense": 0.6, "tier": "Elite",
        "formation": "4-3-3 Holding", "tactic": "High Counter-Pressing & Quick Central Transition",
        "stars": ["Lionel Messi", "Lautaro Martínez", "Julian Álvarez", "Alexis Mac Allister"]
    },
    "France": {
        "attack": 3.4, "defense": 0.6, "tier": "Elite",
        "formation": "4-2-3-1", "tactic": "Explosive Wing Paces & Highly Rigid Central Low-Block",
        "stars": ["Kylian Mbappé", "Antoine Griezmann", "William Saliba", "Eduardo Camavinga"]
    },
    "England": {
        "attack": 3.3, "defense": 0.7, "tier": "Elite",
        "formation": "4-2-3-1", "tactic": "Patient Tactical Build-up & Attacking Half-Space Overloads",
        "stars": ["Jude Bellingham", "Harry Kane", "Bukayo Saka", "Phil Foden"]
    },
    "Brazil": {
        "attack": 3.2, "defense": 0.7, "tier": "Strong",
        "formation": "4-2-3-1", "tactic": "Samba Flair (Creative Overloads & Wing Isolation ISO)",
        "stars": ["Vinícius Júnior", "Rodrygo", "Bruno Guimarães", "Marquinhos"]
    },
    "Germany": {
        "attack": 3.0, "defense": 0.9, "tier": "Strong",
        "formation": "4-2-3-1", "tactic": "Heavy Vertical Overload & Aggressive Gegenpressing",
        "stars": ["Jamal Musiala", "Florian Wirtz", "Kai Havertz", "Antonio Rüdiger"]
    },
    "Japan": {
        "attack": 2.8, "defense": 0.8, "tier": "Strong",
        "formation": "3-4-2-1", "tactic": "Fast Fluid Breaks & Highly Disciplined Mid-Block Squeeze",
        "stars": ["Kaoru Mitoma", "Takefusa Kubo", "Wataru Endo", "Takumi Minamino"]
    },
    "Morocco": {
        "attack": 2.7, "defense": 0.9, "tier": "Strong",
        "formation": "4-3-3", "tactic": "Elite Defensive Containment & Lightning Counter Attacks",
        "stars": ["Achraf Hakimi", "Brahim Díaz", "Sofyan Amrabat", "Yassine Bounou"]
    },
    "Saudi Arabia": {
        "attack": 2.1, "defense": 1.2, "tier": "Competitive",
        "formation": "5-3-2", "tactic": "Aggressive Defending Offside Trap & Direct Long-Ball Delivery",
        "stars": ["Salem Al-Dawsari", "Firas Al-Buraikan", "Saud Abdulhamid", "Sultan Al-Ghannam"]
    },
    "India": {
        "attack": 1.4, "defense": 1.6, "tier": "Developing",
        "formation": "4-2-3-1", "tactic": "Wing-Focused Cross Inputs & Compact Central Midfield Line",
        "stars": ["Lallianzuala Chhangte", "Manvir Singh", "Anirudh Thapa", "Gurpreet Singh Sandhu"]
    },
    "Pakistan": {
        "attack": 1.2, "defense": 1.8, "tier": "Developing",
        "formation": "4-4-2 Compact", "tactic": "Low Defensive Structural Block & Breakout Counter Sprints",
        "stars": ["Otis Khan", "Esa Suliman", "Harun Hamid", "Yousuf Butt"]
    }
}

FORM_MODIFIERS = {
    "Peak Match Form (Winning Streak)": 1.4,
    "Good Match Form (Mostly Wins)": 1.1,
    "Average Match Form (Mixed Results)": 1.0,
    "Poor Match Form (Struggling to Score)": 0.7
}

# --- POISSON MATH ENGAGEMENT ENGINE ---
def calculate_poisson(actual, expected):
    if expected <= 0:
        return 0.0
    return (math.exp(-expected) * (expected**actual)) / math.factorial(actual)

def process_match_odds(home, away, home_form, away_form, stadium_adv):
    h_base = TEAM_DATABASE[home]
    a_base = TEAM_DATABASE[away]
    
    h_mod = FORM_MODIFIERS[home_form]
    a_mod = FORM_MODIFIERS[away_form]
    
    stadium_bonus = 0.35 if stadium_adv else 0.0
    
    # Calculate expected final goals space values
    home_xg = max(0.15, (h_base["attack"] / a_base["defense"]) * h_mod + stadium_bonus)
    away_xg = max(0.15, (a_base["attack"] / h_base["defense"]) * a_mod)
    
    goals_range = 6
    h_distribution = [calculate_poisson(g, home_xg) for g in range(goals_range + 1)]
    a_distribution = [calculate_poisson(g, away_xg) for g in range(goals_range + 1)]
    
    h_win, a_win, tie = 0.0, 0.0, 0.0
    top_score_prob = -1.0
    final_h_goals, final_a_goals = 0, 0
    
    for h_goals in range(goals_range + 1):
        for a_goals in range(goals_range + 1):
            match_prob = h_distribution[h_goals] * a_distribution[a_goals]
            
            if h_goals > a_goals:
                h_win += match_prob
            elif a_goals > h_goals:
                a_win += match_prob
            else:
                tie += match_prob
                
            if match_prob > top_score_prob:
                top_score_prob = match_prob
                final_h_goals, final_a_goals = h_goals, a_goals
                
    total_space = h_win + a_win + tie
    return {
        "home_percent": (h_win / total_space) * 100,
        "draw_percent": (tie / total_space) * 100,
        "away_percent": (a_win / total_space) * 100,
        "home_xg": home_xg,
        "away_xg": away_xg,
        "predicted_scoreline": f"{final_h_goals} - {final_a_goals}"
    }

# --- APPLICATION INTERFACE LAYOUT DISPLAY ---
st.title("⚽ Pro Football Predictor Engine")
st.markdown("Advanced match simulator incorporating tactical formations, star player databases, and underdog modifiers.")
st.divider()

team_list = list(TEAM_DATABASE.keys())
form_list = list(FORM_MODIFIERS.keys())

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏠 Home Setup")
    home_team = st.selectbox("Select Home Squad:", team_list, index=10) # Defaults directly to Pakistan
    home_form = st.selectbox("Home Current Condition:", form_list, index=2)
    
    h_info = TEAM_DATABASE[home_team]
    st.markdown(f"**Formation Grid:** `{h_info['formation']}`")
    st.markdown(f"**Tactical Blueprint:** *{h_info['tactic']}*")
    st.markdown(f"**Star Roster Profiles:** {', '.join(h_info['stars'])}")

with col2:
    st.subheader("✈️ Away Setup")
    away_team = st.selectbox("Select Away Squad:", team_list, index=0) # Defaults directly to Spain
    away_form = st.selectbox("Away Current Condition:", form_list, index=2)
    
    a_info = TEAM_DATABASE[away_team]
    st.markdown(f"**Formation Grid:** `{a_info['formation']}`")
    st.markdown(f"**Tactical Blueprint:** *{a_info['tactic']}*")
    st.markdown(f"**Star Roster Profiles:** {', '.join(a_info['stars'])}")

st.divider()

# --- AUTOMATED UNDERDOG DESIGNATION ENGINE ---
# Evaluates total mathematical strength differences between the selected configurations
h_strength = (TEAM_DATABASE[home_team]["attack"] / TEAM_DATABASE[away_team]["defense"]) * FORM_MODIFIERS[home_form]
a_strength = (TEAM_DATABASE[away_team]["attack"] / TEAM_DATABASE[home_team]["defense"]) * FORM_MODIFIERS[away_form]

if abs(h_strength - a_strength) < 0.25:
    st.warning("⚖️ Match Assessment: **Evenly Balanced Fixture**. No clear tactical underdog labeled.")
elif h_strength < a_strength:
    st.error(f"⭐ Match Assessment: **{home_team} is the Underdog** in this fixture setup! A win would score a classic football upset.")
else:
    st.error(f"⭐ Match Assessment: **{away_team} is the Underdog** in this fixture setup! A win would score a classic football upset.")

home_adv_toggle = st.checkbox("🏟️ Apply Stadium Home Crowds Advantage Coefficient", value=True)
st.write("")

# Action Execution Trigger
run_prediction = st.button("🚀 Run Simulator Analytics", use_container_width=True)

if run_prediction:
    if home_team == away_team:
        st.error("Validation Halt: Please specify two different national squads to calculate simulations.")
    else:
        results = process_match_odds(home_team, away_team, home_form, away_form, home_adv_toggle)
        
        st.subheader("📊 Modeled Outcome Probability Spectrum")
        
        st.write(f"**{home_team} Win Expectancy:** {results['home_percent']:.1f}%")
        st.progress(int(results['home_percent']))
        
        st.write(f"**Draw Probability Space:** {results['draw_percent']:.1f}%")
        st.progress(int(results['draw_percent']))
        
        st.write(f"**{away_team} Win Expectancy:** {results['away_percent']:.1f}%")
        st.progress(int(results['away_percent']))
        
        st.divider()
        st.subheader("🎯 Primary Prediction Metrics Dashboard")
        m1, m2, m3 = st.columns(3)
        
        with m1:
            if results['home_percent'] > results['away_percent'] and results['home_percent'] > results['draw_percent']:
                winner_tag = f"{home_team} Win"
            elif results['away_percent'] > results['home_percent'] and results['away_percent'] > results['draw_percent']:
                winner_tag = f"{away_team} Win"
            else:
                winner_tag = "Draw Projected"
            st.metric("Projected Outcome", winner_tag)
            
        with m2:
            st.metric("Expected Goals Variance (xG)", f"{results['home_xg']:.2f} vs {results['away_xg']:.2f}")
            
        with m3:
            st.metric("Most Likely Full-Time Score", results['predicted_scoreline'])
