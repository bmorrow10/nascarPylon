# NASCAR API Reference & Resources

Comprehensive reference for accessing NASCAR live race data.

## Primary Data Source: feed.nascar.com

NASCAR provides free, public JSON endpoints during live races.

### Known Endpoints

Based on research from multiple community projects:

#### 1. **Live Feed** (Main endpoint)
```
https://feed.nascar.com/live-feed.json
```
**Returns:** Current race positions, intervals, lap count, flag status

**Key data:**
- Driver positions
- Intervals to leader/next car  
- Current lap / total laps
- Flag status (GREEN/YELLOW/RED)
- Series info

**Usage:** Poll every 5-10 seconds during active race

#### 2. **Flag State**
```
https://feed.nascar.com/flag-state.json
```
**Returns:** Detailed flag history and current status

**Includes:**
- Flag changes throughout race
- Caution reason
- Lap of flag change

#### 3. **Lap Times**
```
https://feed.nascar.com/lap-times.json
```
**Returns:** Lap-by-lap timing data for all drivers

**Includes:**
- Individual lap times
- Best lap
- Last lap
- Average lap speed

#### 4. **Loop Data** (Sector times)
```
https://feed.nascar.com/loop-data.json
```
**Returns:** Driver data from timing loops around track

**Includes:**
- Sector times
- Speed through loops
- Positional changes

#### 5. **Pit Stops**
```
https://feed.nascar.com/pit-stops.json
```
**Returns:** All pit stop data

**Includes:**
- Pit in/out times
- Pit duration
- Adjustments made
- Tire changes

#### 6. **Points** (Live)
```
https://feed.nascar.com/points.json
```
**Returns:** Current race points and stage points

**Includes:**
- Race points earned
- Stage points
- Playoff points

## Community Projects & Documentation

### 1. **ooohfascinating/NascarApi**
- **GitHub:** https://github.com/ooohfascinating/NascarApi
- **Description:** Detailed API documentation with example responses
- **Value:** Has actual JSON structure examples
- **Files to check:**
  - `LiveFeed.MD` - Main live feed documentation
  - `FlagState.MD` - Flag data structure
  - `LapTimes` - Lap timing data
  - `LoopStats` - Loop/sector data

**License:** MIT
**Status:** Active documentation (31 stars)

### 2. **RRoberts4382/rNascar23.Sdk**
- **GitHub:** https://github.com/RRoberts4382/rNascar23.Sdk
- **Description:** C# SDK for NASCAR endpoints
- **Value:** Production-ready API wrapper (in C#)
- **Key features:**
  - Dependency injection ready
  - AutoMapper integration
  - Comprehensive data models

**License:** MIT
**Status:** Last updated 2023 (still relevant)

### 3. **Kevinw14/NascarPylon**
- **GitHub:** https://github.com/Kevinw14/NascarPylon
- **Description:** Another pylon project (check src/ folder)
- **Value:** May have parsing/display code we can reference
- **Status:** To investigate

## Data Structure Notes

### Series IDs
From community projects:
- Cup Series: `1`
- Xfinity Series: `2`  
- Truck Series: `3`

### Race Weekend IDs
NASCAR uses race IDs to identify specific events. These change each week.

**Finding current race ID:**
- Check NASCAR.com race center URL
- Check `weekend-feed.json` (if available)
- Use race list endpoint

## Implementation Strategy

### For Our Python Project

**Phase 1: Basic Live Feed**
```python
import requests

def get_live_feed():
    url = "https://feed.nascar.com/live-feed.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None
```

**Phase 2: Parse to Our Format**
Map NASCAR JSON → our camelCase format for consistency

**Phase 3: Error Handling**
- Handle network errors
- Handle "no active race" (404 or empty data)
- Validate data structure

**Phase 4: Continuous Polling**
- Poll every 5 seconds during race
- Update `lastUpdate` timestamp
- Trigger auto-mode detection

## Testing Plan

### Sunday's Clash (Feb 1, 2026)

1. **Before race (~6pm ET):**
   ```bash
   python testNascarEndpoints.py --save
   ```
   Test all endpoints, save responses

2. **During race:**
   - Verify data structure
   - Check update frequency
   - Note any issues

3. **After race:**
   - Parse saved samples
   - Build production scraper
   - Update data models

## Code We Can Reference (Not Copy)

From these repos, we can look at:

✅ **Data structure/parsing patterns**
- How they map NASCAR JSON to objects
- Field names and types
- Error handling approaches

✅ **API endpoint discovery**
- Which endpoints they found useful
- How they handle race IDs
- Series selection logic

❌ **Do NOT directly copy:**
- Their exact code (licensing respect)
- Their class structures
- Their business logic

Instead: **Learn from their approach, write our own implementation**

## Attribution

When using insights from these projects:

```python
# Inspired by:
# - ooohfascinating/NascarApi (API documentation)
# - RRoberts4382/rNascar23.Sdk (endpoint structure)
# See ACKNOWLEDGMENTS.md for full credits
```

## Next Steps

1. ✅ Test endpoints Sunday during Clash
2. ⏳ Document actual response structure  
3. ⏳ Build Python data models
4. ⏳ Implement parser (NASCAR JSON → our format)
5. ⏳ Add continuous polling
6. ⏳ Integrate with auto-mode detection

## Resources

- **NASCAR API Docs:** https://github.com/ooohfascinating/NascarApi
- **rNascar SDK:** https://github.com/RRoberts4382/rNascar23.Sdk
- **NASCAR Feed Base:** https://feed.nascar.com/
- **Our test script:** `tools/testNascarEndpoints.py`

---

**Last Updated:** February 2026
**Status:** Pre-season testing phase