from get_url import get_url
from series import series
from films import films


def main():
    url, t, title = get_url()  # Try to get existing and complete url
    title = ''.join(char for char in title if char.isalnum() or char == " ")
    if t:
        series(url, t, title)
    else:
        films(url, title)


if __name__ == "__main__":
    main()
