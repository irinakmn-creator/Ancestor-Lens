import os
import re

def add_link_to_explore_more(filename, link_html):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Try to find the closing </ul> in the "Explore More" section
    if '<h2>Explore More' in content or '<h2>Explore More' in content:
        # insert before the closing </ul> of the Explore More section
        # This regex looks for </ul> after Explore More
        pattern = re.compile(r'(<h2>Explore More.*?)(</ul>)', re.DOTALL | re.IGNORECASE)
        new_content = pattern.sub(r'\1    ' + link_html + '\n                        \2', content)
        if new_content != content:
            with open(filename, 'w') as f:
                f.write(new_content)
            print(f"Updated {filename}")
        else:
            print(f"Could not find exact injection point in {filename}")
    else:
        print(f"No Explore More section in {filename}")

# Links
link_accuracy = '<li>👉 <a href="blog-how-accurate-ai-ethnicity-test.html">Learn how accurate AI ethnicity tests are and what results mean</a></li>'
link_photo = '<li>👉 <a href="blog-best-photo-ai-ancestry-test.html">Read our photo tips for a clearer result and best face analysis</a></li>'
link_apps = '<li>👉 <a href="blog-best-ancestry-apps-without-dna-test.html">Compare ancestry apps without a DNA test to choose an ancestry app</a></li>'

# 1. Accuracy
for f in ['blog-ai-face-ethnicity-test.html', 'blog-ethnicity-detection.html', 'blog-ai-vs-dna.html', 'blog-what-nationality-i-look-like.html', 'blog-what-country-do-my-facial-features-come-from.html']:
    add_link_to_explore_more(f, link_accuracy)

# 2. Photo
for f in ['blog-historical-twin-ai-app.html', 'blog-ancestor-face-app.html', 'blog-ai-face-ethnicity-test.html', 'blog-what-nationality-look-like.html']:
    add_link_to_explore_more(f, link_photo)

# 3. Apps
for f in ['blog-origins.html', 'blog-ancestry-without-dna.html', 'blog-heritage-no-dna.html', 'blog-dna-vs-ai.html']:
    add_link_to_explore_more(f, link_apps)

