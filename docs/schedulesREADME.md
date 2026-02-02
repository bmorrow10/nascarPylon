# NASCAR Schedule Management

## Quick Start

1. **Edit schedules** in `schedules/*.csv` files
2. **Run converter**: `python convert_schedules.py`
3. **Updated JSON** files will be in `data/` directory

## CSV Format

All schedules follow this format:

```csv
round,raceName,track,location,date,day,startTime,broadcast,distance,laps,isChase
1,Daytona 500,Daytona International Speedway,"Daytona Beach, FL",2026-02-15,Sunday,14:30,FOX,500 mi,200,false
```

### Column Descriptions

- **round**: Race number in the season (1-40)
- **raceName**: Official race name
- **track**: Track name
- **location**: City, State
- **date**: YYYY-MM-DD format
- **day**: Day of week
- **startTime**: 24-hour format (HH:MM)
- **broadcast**: TV network (FOX, FS1, NBC, USA, TNT, Prime, CW)
- **distance**: Race distance with units
- **laps**: Number of laps (0 if TBA)
- **isChase**: `true` for playoff races, `false` for regular season

## Files

### CSV Files (edit these!)
- `schedules/cup.csv` - NASCAR Cup Series
- `schedules/xfinity.csv` - Xfinity Series (O'Reilly)
- `schedules/trucks.csv` - Craftsman Truck Series

### Generated JSON Files (don't edit directly!)
- `data/sched.json` - Cup Series
- `data/schedOR.json` - Xfinity Series
- `data/schedTruck.json` - Truck Series

## Notes

- All times are in **ET (Eastern Time)**
- Chase races start at Southern 500 (typically early September)
- Use `isChase: true` for all playoff races
- All JSON keys use **camelCase** format
- CSV is easier to maintain than JSON directly