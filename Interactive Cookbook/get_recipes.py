from get_directions import get_directions
from fetchURL import fetchURL
import sys

def main():
	if len(sys.argv) < 2:
		print("Please give a recipe url.")
	else:
		url = ''.join(sys.argv[1])
		fetchURL(url)
		get_directions(url)

if __name__ == '__main__':
	main()