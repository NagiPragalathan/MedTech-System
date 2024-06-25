import pandas as pd
import folium
from folium import plugins
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import random

# Updated data for cities and main places in Tamil Nadu
data = {
    'City': [
        'Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem', 'Tirunelveli', 
        'Vellore', 'Erode', 'Tiruppur', 'Thanjavur', 'Dindigul', 'Theni', 'Virudhunagar', 
        'Nagapattinam', 'Kanyakumari', 'Tiruvannamalai', 'Cuddalore', 'Kanchipuram', 
        'Thoothukudi', 'Nagercoil'
    ],
    'Latitude': [
        13.0827, 11.0168, 9.9252, 10.7905, 11.6643, 8.7139, 12.9165, 11.3410, 11.1085, 
        10.7870, 10.3673, 10.0104, 9.5877, 10.7649, 8.0883, 12.2253, 11.7447, 12.8342, 
        8.7642, 8.1729
    ],
    'Longitude': [
        80.2707, 76.9558, 78.1198, 78.7047, 78.1460, 77.7567, 79.1325, 77.7282, 77.3411, 
        79.1378, 77.9803, 77.4807, 77.9575, 79.8431, 77.5385, 79.0730, 79.7684, 79.7036, 
        78.1348, 77.4316
    ],
    'Patients': [random.randint(100, 1000) for _ in range(20)],
    'Hospitals': [random.randint(10, 50) for _ in range(20)],
    'Doctors': [random.randint(50, 300) for _ in range(20)],
    'MainPlaces': [
        ['Marina Beach', 'Fort St. George', 'Kapaleeshwarar Temple'],
        ['Dhyanalinga', 'VOC Park and Zoo', 'Kovai Kutralam Falls'],
        ['Meenakshi Amman Temple', 'Thirumalai Nayakar Mahal', 'Gandhi Memorial Museum'],
        ['Sri Ranganathaswamy Temple', 'Rockfort Temple', 'Jambukeswarar Temple'],
        ['Yercaud', 'Kottai Mariamman Temple', 'Sugavaneswarar Temple'],
        ['Nellaiappar Temple', 'Papanasam', 'Mundanthurai Tiger Reserve'],
        ['Vellore Fort', 'Jalakandeswarar Temple', 'Amirthi Zoological Park'],
        ['Bannari Amman Temple', 'Bhavani Sagar Dam', 'Vellode Bird Sanctuary'],
        ['Avinashi Temple', 'Tirupur Kumaran Memorial Statue', 'Noyyal River'],
        ['Brihadeeswarar Temple', 'Thanjavur Royal Palace', 'Saraswathi Mahal Library'],
        ['Dindigul Fort', 'Sirumalai Hills', 'St. Joseph Church'],
        ['Vaigai Dam', 'Suruli Falls', 'Meghamalai'],
        ['Ayyanar Falls', 'Virudhunagar Fort', 'Kamarajar Memorial House'],
        ['Nagore Dargah', 'Sikkal Singaravelar Temple', 'Velankanni Church'],
        ['Vivekananda Rock Memorial', 'Thiruvalluvar Statue', 'Kanyakumari Beach'],
        ['Arunachaleswarar Temple', 'Sathanur Dam', 'Gingee Fort'],
        ['Silver Beach', 'Pichavaram Mangrove Forest', 'Padaleeswarar Temple'],
        ['Kamakshi Amman Temple', 'Ekambareswarar Temple', 'Kanchi Kudil'],
        ['Our Lady of Snows Basilica', 'Ettayapuram Palace', 'Panchalankurichi Fort'],
        ['Nagaraja Temple', 'Vattakottai Fort', 'Thirparappu Falls']
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Initialize the map centered around Tamil Nadu
tamil_nadu_coords = [11.1271, 78.6569]
map_tamil_nadu = folium.Map(location=tamil_nadu_coords, zoom_start=7)

# Function to add pie charts to the map
def add_pie_charts(map_obj, data):
    for _, row in data.iterrows():
        fig, ax = plt.subplots()
        sizes = [row['Patients'], row['Hospitals'], row['Doctors']]
        labels = ['Patients', 'Hospitals', 'Doctors']
        colors = ['#ff9999','#66b3ff','#99ff99']
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title(f"{row['City']}")
        
        # Save it to a temporary file
        tmpfile = BytesIO()
        plt.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        html = '<img src="data:image/png;base64,{}">'.format(encoded)
        iframe = folium.IFrame(html, width=300, height=300)
        popup = folium.Popup(iframe, max_width=650)
        
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=popup,
            tooltip=row['City'],
            icon=folium.Icon(color='blue')
        ).add_to(map_obj)

# Function to add main places to the map
def add_main_places(map_obj, data):
    for _, row in data.iterrows():
        for place in row['MainPlaces']:
            folium.Marker(
                location=[row['Latitude'] + random.uniform(-0.05, 0.05), row['Longitude'] + random.uniform(-0.05, 0.05)],
                popup=f"City: {row['City']}<br>Main Place: {place}",
                tooltip=f"{row['City']} - {place}",
                icon=folium.Icon(color='green')
            ).add_to(map_obj)

# Add pie charts and main places to the map
add_pie_charts(map_tamil_nadu, df)
add_main_places(map_tamil_nadu, df)

# Save the map to an HTML file
map_tamil_nadu.save('tamil_nadu_disease_map_with_pie_charts.html')

print("Map has been created and saved as 'tamil_nadu_disease_map_with_pie_charts.html'.")
