import os
import re
import json
import folium

data_dir = 'data/'

def main():
    test_id = None
    coords_raw = []

    min_time = None
    max_time = None

    for f in os.listdir(data_dir):
        if not os.path.isfile(os.path.join(data_dir, f)):
            continue
        f_regex = re.search(r"muni_(\d+).json", f)
        if not f_regex:
            continue

        num = int(f_regex.group(1))
        if not min_time or not max_time:
            min_time = num
            max_time = num
        elif num < min_time:
            min_time = num
        elif num > max_time:
            max_time = num

        with open(f'{data_dir}{f}', 'r') as f_in:
            data = json.loads(''.join(f_in.readlines()))

            if not test_id:
                test_id = data[3]['id']
            
            for d in data:
                if d['id'] != test_id:
                    continue
                coords_raw.append({
                    'n': num,
                    'c': (d['lat'], d['lon'])
                })

    coords_raw.sort(key=lambda x: x['n'])

    coords = [coords_raw[0]]
    for i in range(1, len(coords_raw)):
        if coords_raw[i]['c'] != coords_raw[i - 1]['c']:
            coords.append(coords_raw[i])

    print(len(coords))

    m = folium.Map(location=(37.77493, -122.44942), zoom_start=13.5)

    # Add markers for each coordinate
    grad_color_a = (255, 0, 0)
    grad_color_b = (0, 255, 0)
    def get_color_at_t(t):
        return '#%02x%02x%02x' % (
            int(grad_color_a[0] + (grad_color_b[0] - grad_color_a[0]) * t),
            int(grad_color_a[1] + (grad_color_b[1] - grad_color_a[1]) * t),
            int(grad_color_a[2] + (grad_color_b[2] - grad_color_a[2]) * t),
        )
    for coord in coords:
        t = (coord['n'] - min_time) / (max_time - min_time)
        folium.CircleMarker(location=coord['c'], radius=3, color=get_color_at_t(t)).add_to(m)

    # Save the map to an HTML file
    m.save('map.html')


if __name__ == "__main__":
    main()
