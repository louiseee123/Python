# Starter Selection Improvement Plan

## Tasks:
- [ ] Update `quickserve/pokemon/templates/pokemon/starter_selection.html`
  - Transform from grid layout to a horizontal carousel
  - Display showdown (.gif) sprites for each Pokemon
  - Pokemon sprite should hover above a pokeball
  - Show "Choose" button only for the focused Pokemon
  - Add carousel navigation (arrows)
  
- [ ] Update `quickserve/pokemon/views.py`
  - Remove auto-unlock of all starters in `signup()` function
  - Remove auto-unlock of all starters in `create_trainer()` function
  - New accounts will only get their chosen starter
