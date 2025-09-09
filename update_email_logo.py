"""Quick script to update email templates with logo URL"""
import os

# First, upload your logo to one of these services:
# 1. https://imgbb.com/ (free, no account needed)
# 2. https://imgur.com/upload
# 3. Your website: upload to agentcommissiontracker.com

# After uploading, you'll get a direct image URL like:
# https://i.ibb.co/XXXXXX/your-logo.png

# Then run this command in your terminal:
print("""
After uploading your logo, add this to your Render webhook environment:

LOGO_URL=https://your-actual-logo-url.png

For now, you can use a placeholder service that generates a logo:
LOGO_URL=https://via.placeholder.com/200x80/4CAF50/FFFFFF?text=Agent+Commission+Tracker
""")

# Alternative: If you want to host it on GitHub:
print("""
Or upload to your GitHub repo:
1. Add the logo to your repo's 'Logo' folder  
2. Commit and push
3. Go to the file on GitHub
4. Click 'Raw'
5. Use that URL as your LOGO_URL
""")