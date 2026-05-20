Binary search is a highly efficient search [[algorithm]] that operates on sorted collections of [[data]]. It employs a divide-and-conquer strategy to repeatedly divide the search space in half, making it significantly faster than linear search for large datasets. The [[algorithm]]'s elegant simplicity belies its powerful impact on [[computer science]] and practical applications.

## Mathematical Foundation

Binary search reduces the search space by half in each step, leading to a logarithmic [[time complexity]]. For a collection of size n, the maximum number of steps required is:

$\lfloor \log_2(n) \rfloor + 1$

This logarithmic efficiency makes binary search extremely scalable for large datasets.

## Core [[Algorithm]] Implementation

The basic implementation of binary search can be expressed recursively or iteratively:

### Iterative Implementation

```
def binary_search(arr, target):
	left, right = 0, len(arr) - 1
	while left <= right:
		mid = left + (right - left) // 2  # Avoid potential integer overflow
		if arr[mid] == target:
			return mid
		elif arr[mid] < target:
			left = mid + 1
		else:
			right = mid - 1
	return -1  # Element not found
```

### Recursive Implementation

```
def binary_search_recursive(arr, target, left, right):
	if left > right:
		return -1
		
	mid = left + (right - left) // 2
	
	if arr[mid] == target:
		return mid
	elif arr[mid] < target:
		return binary_search_recursive(arr, target, mid + 1, right)
	else:
		return binary_search_recursive(arr, target, left, mid - 1)
```

## Variants and Extensions

### Finding Insertion Point

Binary search can be modified to find the correct insertion point for a new element:

```
def binary_search_insert(arr, target):
	left, right = 0, len(arr)
	
	while left < right:
		mid = left + (right - left) // 2
		if arr[mid] < target:
			left = mid + 1
		else:
			right = mid
	return left
```

### Finding Range Boundaries

For duplicates, we can find the first and last occurrences:

```
def binary_search_boundaries(arr, target):
	def find_first():
		left, right = 0, len(arr) - 1
		
		while left <= right:
			mid = left + (right - left) // 2
			if arr[mid] == target and (mid == 0 or arr[mid-1] < target):
				return mid
			elif arr[mid] < target:
				left = mid + 1
			else:
				right = mid - 1
				return -1
				
			def find_last():
				left, right = 0, len(arr) - 1
				while left <= right:
					mid = left + (right - left) // 2
					if arr[mid] == target and (mid == len(arr)-1 or arr[mid+1] > target):
						return mid
					elif arr[mid] > target:
						right = mid - 1
					else:
						left = mid + 1
					return -1
				return (find_first(), find_last())
```

## Performance Analysis

### [[Time Complexity]]

- Best Case: O(1) - target found at midpoint
- Average Case: O(log n)
- Worst Case: O(log n)

### [[Space Complexity]]

- Iterative: O(1)
- Recursive: O(log n) due to call stack

## Common Applications

### [[Database]] Systems

Binary search is fundamental in:

- Index searching
- Range queries
- Finding insertion points in B-trees

### System Programming

Used in:

- Memory allocation [[Algorithm|algorithms]]
- Process scheduling
- Resource management

### Numerical Computations

Applied in:

- Root finding [[Algorithm|algorithms]]
- [[Optimization]] problems
- Numerical integration

## Implementation Considerations

### Edge Cases

Careful attention must be paid to:

- Empty arrays
- Single-element arrays
- Duplicate elements
- Boundary conditions

### Floating-Point Considerations

When working with floating-point numbers:

```
def binary_search_float(arr, target, epsilon=1e-10):
	left, right = 0, len(arr) - 1
	while left <= right:
		mid = left + (right - left) // 2
		if abs(arr[mid] - target) < epsilon:
			return mid
		elif arr[mid] < target:
			left = mid + 1
		else:
			right = mid - 1
		return -1
```

## Advanced Topics

### Interpolation Search

An improvement over binary search for uniformly distributed [[data]]:

```
def interpolation_search(arr, target):
	left, right = 0, len(arr) - 1
	while left <= right and target >= arr[left] and target <= arr[right]:
		if left == right:
			return left if arr[left] == target else -1                     pos = left + ((right - left) * (target - arr[left])) // (arr[right] - arr[left])
		if arr[pos] == target:
			return pos
		elif arr[pos] < target:
			left = pos + 1
		else:
			right = pos - 1
		return -1
```