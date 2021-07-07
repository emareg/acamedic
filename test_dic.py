import sys
sys.path.insert(0, './tests')

print("Testing Syntax:")
print("-----------------------")
import test_syntax

print("\n\nTesting for duplicates:")
print("-----------------------")
import test_duplicates

print("\n\nTesting correctness:")
print("-----------------------")
import test_correctness

print("\n\nTesting consistency:")
print("-----------------------")
import test_consistency