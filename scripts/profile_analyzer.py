import pstats
import argparse
import sys

def analyze_profile(stats_file: str) -> None:
    """
    Loads and prints formatted statistics from a cProfile output file.

    Prints three sections:
    1. Top 15 functions by total time (exclusive of sub-calls).
    2. Top 15 functions by cumulative time (inclusive of sub-calls).
    3. Top 15 functions by number of calls.

    Args:
        stats_file (str): Path to the standard cProfile binary output file.
    """
    try:
        # load the stats file
        stats = pstats.Stats(stats_file)
    except FileNotFoundError:
        print(f"Error: File not found at '{stats_file}'")
        sys.exit(1)
    except Exception as e:
        # Catch generic errors potentially caused by corrupted or incompatible binary files
        print(f"Error loading stats file '{stats_file}': {e}")
        sys.exit(1)

    print("="*20, "PROFILING RESULTS", "="*20)
    print(f"Source file: {stats_file}\n")

    # Sort by 'total time' (tottime) and print the top 15 functions
    print("--- Top 15 by Total Time (tottime) ---")
    print("(Time spent *inside* the function, excluding sub-calls)")
    stats.sort_stats("tottime").print_stats(15)

    # Sort by 'cumulative time' (cumtime) and print the top 15
    print("\n" + "---" * 10)
    print("--- Top 15 by Cumulative Time (cumtime) ---")
    print("(Time spent in function *and* all sub-calls)")
    stats.sort_stats("cumtime").print_stats(15)
    
    # Sort by 'number of calls' (ncalls)
    print("\n" + "---" * 10)
    print("--- Top 15 by Number of Calls (ncalls) ---")
    stats.sort_stats("ncalls").print_stats(15)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze and print readable statistics from a cProfile binary file."
    )
    parser.add_argument(
        "stats_file",
        type=str,
        help="Path to the cProfile stats file to analyze."
    )

    args = parser.parse_args()
    analyze_profile(args.stats_file)