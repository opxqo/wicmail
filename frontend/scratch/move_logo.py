import re

file_path = '/Users/luotao/Code/tools/wicmail/frontend/src/views/landing/index.vue'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Locate and extract the school brand div containing the SVG (and clean it up to use SchoolLogo)
# We will find the footer-school-brand div, extract it, and replace it at its original location with empty space.
pattern_school_brand = r'(<!-- 学校合作/关联标识 -->\s*<div class="footer-school-brand">.*?</div>)'
match = re.search(pattern_school_brand, content, re.DOTALL)
if not match:
    print("Error: Could not locate school logo SVG section.")
    exit(1)

# Remove the school brand section from its original position
content = content.replace(match.group(1), "")

# 2. Locate footer-logo-link block
pattern_logo_link = r'(<router-link to="/" class="footer-logo-link">.*?</router-link>)'
match_logo = re.search(pattern_logo_link, content, re.DOTALL)
if not match_logo:
    print("Error: Could not locate footer logo link.")
    exit(1)

# 3. Create the new combined brand header layout using the reusable SchoolLogo component
new_header = f"""<div class="footer-brand-header">
              {match_logo.group(1)}
              <div class="footer-logo-divider" />
              <div class="footer-school-brand">
                <SchoolLogo class="footer-school-logo" />
              </div>
            </div>"""

content = content.replace(match_logo.group(1), new_header)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Success: Layout updated successfully.")
