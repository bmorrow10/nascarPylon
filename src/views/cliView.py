# src/views/cliView.py

class Colors:
    """ANSI color codes for terminal output"""
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


# Track previous positions for position change indicators
_previous_positions = {}


def get_position_indicator(car_number, current_position):
    """
    Get position change indicator
    Returns: '↑' (green) if improved, '↓' (red) if worsened, ' ' if same
    """
    previous = _previous_positions.get(car_number, current_position)
    
    if current_position < previous:
        # Moved up (lower position number is better)
        indicator = Colors.GREEN + "↑" + Colors.ENDC
    elif current_position > previous:
        # Moved down
        indicator = Colors.RED + "↓" + Colors.ENDC
    else:
        # Same position
        indicator = " "
    
    # Update for next time
    _previous_positions[car_number] = current_position
    
    return indicator


def get_flag_color(flag_status):
    """Return colored flag status string"""
    flag_upper = flag_status.upper()
    
    if flag_upper == "GREEN":
        return Colors.GREEN + Colors.BOLD + "GREEN" + Colors.ENDC
    elif flag_upper == "YELLOW":
        return Colors.YELLOW + Colors.BOLD + "YELLOW" + Colors.ENDC
    elif flag_upper == "RED":
        return Colors.RED + Colors.BOLD + "RED" + Colors.ENDC
    elif flag_upper == "WHITE":
        return Colors.WHITE + Colors.BOLD + "WHITE" + Colors.ENDC
    elif flag_upper == "CHECKERED":
        return Colors.WHITE + Colors.BOLD + "CHECKERED" + Colors.ENDC
    else:
        return flag_status


def render_live(layout):
    """Render live race view with enhanced features"""
    header = layout["header"]
    
    print("=" * 60)
    flag_colored = get_flag_color(header['flag'])
    
    # Show laps to go if available
    if 'lapsToGo' in header and header.get('lapsToGo') is not None:
        print(f"{flag_colored:<20}  Lap {header['lap']}/{header['total']}  " + 
              f"({Colors.CYAN}{header['lapsToGo']} to go{Colors.ENDC})")
    else:
        print(f"{flag_colored:<20}  Lap {header['lap']}/{header['total']}")
    
    print("=" * 60)

    def render_row(car):
        # Position change indicator
        pos_indicator = get_position_indicator(car['car'], car['position'])
        
        # Battle indicator (within 0.15s)
        battle = Colors.YELLOW + "*" + Colors.ENDC if car.get("battling", False) else " "
        
        # Interval display
        interval = "LEADER" if car.get("interval") is None else f"+{car['interval']:.3f}"
        
        # Status indicators
        status_flags = ""
        if not car.get("isOnTrack", True):
            status_flags += Colors.RED + " [OFF]" + Colors.ENDC
        if car.get("isOnDVP", False):
            status_flags += Colors.YELLOW + " [DVP]" + Colors.ENDC
        
        # Passing differential (if available and significant)
        passing_diff = car.get("passingDifferential", 0)
        if passing_diff > 0:
            diff_str = Colors.GREEN + f" +{passing_diff}" + Colors.ENDC
        elif passing_diff < 0:
            diff_str = Colors.RED + f" {passing_diff}" + Colors.ENDC
        else:
            diff_str = ""
        
        print(f"{battle}{pos_indicator} {car['position']:>2}  #{car['car']:<3}  "
              f"{car['driver']:<12}  {interval:>7}{status_flags}{diff_str}")

    # Render fixed top 10
    for car in layout["fixed"]:
        render_row(car)

    print("-" * 60)

    # Render scrolling section
    for car in layout["scrolling"]:
        render_row(car)


def render_points(layout):
    """Render points standings"""
    header = layout.get("header", {})
    print("=" * 60)
    title = header.get("title", "NASCAR CUP SERIES POINTS")
    print(f"{Colors.BOLD}{title:^60}{Colors.ENDC}")
    print("=" * 60)

    for driver in layout["drivers"]:
        interval = "LEADER" if driver.get("pointsBack") == 0 else f"-{driver['pointsBack']}"
        
        # Color code top 3
        if driver['position'] == 1:
            pos_color = Colors.YELLOW + Colors.BOLD
        elif driver['position'] == 2:
            pos_color = Colors.WHITE + Colors.BOLD
        elif driver['position'] == 3:
            pos_color = Colors.CYAN + Colors.BOLD
        else:
            pos_color = ""
        
        print(f"{pos_color}{driver['position']:>2}{Colors.ENDC}  "
              f"#{driver['car']:<3}  {driver['driver']:<12}  {interval:>7}")


def render_schedule(layout):
    """Render schedule view"""
    print("=" * 70)
    print(f"{Colors.BOLD}{layout['header'].center(70)}{Colors.ENDC}")
    print("=" * 70)

    for race in layout["rows"]:
        # Chase/playoff indicator
        if race.get("isChase", False):
            chase_marker = Colors.YELLOW + "🏆" + Colors.ENDC
        else:
            chase_marker = "  "
        
        # Series color coding
        series = race.get("series", "")
        if series == "CUP":
            series_color = Colors.BOLD + Colors.YELLOW
        elif series == "XFINITY":
            series_color = Colors.GREEN
        elif series == "TRUCKS":
            series_color = Colors.RED
        else:
            series_color = ""
        
        line = (
            f"{chase_marker} {race['date']}  "
            f"{race['time']:<5}  "
            f"{race['name']:<35}  "
            f"{race['broadcast']:<5}  "
            f"{series_color}{series:<8}{Colors.ENDC}"
        )

        print(line)


def clear_position_history():
    """Clear position change tracking (call when switching modes)"""
    global _previous_positions
    _previous_positions = {}