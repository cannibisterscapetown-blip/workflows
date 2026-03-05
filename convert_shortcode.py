def shortcode_to_id(shortcode):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
    media_id = 0
    for char in shortcode:
        media_id = media_id * 64 + alphabet.index(char)
    return media_id

shortcode = "DTZzjbrDYzC"
media_id = shortcode_to_id(shortcode)
print(f"Shortcode: {shortcode}")
print(f"Media ID: {media_id}")
