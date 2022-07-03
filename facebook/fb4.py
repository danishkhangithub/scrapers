# packages
import facebook
import json

def main():
  token = 'EAACdV5eYR0gBACE1CoGbVeejzvKKDXZBs9IV6NiRzuZCZAUvJTG9sbmgQ64Ti3u0AC51uLxVYOtTogJylcnyIhKLIsZBpQHgDGUABmEHlc3ZBZA8YZAudRcnl8WjdgBaPDM0gKrlmZAqThB1EKieeswZAMiKZCJglnM8qTpcDQw3G3EGSYEogq8zOFvYARzNQVGHFPfkB7cBJXNj4wnlZApdKgrcn4cwZCbXjCxor1zmcmVZBaCxZBUvZBo2D52'
  graph = facebook.GraphAPI(token)
  page_name = input("Enter a page name: ")
  
  # list of required fields
  fields = ['id','name','about','likes','link','band_members']
  
  fields = ','.join(fields)
  
  pages = graph.get_object(page_name, fields = fields)
  
  print(json.dumps(page, indent = 4))
  
  
if __name__ == '__main__':
   main()  
  

