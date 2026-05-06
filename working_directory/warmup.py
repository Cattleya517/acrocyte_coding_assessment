"""Print a random LeetCode warmup URL.

Usage: uv run python warmup.py
"""
import random

PROBLEMS = [
    "https://leetcode.com/problems/fizz-buzz/",
    "https://leetcode.com/problems/reverse-string/",
    "https://leetcode.com/problems/length-of-last-word/",
    "https://leetcode.com/problems/jewels-and-stones/",
    "https://leetcode.com/problems/number-of-1-bits/",
    "https://leetcode.com/problems/contains-duplicate/",
    "https://leetcode.com/problems/missing-number/",
    "https://leetcode.com/problems/single-number/",
]


def main() -> None:
    url = random.choice(PROBLEMS)
    print("Your warmup problem:")
    print(f"  {url}")
    print()
    print("Solve it on leetcode.com. AI assistance is NOT allowed for this part.")


if __name__ == "__main__":
    main()
