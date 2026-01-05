import streamlit as st
import datetime

# --- CONFIGURATION & DATA ---
# This dictionary holds your entire workout schedule. 
# Changing the text here changes what appears in the app.
schedule = {
    "Monday": {
        "focus": "Lower Body Power & Strength",
        "type": "Lifting",
        "exercises": [
            {"name": "Box Jumps (Primer)", "sets": "3", "reps": "3", "note": "Step down, do not jump down. Max height."},
            {"name": "Trap Bar Deadlift (Main)", "sets": "3", "reps": "5", "note": "RPE 8. Leave 1-2 reps in tank."},
            {"name": "Reverse Lunges", "sets": "3", "reps": "8/leg", "note": "Protects back, crushes glutes."},
            {"name": "Romanian Deadlifts", "sets": "3", "reps": "10-12", "note": "3-second eccentric (lowering)."},
            {"name": "Sled Push Finisher", "sets": "5 rounds", "reps": "20 yards", "note": "60s rest between rounds."}
        ]
    },
    "Tuesday": {
        "focus": "Zone 2 Engine Building",
        "type": "Cardio",
        "exercises": [
            {"name": "Rucking / Cycling / Incline Walk", "sets": "1", "reps": "45-60 min", "note": "Strict Zone 2. Nasal breathing only!"}
        ]
    },
    "Wednesday": {
        "focus": "Upper Body Strength (V-Taper)",
        "type": "Lifting",
        "exercises": [
            {"name": "Med Ball Slams", "sets": "3", "reps": "5", "note": "Throw it through the floor."},
            {"name": "Overhead Press", "sets": "3", "reps": "5", "note": "Engage glutes and core."},
            {"name": "Weighted Pull-Ups", "sets": "3", "reps": "6-8", "note": "Or heavy lat pulldowns."},
            {"name": "Incline DB Bench", "sets": "3", "reps": "8-10", "note": "Safer for shoulders than flat bench."},
            {"name": "Accessory Superset", "sets": "3 rounds", "reps": "15 Face Pulls / 10 Hammer Curls", "note": "For rotator cuff and elbow health."}
        ]
    },
    "Thursday": {
        "focus": "Metabolic Conditioning (HIIT)",
        "type": "Cardio",
        "exercises": [
            {"name": "Rower / Assault Bike / SkiErg", "sets": "15-20 mins", "reps": "30s Work / 30s Rest", "note": "Hydrate well! Zepbound + HIIT can drain you."}
        ]
    },
    "Friday": {
        "focus": "The Hybrid Athlete (Full Body)",
        "type": "Lifting",
        "exercises": [
            {"name": "Farmer's Carries", "sets": "4", "reps": "40 yards", "note": "Walk fast, stand tall."},
            {"name": "Kettlebell Swings", "sets": "4", "reps": "15", "note": "Explosive hip snap."},
            {"name": "Landmine Rotations", "sets": "3", "reps": "10/side", "note": "Vital for rotational power."},
            {"name": "Suitcase Deadlift", "sets": "3", "reps": "8/side", "note": "Fight the urge to lean."},
            {"name": "Pump Work (Optional)", "sets": "10 mins", "reps": "AMRAP", "note": "Arms/Shoulders for aesthetics."}
        ]
    },
    "Saturday": {
        "focus": "Active Recovery",
        "type": "Recovery",
        "exercises": [
            {"name": "Walk / Swim / Yoga", "sets": "1", "reps": "30-60 min", "note": "Foam roll quads and lats. Take off if beaten up."}
        ]
    },
    "Sunday": {
        "focus": "Total Rest",
        "type": "Rest",
        "exercises": []
    }
}

# --- APP LOGIC STARTS HERE ---

st.set_page_config(page_title="Peak Performance Tracker", page_icon="💪")

# 1. Sidebar: User Settings
st.sidebar.header("User Settings")
# We calculate the week number to handle your "Week 5 Deload" logic
current_week = st.sidebar.number_input("Current Training Week", min_value=1, value=1)
user_weight = st.sidebar.number_input("Your Bodyweight (lbs)", value=200)

# Check for Deload Logic
is_deload = False
if current_week % 5 == 0:
    is_deload = True
    st.sidebar.warning("⚠ DELOAD WEEK ACTIVE: Weights reduced by 40%. Focus on technique.")
else:
    st.sidebar.success(f"Week {current_week}: PUSH WEEK. Try to add weight.")

# 2. Determine Day of Week
# We let you override the day in the sidebar for testing purposes
days_list = list(schedule.keys())
today_name = datetime.datetime.now().strftime("%A")
selected_day = st.sidebar.selectbox("Select Day", days_list, index=days_list.index(today_name) if today_name in days_list else 0)

# 3. Main Header
routine = schedule[selected_day]
st.title(f"📅 {selected_day}: {routine['focus']}")

# 4. Display Readiness/Notes based on Stack
if routine['type'] == "Cardio" or routine['type'] == "Lifting":
    with st.expander("💊 Stack & Nutrition Reminder"):
        st.write("- **Tirzepatide:** Ensure you have eaten enough protein before training.")
        st.write("- **Hydration:** Add electrolytes, especially for HIIT.")

# 5. THE UNBREAKABLE WARM-UP (Only shows on Lifting Days)
if routine['type'] == "Lifting":
    st.subheader("🔥 The Unbreakable Warm-Up")
    st.info("BPC-157 Primer: Stimulate collagen before loading.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.checkbox("5 Min Cardio (Bike/Walk)")
    with col2:
        st.checkbox("2x45s Wall Sit (Iso)")
    with col3:
        st.checkbox("2x45s Plank (Iso)")
    st.markdown("---")

# 6. The Workout Loop
st.subheader("🏋️ Work Set")

if routine['type'] == "Rest":
    st.write("Enjoy your Sunday. Meal prep for the week. High protein today.")
else:
    for exercise in routine['exercises']:
        # Create a container for each exercise
        with st.container():
            st.markdown(f"### {exercise['name']}")
            
            # Display Sets/Reps
            c1, c2, c3 = st.columns([2, 2, 3])
            c1.write(f"**Sets:** {exercise['sets']}")
            c2.write(f"**Reps:** {exercise['reps']}")
            c3.caption(f"📝 {exercise['note']}")
            
            # INPUT: Track weight used
            # If it's a lifting day, allow weight input
            if routine['type'] == "Lifting":
                weight = st.number_input(f"Weight (lbs) for {exercise['name']}", key=exercise['name'], step=5)
                
                # THE DELOAD MATH LOGIC
                if weight > 0:
                    if is_deload:
                        recommended = weight * 0.6
                        st.write(f"📉 **Deload Target:** You should only lift **{int(recommended)} lbs** today.")
                    else:
                        st.write(f"🚀 **Target:** Lift {weight} lbs with perfect form.")

            st.checkbox(f"Done: {exercise['name']}", key=f"check_{exercise['name']}")
            st.divider()

# 7. HIIT Timer (Only for Thursday)
if selected_day == "Thursday":
    st.subheader("⏱ HIIT Interval Timer")
    st.write("Do 30s Hard / 30s Easy")
    if st.button("Start 30s Timer"):
        import time
        progress_bar = st.progress(0)
        for i in range(30):
            time.sleep(1) # Wait 1 second
            progress_bar.progress((i + 1) / 30)
        st.success("SWITCH INTERVAL!")
