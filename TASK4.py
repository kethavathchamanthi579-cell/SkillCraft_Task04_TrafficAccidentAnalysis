import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium

# -----------------------------------
# Load Dataset (Smaller Sample for Faster Execution)
# -----------------------------------

print("Loading dataset...")

df = pd.read_csv(
    "US_Accidents_March23.csv",
    nrows=50000
)

print("Dataset Loaded Successfully!\n")

# -----------------------------------
# Display Basic Information
# -----------------------------------

print("First 5 Rows:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

# -----------------------------------
# Data Cleaning
# -----------------------------------

important_columns = [
    'Weather_Condition',
    'Start_Time',
    'Start_Lat',
    'Start_Lng'
]

df = df.dropna(subset=important_columns)

print("\nDataset Shape After Cleaning:")
print(df.shape)

# -----------------------------------
# Convert Date and Time
# -----------------------------------

df['Start_Time'] = pd.to_datetime(
    df['Start_Time'],
    format='mixed'
)

df['Hour'] = df['Start_Time'].dt.hour

# -----------------------------------
# Weather Condition Analysis
# -----------------------------------

print("\nGenerating Weather Graph...")

plt.figure(figsize=(12,6))

df['Weather_Condition'].value_counts().head(10).plot(
    kind='bar'
)

plt.title("Top 10 Weather Conditions During Accidents")
plt.xlabel("Weather Condition")
plt.ylabel("Accident Count")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("accidents_by_weather.png")

plt.close()

print("accidents_by_weather.png generated")

# -----------------------------------
# Time Analysis
# -----------------------------------

print("\nGenerating Time Analysis Graph...")

plt.figure(figsize=(12,6))

sns.countplot(x='Hour', data=df)

plt.title("Accidents by Hour")
plt.xlabel("Hour")
plt.ylabel("Accident Count")

plt.tight_layout()

plt.savefig("accidents_by_time.png")

plt.close()

print("accidents_by_time.png generated")

# -----------------------------------
# Severity Analysis
# -----------------------------------

if 'Severity' in df.columns:

    print("\nGenerating Severity Graph...")

    plt.figure(figsize=(8,5))

    sns.countplot(x='Severity', data=df)

    plt.title("Accident Severity Distribution")
    plt.xlabel("Severity")
    plt.ylabel("Count")

    plt.tight_layout()

    plt.savefig("accident_severity.png")

    plt.close()

    print("accident_severity.png generated")

# -----------------------------------
# Hotspot Map
# -----------------------------------

print("\nGenerating Hotspot Map...")

sample_df = df.head(200)

map_center = [
    sample_df['Start_Lat'].mean(),
    sample_df['Start_Lng'].mean()
]

accident_map = folium.Map(
    location=map_center,
    zoom_start=4
)

for index, row in sample_df.iterrows():

    folium.CircleMarker(
        location=[row['Start_Lat'], row['Start_Lng']],
        radius=3,
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(accident_map)

accident_map.save("hotspot_map.html")

print("hotspot_map.html generated")

# -----------------------------------
# Summary File
# -----------------------------------

print("\nGenerating Summary File...")

with open("summary.txt", "w") as file:

    file.write("Traffic Accident Analysis Summary\n")
    file.write("----------------------------------\n\n")

    file.write(f"Total Records: {df.shape[0]}\n\n")

    file.write("Top Weather Conditions:\n")
    file.write(
        str(
            df['Weather_Condition']
            .value_counts()
            .head(5)
        )
    )

print("summary.txt generated")

# -----------------------------------
# Completion Message
# -----------------------------------

print("\nAnalysis Completed Successfully!")

print("\nGenerated Files:")
print("1. accidents_by_weather.png")
print("2. accidents_by_time.png")
print("3. accident_severity.png")
print("4. hotspot_map.html")
print("5. summary.txt")