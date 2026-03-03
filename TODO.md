# Pokemon Details Card Component - Implementation Plan

## Steps to Complete:

### 1. Create the Reusable Component
- [x] Create `quickserve/pokemon/templates/pokemon/components/pokemon_detail_card.html`

  - TGC-style card layout with type-based gradients
  - Pokemon name in ALL CAPS, BOLD at top left
  - Rainbow star icon (only if shiny) at top left
  - Type.png image at top right
  - Pokemon sprite from showdown directory (.gif) in center
  - "Pokemon Details" section with Rarity and Pokedex Entry
  - Context-aware buttons (Add to Team / Remove from Team / Back)

### 2. Update Pokedex Template
- [x] Modify `quickserve/pokemon/templates/pokemon/pokedex.html`

  - Replace direct navigation with modal using the new component
  - Pass appropriate context variables to the component

### 3. Update My Team Template
- [x] Modify `quickserve/pokemon/templates/pokemon/my_team_updated.html`

  - Update modal for available Pokemon section to use new component
  - Update modal for active team section to use new component
  - Ensure proper button functionality (Add vs Remove)

### 4. Testing
- [x] Test component in Pokedex page
- [x] Test component in My Team page (available section)
- [x] Test component in My Team page (active team section)
- [x] Verify Add to Team functionality works
- [x] Verify Remove from Team functionality works


---

## Additional Completed Tasks:

### Hatch 5 Eggs Feature
- [x] Create `hatch_5_result.html` template with 3-phase animation
- [x] Add `hatch_5_eggs` view to `views.py` for batch processing
- [x] Add URL pattern for `hatch_5_eggs` in `urls.py`
- [x] Add "Hatch 5 Eggs" button to dashboard (shown when user has 5+ eggs)
- [x] Animation: 5 eggs wobble simultaneously with staggered timing
- [x] Flash effects based on highest rarity/shiny status (white/gold/rainbow)
- [x] Shiny burst effect for shiny Pokemon
- [x] 5 Pokemon sprites appear horizontally after eggs fade
- [x] 5 TGC-style result cards with type gradients, rarity glows, shiny indicators
- [x] Summary section showing total XP, shiny count, team additions, coins earned

### Remove My Team from Navigation
- [x] Remove "My Team" link from `pokedex.html` navbar
- [x] Remove "My Team" link from `profile.html` navbar
- [x] Remove "My Team" link from `shop.html` navbar
- [x] Remove "My Team" link from `inventory.html` navbar
- [x] Remove "My Team" link from `achievements.html` navbar
